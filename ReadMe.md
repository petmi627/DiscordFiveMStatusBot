# Discord FiveM Status Bot

This is a small discord bot, that checks the status of a FiveM server.

## Installation

Please clone the repository and navigate to the working directory and build the Docker container.

```bash
docker build -t dicord-fivem-status-bot .
```

After the operation you can start the bot, you need to change the variables as you need it.

```bash
docker run --detach -e "token=[Your Token]" -v "${PWD}/config.json:config.json" --name dicord-bot-fivem-status dicord-fivem-status-bot
```

## Usage

In discord, mention the bot name and type help to get a list with commands

Type "$status" to get the status

Type "$players" to get the players connected
