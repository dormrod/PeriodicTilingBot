"""
Script to get @mentions to bot in given time window
"""

import sys
import yaml
import datetime
import requests

ACCOUNT_NAME = "procrystalbot"
KEYWORD = "keyword"

def main():

    tweet_ids = get_tweet_ids()
    write_tweet_ids(tweet_ids)

    seed_parameters = read_seed_parameters()
    update_seed_parameters(seed_parameters, len(tweet_ids))


def get_tweet_ids():
    """Get Tweet IDs mentioning keyword from Twitter API"""

    # Read bearer token from secrets file
    with open("./secrets.yml", "r") as f:
        bearer_token = yaml.load(f, Loader=yaml.FullLoader)["BEARER_TOKEN"]

    # Set start and end times as current time rounded down to nearest minute with supplied offset
    dt_fmt = "%Y-%m-%dT%H:%M:00Z"
    dt_now = datetime.datetime.now().replace(second=0, microsecond=0)
    start_time_offset = int(sys.argv[1])
    end_time_offset = int(sys.argv[2])
    dt_end = dt_now - datetime.timedelta(minutes=end_time_offset)
    dt_start = dt_now - datetime.timedelta(minutes=start_time_offset)
    dt_end = dt_end.strftime(dt_fmt)
    dt_start = dt_start.strftime(dt_fmt)

    # Make request, checking for mentions in specified time period
    uri = "https://api.twitter.com/2/tweets/search/recent"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    query = {"query": f"@{ACCOUNT_NAME}",
             "start_time" : dt_start,
             "end_time" : dt_end}
    response = requests.get(uri, headers=headers, params=query)

    # Get tweet ids from tweets with specified keyword
    tweet_ids = []
    if response.status_code == 200:
        content = response.json()
        num_results = content["meta"]["result_count"]
        if num_results > 0:
            for result in content["data"]:
                if KEYWORD in result["text"].lower():
                    tweet_ids.append(result["id"])

    # Log response if fails
    else:
        with open(f"../../output/logs/{dt_now.strftime(dt_fmt)}", "w") as f:
            f.write("{} \n {} \n {} ".format(query, response.status_code, response.content))

    return tweet_ids


def write_tweet_ids(tweet_ids):
    """Write Tweet IDs to temporary file"""

    with open("../../output/ids.tmp", "w") as f:
        if len(tweet_ids)>0:
            yaml.dump(tweet_ids, f)


def read_seed_parameters():
    """Read seed parameters from temporary file"""
    """Read seed parameters from temporary file"""

    with open("../../output/seed.tmp", "r") as f:
        seed = int(f.readline())
        samples = int(f.readline())
    return (seed, samples)


def update_seed_parameters(parameters, samples):
    """Update seed file with new starting seed and number of samples to be generated"""

    with open("../../output/seed.tmp", "w") as f:
        f.write(f"{parameters[0]+parameters[1]}\n")
        f.write(f"{samples}")


if __name__ == "__main__":
    main()