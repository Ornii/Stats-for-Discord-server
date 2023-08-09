# Stats-for-Discord-server
## Presentation

It's a Python script for a Discord bot that makes stats for your discord server. The bot analyzes every messages that have been dent on this server.
It gives a .txt document with the wanted data. This bot **doesn't store the messages content**. For every messages that have been sent on the server,  stores the date + the message author + the type.

## Installation

1. Install Python: https://www.python.org/downloads/
2. Download python module discord and the module discord.ext with: `pip install discord` and `pip install discord.ext`
3. Create a discord application: https://discordpy.readthedocs.io/en/stable/discord.html
4. Get and copy your token: https://discord.com/developers/applications (click on: [your bot]/Bot/Reset Token/Yes do it!/Copy)
5. On the same page, check Presence intent, Server members intent and Message content intent (all on on)
6. Then, paste in script.py in line 6 the Token between the "
7. Invite your bot to the server where you want to make stats: https://discord.com/developers/applications (click on: [your bot]/OAuth2/URL Generator)
Check at least: Read messages/View Channels + Send Messages + Read Message History + Use Slash Commands

## Utilisation

1. `/makestats` channel makes data just for the channel where the message has been sent.
Otherwise: `/makestats server` makes data for every channel in the server where the message has been sent.
The data is stored in a folder inside the main folder where the script is located. The name of the data folder is <data_guild_ + the id ofnyour setver>. 
Inside this folder, there are files named data_channel_ + id of channels of the server.
In theses files, each row is dedicated for only one author
2. `/numberofmessages` gives the count of messages in the wanted server
3. '/numberofmember'gives the count of different members that have sent one or more messages in the server

