# ProcrystalTwitterBot

Twitter bot to send ascii art 8x8 procrystals to users who @ mention it.

## Setup

1) Run `initialise_db.py` which generates `procrystaldb.db` SQLite database.
2) Manually set up an S3 bucket called `procrystals` and add the database.
3) Compile the procrystals code i.e. `cmake . ;  make`
4) Initialise the empty directories `./output/` and `./output/logs/`.
5) Add secrets to `./src/twitter/secrets.yml`.

## Running

TBC

## Script Overview

Quick overview of the workings of various scripts

### spin_up.py

Run when starting up procrystalline session on new machine.

Pulls SQLite database from S3 bucket to ensure continuity of procrystal IDs.

Sets bio of bot to running.

### get_tweets.py

Gets all tweets containing @ mention in specified time period.

Stores username and tweet ID to SQLite database.

Makes temporary file with seed information for procrystals code.

### post_lattices.py

Checks database for tweets that need replying to and sends message.

Updates database if tweet was sent successfully.

### tear_down.py

Run when finishing session.

Push current database to S3 bucket.

Sets bio of bot to offline.

