import os
from token import fetch_token

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

def main():
   refreshed_token = fetch_token()

if __name__ == '__main__':
    main()
