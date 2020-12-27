"""
Script to spin up Procrystal bot.
1) Download sqlite database from S3
2) Post to Twitter and change bio
"""


import sys
import yaml
import requests
import boto3
import post_lattices


def fetch_database():
    """
    Get copy of most recent database from S3.
    """

    with open("./secrets.yml", "r") as f:
        secrets = yaml.load(f, Loader=yaml.FullLoader)
        access_key = secrets["AWS_ACCESS_KEY"]
        secret_key = secrets["AWS_SECRET_KEY"]

    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    s3.download_file('procrystals', 'procrystaldb.db', '../database/procrystaldb.db')


def set_bio_running():
    """
    Set Twitter bio to running.
    """

    bio = """
    Tweeting 8x8 procrystalline lattices to the world since 2021.

Status: testing 🟠

🔗 https://journals.aps.org/pre/abstract/10.1103/PhysRevE.102.062308 
    """

    uri = f" https://api.twitter.com/1.1/account/update_profile.json?description={bio}"
    response = requests.request("POST", url=uri, auth=post_lattices.generate_auth())


if __name__ == "__main__":
    fetch_database()
    set_bio_running()
