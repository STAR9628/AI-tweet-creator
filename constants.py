import tweepy

API_KEY = "2MicHzKAmSAYfG0P7a7evRMvs"
API_SECRET_KEY = "beVTdQviwzBbZiBZo93O4P5ncZ3u5rdY9urBZ33bV9nWRqO912"
ACCESS_TOKEN = "944088005056200705-hs9JDShmwvCXcrEzp2SlOOCMaGcyzJG"
ACCESS_TOKEN_SECRET = "khSJFTROXY29kPa3vBYBjBWlg9C9yacS9W2ioToNKkPn7"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAMaM3gEAAAAA3DTLhJh8YhIdjmCAu7B73OAUJcs%3DtmRW3ilYHJvfMNIoY7yKtuxIdKQQj4XFm4Ame42tLhb0UPK7sK"

twitter_client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True,
)