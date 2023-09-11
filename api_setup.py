import openai
import os
import sys

def setup_api_key():
    try:
        openai.api_key = os.environ['OPENAI_API_KEY']
    except KeyError:
        sys.stderr.write("""
        You haven't set up your API key yet.
        ...
        """)
        exit(1)

setup_api_key()
