
import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_functions import available_functions, call_function
from config import MAX_ITERATIONS
import sys


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key is None:
    raise RuntimeWarning("empty key")


parser = argparse.ArgumentParser(description="Franco")
parser.add_argument("user_prompt", type=str, help="Dì pure a Franco, Franco è qui per te")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

client = genai.Client(api_key=api_key)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("API failed")

    used = response.usage_metadata
    if verbose:
        print(f"Prompt tokens: {used.prompt_token_count}")
        print(f"Response tokens: {used.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose=verbose)

        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
            or not function_call_result.parts[0].function_response.response
        ):
            raise RuntimeError("Empty function response")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_results.append(function_call_result.parts[0])

    messages.append(types.Content(role="user", parts=function_results))

    return None

def main():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(MAX_ITERATIONS):
        final_text = generate_content(client, messages, args.verbose)
        if final_text is not None:
            print("Final response:")
            print(final_text)
            return

    print(f"Maximum iterations ({MAX_ITERATIONS}) reached")
    sys.exit(1)

if __name__ == "__main__":
    main()
                              
