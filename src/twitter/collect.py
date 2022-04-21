import datetime
import json
import os

from twarc import Twarc2, expansions


# credits: https://github.com/twitterdev/getting-started-with-the-twitter-api-v2-for-academic-research/blob/main/modules/6a-labs-code-academic-python.md (accessed 20/04/2022)
def search_tweets():
    # Twitter API client
    client = Twarc2(bearer_token=os.environ.get("TWITTER_API_TOKEN"))

    # 1 week before start of EURO2020
    start_time = datetime.datetime(2021, 6, 4, 0, 0, 0, 0, datetime.timezone.utc)

    # 1 week after end of EURO2020
    end_time = datetime.datetime(2021, 7, 18, 0, 0, 0, 0, datetime.timezone.utc)

    # collect tweets related to official account or hashtag
    query = "@EURO2020 OR #EURO2020"

    # The search_all method call the full-archive search endpoint to get Tweets based on the query, start and end times
    search_results = client.search_all(query=query, start_time=start_time, end_time=end_time, max_results=100)

    for page in search_results:
        result = expansions.flatten(page)
        for tweet in result:
            print(f"Tweet: {json.dumps(tweet, indent=4)}")

            # timestamp (UNIX time)
            created_at = tweet["created_at"]
            timestamp = int(datetime.datetime.strptime(
                created_at, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc).timestamp())  # second resolution is enough
            print(f"Tweet date: {created_at}")
            print(f"Tweet timestamp: {timestamp}")

            # hashtags
            hashtags = []
            try:
                hashtags = tweet["entities"]["hashtags"]
                hashtags = list(set([h["tag"] for h in hashtags]))    # remove duplicates
            except KeyError:
                pass

            # mentions
            mentions = []
            try:
                mentions = tweet["entities"]["mentions"]
                mentions = list(set([m["username"] for m in mentions]))    # remove duplicates
            except KeyError:
                pass

            # tweet author
            author = tweet["author"]["username"]

            print("Hashtags: ", hashtags)
            print("Author: ", author)
            print("Mentions: ", mentions)

            # edges
            user_mentions = [(author, m) for m in mentions]
            user_hashtag = [(author, h) for h in hashtags]

            hashtag_hashtag = []    # hashtag co-occurrence
            for i, h1 in enumerate(hashtags):
                hashtag_hashtag.extend([(h1, h2) for h2 in hashtags[i + 1:]])

            user_user = []    # user co-occurrence
            for i, u1 in enumerate(mentions):
                user_user.extend([(u1, u2) for u2 in mentions[i + 1:]])

            print("Edges user mentions: ", user_mentions)
            print("Edges user hashtag: ", user_hashtag)
            print("Edges hashtag co-occurrence: ", hashtag_hashtag)
            print("Edges user co-occurrence: ", user_user)
