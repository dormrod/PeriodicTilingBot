"""
Script to post generated procrystalline lattices in reply to specific tweet ids
"""

import os.path
import yaml
import logging
from log_handling import setup_logger
import requests
import sqlite3
from requests_oauthlib import OAuth1


def main():

    pro_ids, usernames, tweet_ids = get_pending_tweets()

    if usernames is not None:
        auth = generate_auth()
        reply_to_tweets(pro_ids, usernames, tweet_ids, auth)


def get_pending_tweets():
    """Get procrystal ids, usernames and tweet ids from database"""

    # Make connection to local database
    connection = sqlite3.connect("../database/procrystaldb.db")
    cursor = connection.cursor()

    # Get all pending tweets in database
    logging.info("Getting pending tweets from database")
    cursor.execute("SELECT procrystal_id, username, tweet_id FROM Twitter WHERE reply_sent=FALSE;")
    rows = cursor.fetchall()
    connection.close()

    # Check procrystal file exists and if so add to pending
    pro_ids = []
    usernames = []
    tweet_ids = []
    logging.info(f"Pending tweets found: {len(rows)}")
    for row in rows:
        pro_id, username, tweet_id = row
        if os.path.isfile(f"../../output/sq3_sample_{pro_id}.dat"):
            pro_ids.append(pro_id)
            usernames.append(username)
            tweet_ids.append(tweet_id)
        else:
            logging.warning(f"Pending tweet with procrystal id {pro_id} has no matching procrystal file")

    return pro_ids, usernames, tweet_ids


def generate_auth():
    """Generate OAuth1"""

    with open("./secrets.yml", "r") as f:
        secrets = yaml.load(f, Loader=yaml.FullLoader)
    api_key = secrets["API_KEY"]
    api_secret_key = secrets["API_SECRET_KEY"]
    access_token = secrets["ACCESS_TOKEN"]
    access_token_secret = secrets["ACCESS_TOKEN_SECRET"]

    return OAuth1(api_key, api_secret_key, access_token, access_token_secret,
                  signature_method="HMAC-SHA1", signature_type='query')


def reply_to_tweets(pro_ids, usernames, tweet_ids, auth):
    """Reply to Tweet with procrystal and update database with successes"""

    connection = sqlite3.connect("../database/procrystaldb.db")
    logging.info("Sending procrystals")
    for i, pro_id in enumerate(pro_ids):
        username = usernames[i]
        tweet_id = tweet_ids[i]
        logging.info(f"Reading lattice {pro_id}")
        lattice = read_lattice(pro_id)
        success = post_lattice(pro_id, username, tweet_id, lattice, auth)
        if success:
            update_sent_status(pro_id, connection)
    connection.close()


def read_lattice(id):
    """Read lattice with corresponding procrystal id"""

    with open(f"../../output/sq3_sample_{id}.dat", "r") as f:
        lattice = f.read()
    return lattice[:-3]


def post_lattice(pro_id, user, tweet_id, lattice, auth):
    """Post lattice in response to Tweet"""

    logging.info(f"Replying to tweet {tweet_id}")
    content = f"Here's your procrystal (%23{pro_id}) @{user}!\n\n{lattice}"
    uri = f"https://api.twitter.com/1.1/statuses/update.json?status={content}&in_reply_to_status_id={tweet_id}"
    response = requests.request("POST", url=uri, auth=auth)
    if response.status_code == 200:
        logging.info("Tweet successfully sent")
    else:
        logging.info(f"Tweet errored with: {response.json()}")
    return response.status_code == 200


def update_sent_status(pro_id, connection):
    """Update sent status of successfully sent Tweets in database"""

    cursor = connection.cursor()
    cursor.execute(f"UPDATE TWITTER SET reply_sent=TRUE WHERE procrystal_id={pro_id};")
    connection.commit()


if __name__ == "__main__":
    setup_logger("../../output/logs/post_lattices.log")
    main()