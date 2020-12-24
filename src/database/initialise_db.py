"""
Initialises database used to record tweets.
"""

import sqlite3

def initialise_database(db_file, table_name, create_sql):
    """
    Drop existing table if present and make initialise new table.
    """

    # Connect to database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Delete previous table
    delete_sql = f"""
    DROP TABLE IF EXISTS {table_name};
    """
    cursor.execute(delete_sql)

    # Create new table
    cursor.execute(create_sql)

    # Close connection
    connection.close()


def initialise_tweet_database():
    """
    Initialise Twitter table for storing inbound and outbound Tweet information.
    """

    twitter_sql = """
    CREATE TABLE Twitter (
        procrystal_id integer PRIMARY KEY,
        tweet_id text not null,
        username text not null,
        reply_sent bool not null,
        UNIQUE(tweet_id)
    )
    """
    initialise_database("./procrystaldb.db", "Twitter", twitter_sql)


if __name__ == "__main__":
    initialise_tweet_database()
