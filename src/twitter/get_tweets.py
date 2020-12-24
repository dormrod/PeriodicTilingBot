"""
Script to get @mentions to bot in given time window
"""

import sys
import yaml
import datetime
import requests
import sqlite3

ACCOUNT_NAME = "procrystalbot"
# KEYWORD = "keyword"

def main():

    rows_added = get_tweets()
    seed_parameters = read_seed_parameters()
    update_seed_parameters(seed_parameters, rows_added)


def get_tweets():
    """Get Usernames and Tweet IDs of tweets mentioning keyword from Twitter API.
    Store in local database.
    """

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
             "expansions" : "author_id",
             "user.fields" : "username",
             "start_time" : dt_start,
             "end_time" : dt_end}
    response = requests.get(uri, headers=headers, params=query)

    # Make connection to local database
    connection = sqlite3.connect("../database/procrystaldb.db")
    cursor = connection.cursor()

    # Get current total number of rows in database
    cursor.execute("SELECT COUNT(*) FROM Twitter;")
    initial_rows = cursor.fetchall()[0][0]

    # Get usernames and tweet ids from tweets and save to database
    if response.status_code == 200:
        content = response.json()
        num_results = content["meta"]["result_count"]
        if num_results > 0:
            # First get dictionary of usernames
            user_id_to_name = {}
            for user in content["includes"]["users"]:
                user_id_to_name[user["id"]] = user["username"]
            # Then get tweet id, username and save to database
            for result in content["data"]:
                # if KEYWORD in result["text"].lower():
                    tweet_id = result["id"]
                    username = user_id_to_name[result["author_id"]]
                    sql_insert = f"""
                    INSERT OR IGNORE INTO Twitter (tweet_id, username, reply_sent)
                    VALUES ('{tweet_id}', '{username}', false);
                    """
                    cursor.execute(sql_insert)

    # Log response if fails
    else:
        with open(f"../../output/logs/{dt_now.strftime(dt_fmt)}", "w") as f:
            f.write("{} \n {} \n {} ".format(query, response.status_code, response.content))

    # Get final total number of rows in database and therefore number of rows added
    cursor.execute("SELECT COUNT(*) FROM Twitter;")
    final_rows = cursor.fetchall()[0][0]
    rows_added = final_rows - initial_rows

    # Close database connection
    connection.commit()
    connection.close()

    return rows_added


def read_seed_parameters():
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