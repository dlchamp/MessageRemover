A fulfilled request from a user on [r/discord_bots](https://reddit.com/r/discord_bots)

This is a simple bot that allows you to bulk remove messages from a channel with a highly configurable slash command.

## Prerequisites
### Requirements and Dependencies
This project is written using Python version 3.9.10 and dependencies are managed with Poetry. 
To get started:

1. Download and install [Python 3.9.10](https://www.python.org/downloads/release/python-3910/) or newer
2. Pull a copy of the bot by selecting the green `Code` button, then `Download Zip`
3. Extract the main directory from the downloaded zip
4. Navigate to the root of the main project directory 
5. Open command prompt inside this directory
5. Install Poetry with `pip install poetry==1.1.13`
6. While still inside the project root, run `poetry install` - This will create a virtual environment for the project and install all required dependencies

### Create a new bot application
1. Navigate to https://discord.com/develoeprs/applications (sign-in if needed)
2. Select `New Application`
3. Give it a name - This will be your application's name and also your bot's name as it appears in server's members lists (it can be changed later)
4. Select `Bot` in the left-side navigation panel
5. Select `Add Bot`
6. Enabled the following `Privileged Gateway Intents:
    - Server Members Intents
    - Message Content Intents
7. Select the `Reset Token` button to generate your bot's secret token
    - **BEWARE**: This token is for your eyes only.  Do not share this token as anyone with it has full control of your application/bot account and any servers that it is connected to
    - **WARNING**: This token is hidden once you leave this page.  If you lose it you WILL have to regenerate a new one
8. Copy the token and paste it somewhere safe for now.  You'll need it later
9. Finally, navigate to `Oauth2` > `URL Generator` and select the following options to create an invite link with the correct permissions for this bot to work
    - Scopes:
        - bot
        - applications.commands
    - Bot Permissions
        - Read Messages/View Channels
        - Send Messages
        - Manage Messages
        - Read Message History
10. Copy the generated URL at the bottom of the page and paste it into your browser, or in your Discord client.  This link will invite your bot application to your server.


### Preparing the bot script
1. Go into the root of the project folder you downloaded and extracted earlier and open the sample.env file - paste the token you copied from earlier after the `TOKEN=`, then save as `.env`

#### Optional step
Slash commands require API registration with Discord and this registration for new bots/commands can take up to an hour.  To bypass this, during development you can add your server's ID to the script which tells Discord to register the commands in this bot immediately for ONLY the guild IDs included.  If you do not do this, commands will register globally and be available to any guild the bot is added to after initial registration

To do this, navigate into the `/messageremover` directory and open bot.py with any text editor or IDE.  Near the top of the script you'll find this section of code:

```
# Configure bot's gateway intents and instantiate the Interaction bot object
# add guild IDs into test_guilds to prevent global registration and instantly have commands
# working with guilds whose IDs are in this list (ex: test_guilds=[1234456789,54433635533,342234234344])
intents = Intents.default()
intents.members = True
intents.message_content = True
bot = commands.InteractionBot(intents=intents, test_guilds=[])
```

### Bot is now ready to run
Open command prompt to the main project directory (where `main.py` is) and run it with the following commands.    

`poetry shell`  to enter into the virtual environment we created earlier  
`python main.py` to run the bot script



## Using the Bot
##### Command options
All of the command arguments are optional, however, to get the most out of the command, you should always set a `limit` as this defaults to 1 if no number is included.   
*Note:  Due to API limitations from Discord, messages older than 14 days may take longer to be fetched and deleted.*

|argument|description|
--- | ---
channel | an optional channel that can be passed if you wish to target a channel while using the command in a different channel
with_terms | A comma separated list of terms to search for within a message. If ANY of the terms exist in the message, it will be deleted
without_terms | A comma separated list of terms to search for within a message. ALL items in the list must be present in the message for it to be deleted
limit | The max number of messages to iterate through, this does not mean that many messages will be deleted, but it could be
author | If any messages are from this author, they will be deleted

**Note: DO NOT use `with_terms` and `without_terms` together**
