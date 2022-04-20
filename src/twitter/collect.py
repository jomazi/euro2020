import datetime
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
            print("Tweet: ", tweet)
