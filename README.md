# Moderator Reaction Telegram Bot

A Telegram bot that records the time it takes for a moderator to respond.

## How Does it Work

When someone pings the moderator whose username is specified in the [config file](#configuration-file), the bot saves the message. Then, if the moderator reacts to this message with one of the specified reactions, the bot records how long it took them to do so. You can view the list of records using the /records command.

## Usage

At first rename `.env.dist` file to `.env` and fill or change values in it. Then run it with Docker compose:

```bash
docker compose up -d --build
```

## Configuration File

All bot settings stored in the `.env` file.

### Bot

- `BOT_TOKEN` - your bot token from [BotFather](https://botfather.t.me/)
- `CHAT_ID` - the chat where the bot will work (it starts with "-100")
- `USERNAME` - the moderator's username (case-insensitive)
- `REACTIONS` - the list of reactions that bot will handle

### Database

- `REDIS_HOST` - the hostname of the Redis server
- `REDIS_PORT` - the port on which Redis server is listening
- `PRUNE_TIME` - the time the bot will wait for a reaction to each message (in seconds)
- `RECORDS_LIMIT` - the maximum number of records in the record list