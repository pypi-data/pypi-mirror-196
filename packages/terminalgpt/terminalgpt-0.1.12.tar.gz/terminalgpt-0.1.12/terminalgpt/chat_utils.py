import readline
import time

import openai
import tiktoken
from colorama import Back, Fore, Style
from config import *

TIKTOKEN_ENCODER = tiktoken.get_encoding(ENCODING_MODEL)

def chat_loop(debug: bool, api_key: str):
    total_usage = 0
    openai.api_key = api_key
    messages = [
        INIT_SYSTEM_MESSAGE,
    ]

    while True:
        # Get user input
        user_input = input(Style.BRIGHT + "\nUser: " + Style.RESET_ALL)
        readline.add_history(user_input)
        usage = num_tokens_from_string(user_input)

        # Prevent reaching tokens limit
        while total_usage + usage >= LOCAL_TOKEN_LIMIT:
            # When reaching the limit, remove half of the oldest messages from the context
            while total_usage + usage >= LOCAL_TOKEN_LIMIT / 2:
                popped_message = messages.pop(0)
                total_usage -= num_tokens_from_string(popped_message["content"])

            if total_usage + usage < LOCAL_TOKEN_LIMIT:
                messages.insert(0, INIT_SYSTEM_MESSAGE)

        # Append to messages and send to ChatGPT
        messages.append({"role": "user", "content": user_input})

        # Get answer
        answer = get_answer(messages)

        # Parse usage and message from answer
        total_usage = answer["usage"]["total_tokens"]
        message = answer["choices"][0]["message"]["content"]

        # Append to messages list for next iteration keeping context
        messages.append({"role": "assistant", "content": message})

        # Print answer message
        print(Style.BRIGHT + "\nAssistant:" + Style.RESET_ALL)
        print_slowly(Fore.YELLOW + message + Style.RESET_ALL)

        # Print usage
        if debug:
            print(
                Back.LIGHTBLUE_EX
                + f"\nTotal Usage: {str(total_usage)} tokens"
                + Style.RESET_ALL
            )


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    num_tokens = len(TIKTOKEN_ENCODER.encode(string))
    return num_tokens


def get_answer(messages):
    answer = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return answer


def print_slowly(text, delay=0.02):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

