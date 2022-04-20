import argparse

from twitter import search_tweets

if __name__ == "__main__":
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--twitter", help="collect Twitter data", action="store_true")
    parser.add_argument("--euro2020", help="get EURO2020 information", action="store_true")

    args = parser.parse_args()

    # run task requested by user
    if args.twitter:
        search_tweets()
    elif args.euro2020:
        print("EURO2020")
