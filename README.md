# UEFA EURO 2020 Twitter Dataset

> Twitter dataset around the UEFA EURO 2020 soccer championship.  
> The official schedule can be found in the `data` directory or [here](https://editorial.uefa.com/resources/026a-126a09addc81-6f092f1f9f89-1000/euro2021_match_schedule_-_english_-_310521_20210601103927.pdf) (accessed 20/04/2022).

## Setup

1. Add Twitter API token to `.env` file: `echo "TWITTER_API_TOKEN=<BEARER_TOKEN>" >> .env`
2. Install Python packages: `pipenv install`
3. Run task: a.) `pipenv run twitter` to collect Twitter data b.) `pipenv run euro2020` to get EURO2020 related information
