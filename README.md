# Mediapart Discord Bot ![bot-preview](img/bot.png)

**[DISCLAIMER] The purpose of this bot is not to bypass Mediapart subscription. [Please support their work](https://www.mediapart.fr/abo/abonnement/normal).**

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/r0perice/mediapart-discord-bot/graphs/commit-activity)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](LICENSE)  

## <a name="summary"></a> Summary
1. [Main functionalities](#main-functionalities) 
2. [Deployment procedure](#deployment-procedure)
3. [Bot commands](#bot-commands)

## <a name="main-functionalities"></a>1. Main functionalities
* Retrieve Mediapart articles (only in french for the moment) each hour (configurable) and download then as PDF.
* Send the articles into a discord text channel (configurable).

![](img/bot_messages.png)

## <a name="deployment-procedure"></a>2. Deployment procedure

The installation procedure is given for Linux system (like [Ubuntu](https://ubuntu.com/)) but the bot is packaged as a Docker image, so it should work on all [Docker supported systems](https://docs.docker.com/engine/install/).

### Install docker

 The first step is to install Docker on your system.

> `apt update`  
> `apt install docker.io`

### Pull image

In the following command you need to replace the field `version` with the version you want to deploy.  
Most of the time it will be the latest version available [here](https://github.com/r0perice/mediapart-discord-bot/packages/269328).
> `docker pull docker.pkg.github.com/r0perice/mediapart-discord-bot/mediapart-discord_bot:version`

### Run the image

> `docker run -e MEDIAPART_USER="user_name" -e MEDIAPART_PWD="user_pwd" -e DISCORD_BOT_TOKEN="discord_token" -e CHANNEL_ID="channel_id" -v db-data:/tmp/mediapart_bot -it -d mediapart_discord_bot:version`

* `MEDIAPART_USER`: your Mediapart user name
* `MEDIAPART_PWD`: your Mediapart password
* `DISCORD_BOT_TOKEN`: if don't have one, see [how to retrieve it](https://discordpy.readthedocs.io/en/latest/discord.html)
* `CHANNEL_ID`: the id of the discord channel you want the Mediapart articles to appear (see [how to retrieve this ID](docs/get_discord_channel_id.md))
* `version`: the version of the bot you want to deploy (usually [latest version](https://github.com/r0perice/mediapart-discord-bot/packages/286811))
* (optional) `BOT_FETCH_TIME_HOURS`: the articles fetch time in hours, default is 1 hour.
* (optional) `db-data:/tmp/mediapart_bot`: on the left it is the name of the volume inside the container, on the right the folder on the host

## <a name="bot-commands"></a>3. Bot commands

Following commands can be sent to the bot as Direct Message.

* `!is-alive`: the bot will anwser you if it's alive
* `!logs`: send you a file containing the logs
* `!fetch-articles`: force articles fetching in the mediapart channel (only new articles)
