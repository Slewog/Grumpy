# Grumpy
> This is my discord bot wrote in python with discord.py to manage roles and more stuff

<ins>***Dependecies*** :</ins>
- Python 3.10 or more.
- discord.py
- python-dotenv

<ins>***File variable environments***:</ins>
- ```DISCORD_TOKEN``` the tokken of your bot available on discord developper portal.
- ```TEST_GUILD_ID``` Your development server ID (not required).
- ```LOG_LEVEL``` Set it to DEBUG for development (not required).
- ```COMMAND_PREFIX``` If you want get a custom command prefix during development  (not required).


# To do
- Check when the bot is added or removed from a guild.
- Detect when the bot is going off to do somestuff before shutdown.<br/><br/>
- Report an user.<br/><br/>
- Level system stored in a db with cache system.
- Add a new user on the cache system when i spawn on a guild.
- Load the levels system on the cache when the bot is booting.
- Sync cache and db every 3 or 5 min.
- Command to see your level on a guild.
- Delete the user from the levels manager and delete his data from the db.<br/><br/>
- Command to set the rules channel and the message ID (aadmin usage).
- Create a role react message from a view (admin usage).
- Detect if new user have react to the rules message before let him react for a role.
- Get a role when react to a message.
- Try to detect when an admin add/remove a role from discord to log that in a channel.<br/><br/>
- Add minigames (roll dice, etccc).
- Ask a joke to the bot by command.<br/><br/>
- Maybe create a dashboard to manage role reaction if not to hard (take a look at Flask).
- Delete message by qtty or just purge a channel.