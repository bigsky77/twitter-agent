import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "")
API_SECRET_KEY = os.getenv("API_SECRET_KEY", "")
API_KEY = os.getenv("API_KEY", "")
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "")

def main() -> None:
    """Entry point"""
    consumer_key = os.environ.get("API_KEY") or input("consumer_key: ")
    consumer_secret = os.environ.get("API_SECRET_KEY") or input("consumer_secret: ")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()

    print("\n" + auth_url, "\n")

    pin = input("PIN: ").strip()

    auth.get_access_token(pin)

    print()
    print(f"export API_KEY=\"{consumer_key}\"")
    print(f"export API_SECRET=\"{consumer_secret}\"")
    print(f"export ACCESS_TOKEN=\"{auth.access_token}\"")
    print(f"export ACCESS_TOKEN_SECRET=\"{auth.access_token_secret}\"")


if __name__ == "__main__":
    main()
