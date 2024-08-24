# Webhook scripts

This folder contains scripts that can be used with Discord webhooks to provide server
updates in Discord.

Right now it has two functions:

* updating he server status (player list, MOTD, etc.), and
* scraping potential coordinates mentioned in the in-game chat

## Setup

### Discord webhook

For each feature, go in to Channel Settings and access the Integration menu to
create a webhook. Copy the webhook URL(s) and set the environment variables as follows.

### Environment variables

If you are using pipenv to run, declare the variables in the `.env` file. Otherwise,
set them using `export`.

```dotenv
COORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
STATUS_WEBHOOK_URL=https://discord.com/api/webhooks/...
SERVER_ADDRESS=minecraftserver.com
STATUS_MESSAGE_ID=1234567891234
POLLING_INTERVAL=15
```

All fields are required, except `POLLING_INTERVAL`.

The two URLs are for the webhooks. `POLLING_INTERVAL` is the amount of time in seconds
to update. Around 15 seconds seems to be best without being rate-limited. If not provided,
the default interval is 30 seconds.

`STATUS_MESSAGE_ID` needs to be set **after** running the script for the first time. See below.

## Running

Using pipenv, you can start the script by running:

```shell
pipenv run webhooks path/to/logs
```

which is just a shortcut for:

```shell
python webhooks/run_webhooks.py path/to/logs
```

where `path/to/logs` is the path to the Minecraft server's log folder.

Upon running, a `last_read.json` file will be created at the cwd to keep track of the position of the log files.
The script will then **terminate**, asking you to set `STATUS_MESSAGE_ID`.
See [Server status/Additional setup](#server-status).

## Features

On each cycle, the following trigger:

### Coordinate scraping

The script will look for any player messages that look like there are important coordinates. Simply put,
it just looks for chat messages with a pair or triplet of numbers.

Once detected, it will be sent to Discord along with any text with the message.

### Server status

This displays some server information on Discord, including:

* server address (as set by `SERVER_ADDRESS`)
* server version
* server status (whether it is reachable through the address)
* number and preview of players online
* the message of the day (MOTD).

The channel chosen for this webhook should not be writable to the public and should be empty.
The webhook sends one message to the channel and will continually edit it to display the status (opposed to sending
constantly sending multiple messages).

> #### Additional setup
> After the first run, the webhook will send a message to the channel displaying the status
> and the script will terminate, returning the **message ID** for the status message.
> Set this value to `STATUS_MESSAGE_ID` and run the script again.

