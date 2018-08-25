# T-nk series project, Tunk
# Created by Alec "Tenj" Hinh
# This bot logs certain events and outputs them to a dedicated channel. Intended for server moderators and administrators.
# Included logging events are: Message edits/deletes, member joins/leaves, banning/unbanning, and more.
# It also includes certain server-specific features such as game role adding when a member starts playing a game.
# Requires at least Python 3.6 and Discord.py 1.0.0a (Rewrite branch) to run.

import discord
import os
import asyncio
import time
import datetime
import sys
import json
from discord.ext import commands
from datetime import datetime,tzinfo,timedelta

loggingchannels = []
ignoredchannels = []
ignoredservers = []


        
# Load Channels it will ignore
for line in open ("ignoredchannels.txt"):
    li = line.strip()
    if not li.startswith("#"):
        ignoredchannels.append(int(li))
# Load the servers that it will ignore
for line in open ("ignoredservers.txt"):
    li = line.strip()
    if not li.startswith("#"):
        ignoredservers.append(int(li))
# Static variables the bot will constantly call.
serverIDDict =  {
"Ishana": 159184581830901761,
"Eden": 82999036361048064
}
channelIDDict = {
"Ishana": 313703862798385162,
"Eden": 429425336204394506,
"IshanaSplunk": 477335474525175830
}

splunkIDDict = {
    "Ishana": 477335474525175830,
    "Eden": 429425336204394506
}

# Imports Json data for gameRoles on startup
gameRoleJsonFile = open('gameRoles.json')
gameRoleJsonFileRead = gameRoleJsonFile.read()
gameRoleJson = json.loads(gameRoleJsonFileRead)




# Import Json data for gameRoles
def loadGameRoles():
    gameRoleJsonFile = open('gameRoles.json')
    gameRoleJsonFileRead = gameRoleJsonFile.read()
    gameRoleJson = json.loads(gameRoleJsonFileRead)
    return

async def is_edenServer(ctx):
    return ctx.guild.id == 82999036361048064

start = time.time()
lastRestart = str(datetime.now())
banned = False
#client = discord.Client()
commandPrefix = 'tunk.'
client = commands.Bot(command_prefix=commandPrefix)
# Determines what channel the log will be sent to depending on what server the event was called in.
def getLoggingChannel(serverid):
    global serverIDDict
    global channelIDDict
    if serverid == serverIDDict['Ishana']:
        loggingchannel = channelIDDict['Ishana']
    elif serverid == serverIDDict['Eden']:
        loggingchannel = channelIDDict['Eden']
    else:
        return None
    return loggingchannel
# For one of the servers only, returns the role id with the matching game name sent by a member_update event.
def getGameRole(gameName):
    global gameRoleJson
    if gameName in gameRoleJson:
        gameRole = gameRoleJson[f'{gameName}']
        return gameRole
    elif 'dark souls' in gameName.lower():
        gameRole = 324304854434709508
        return gameRole
    else:
        return None
# Debug utility that finds the role ID with just the name of the role.
def findRoleID(roleName, message):
    result = discord.utils.find(lambda m: m.name == roleName, message.guild.roles)
    if result is not None:
        return str(result.id)
    else:
        return 0
# Same as logging channel, but for special logging events only.
def getSplunkChannel(serverid):
    global serverIDDict
    global splunkIDDict
    if serverid == serverIDDict['Ishana']:
        loggingchannel = splunkIDDict['Ishana']
    elif serverid == serverIDDict['Eden']:
        loggingchannel = splunkIDDict['Eden']
    else:
        return None
    return loggingchannel
# Returns the message on the logging channel.
# Args: message - The message that was deleted.
@client.event
async def on_message_delete(message):
    loggingchannel = getLoggingChannel(message.guild.id)
    if message.channel.id in ignoredchannels or message.channel.name.startswith('mpa') or message.guild.id in ignoredservers:
        return
    elif (message.author.bot):
        return
    elif message.channel.id in ignoredchannels and message.content.startswith('%'):
        return
    else:
        currentTime = time.strftime('%H:%M:%S')
        em = discord.Embed(colour=0xFF0000)
        if len(message.attachments) > 0:
            if message.attachments[0] != None:
                imageurl = message.attachments[0].url
                if message.content != '':
                    em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
                em.set_image(url=imageurl)
                await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + f'**{message.author.name}**\'s message was deleted from ' + f'{message.channel.mention}' + ':', embed=em)
        else:
            em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
            await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + f'**{message.author.name}**\'s message was deleted from ' + f'{message.channel.mention}' + ':', embed=em)
# Called when a member edits their message.
# Args:
# before - the message before it was edited
# after - the message after it was edited.
@client.event   
async def on_message_edit(before, after):
    loggingchannel = getLoggingChannel(before.guild.id)
    if before.channel.id in ignoredchannels or before.channel.name.startswith('mpa'):
        return
    elif (before.content == after.content):
        return
    elif (before.author.bot):
        return
    elif before.guild.id in ignoredservers:
        return
    else:
        currentTime = time.strftime('%H:%M:%S')
        em = discord.Embed(colour=0xFFFF00)
        em.add_field(name='From', value=before.clean_content, inline=False)
        em.add_field(name='To', value=after.clean_content, inline=False)
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :warning: ' + f'**{before.author.name}** edited a message in ' + f'{before.channel.mention}' + ':', embed=em)
# Calls upon a member join.
# args: member - the member that joined the server.
@client.event
async def on_member_join(member):
    loggingchannel = getLoggingChannel(member.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    if member.guild.id in ignoredservers:
        return
    await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :inbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ str(member.id) + ') has joined the server.')
# Calls when a member leaves a server or is kicked/banned from the server.
# args: member - the member that left the server
@client.event
async def on_member_remove(member):
    global banned
    # Banning members already writes an event to the log. This will disable this event to prevent duplicate events logged.
    if banned:
        banned = False
        return
    loggingchannel = getLoggingChannel(member.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    # If someone kicked the user, report who kicked the user and the reason for it if applicable
    async for entry in member.guild.audit_logs(limit=1,action=discord.AuditLogAction.kick, after=datetime.now()):
        logActionDate = entry.created_at
        timeNow = datetime.utcnow()
        formatLog = logActionDate.strftime('%Y-%m-%d %H:%M:%S')
        formatNow = timeNow.strftime('%Y-%m-%d %H:%M:%S')
        if formatLog != formatNow:
            break
        else:
            await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :boot: ' + f'**{entry.user}** has kicked **{entry.target}** (ID: {member.id})\n**Reason**: {entry.reason}')
            return
    if member.guild.id in ignoredservers:
        return
    await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :outbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ str(member.id) + ') has left or been removed from the server.' + '\nJoined at: ' + str(member.joined_at) + '\nAvatar: ' + member.avatar_url)
# Calls when a member updates certain information about themselves.
@client.event
async def on_member_update(before, after):
    global serverIDDict
    loggingchannel = getLoggingChannel(before.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    # Calls when a member gains administrator permissions and logs it. Contains who gave/removed the permissions.
    if before.guild.id == serverIDDict['Ishana']:
        if before.guild_permissions.administrator == False and after.guild_permissions.administrator == True:
            loggingchannel = getSplunkChannel(before.guild.id)
            differenceRole = 'None'
            for role in after.roles:
                if role not in before.roles and role in after.roles:
                    differenceRole = role.name + f' (ID: {role.id})'
                    break
            async for entry in before.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_role_update, after=datetime.now()):
                await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'**{entry.user}** (ID: {str(entry.user.id)}) has added **Administrator** permissions to **{entry.target}**  (ID: {str(entry.target.id)})\nLast Role Updated: **{differenceRole}**')
                return
        elif str(after.guild_permissions.administrator) == 'False' and str(before.guild_permissions.administrator) == 'True':
            loggingchannel = getSplunkChannel(before.guild.id)
            differenceRole = 'None'
            for role in before.roles:
                if role not in after.roles and role in before.roles:
                    differenceRole = role.name + f' (ID: {role.id})'
                    break
            async for entry in before.guild.audit_logs(limit=1,action=discord.AuditLogAction.member_role_update, after=datetime.now()):
                await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'**{entry.user}** (ID: {str(entry.user.id)}) has removed **Administrator** permissions from **{entry.target}**  (ID: {str(entry.target.id)})\nLast Role Updated: **{differenceRole}**')
                return
    # Calls when a member in the Eden server plays a game or not, then adds a role to them corresponding to certain games.
    # Removes the role when they either change games or stop playing completely.
    if before.guild.id == serverIDDict['Eden']:
        async def addRole():
            gameRoleID = getGameRole(after.activity.name)
            if gameRoleID is None:
                pass
            else:
                gameRole = discord.utils.get(client.get_guild(after.guild.id).roles, id=gameRoleID)
                # Don't add the role in if its already present.
                if gameRole in after.roles:
                    return
                print (f'Gave {gameRole.name} to {after.name}')
                await after.add_roles(gameRole)
                return
        async def removeRole():
            gameRoleID = getGameRole(before.activity.name)
            if gameRoleID is None:
                pass
            else:
                gameRole = discord.utils.get(client.get_guild(after.guild.id).roles, id=gameRoleID)
                print (f'Removed {gameRole.name} from {after.name}')
                await after.remove_roles(gameRole)
                return
        if (before.activity is None and after.activity is not None) or (before.activity is not None and after.activity is not None):
            await addRole()
            if before.activity is not None and after.activity is not None:
                if before.activity.name != after.activity.name:
                    await removeRole()
                    return
                else:
                    return
            else:
                return
        if (before.activity is not None and after.activity is None) or (before.activity is not None and after.activity is not None):
            await removeRole()
            return
    if before.nick == after.nick:
        return
    # Otherwise, it's a nickname change. Logs that.
    else:
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :writing_hand: ' + f'**{before.name}**' + f' has changed nicknames from **{before.nick}**' + f' to **{after.nick}**')
# Calls when a member gets banned. Passes a flag to not trigger the on_member_remove function.
@client.event
async def on_member_ban(guild, member):
    global banned
    loggingchannel = getLoggingChannel(guild.id)
    currentTime = time.strftime('%H:%M:%S')
    await asyncio.sleep(1)
    # Uses the Discord Audit log to find out who banned the user and the reason if any was given.
    async for entry in guild.audit_logs(limit=1,action=discord.AuditLogAction.ban, after=datetime.now()):
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :hammer: ' + f'**{entry.user}** has banned **{entry.target}** (ID: {member.id})\n**Reason**: {entry.reason}')
        banned = True
        break
    if member.guild.id in ignoredservers:
        return
# Calls when a member gets their ban revoked.
# Planned: use audit logs to find who performed the unban.
@client.event
async def on_member_unban(guild, user):
    loggingchannel = getLoggingChannel(guild.id)
    currentTime = time.strftime('%H:%M:%S')
    if guild.id in ignoredservers:
        return
    async for entry in guild.audit_logs(limit=1,action=discord.AuditLogAction.unban, after=datetime.now()):
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :o: ' + f'**{entry.user}** has unbanned **{entry.target}** (ID: {user.id}) from the server.')
        return
# Tunk commands, usually for shutdown or debugging.
@client.event
async def on_message(message):
    global gameRoleJson
    loggingchannel = getLoggingChannel(message.guild.id)
    if message.channel.id == 309640943341142016:
        currentTime = time.strftime('%H:%M:%S')
        user = message.author
        for index in range(len(message.author.roles)):
            if message.author.roles[index].id == 254207687242285066:
                return
            else:
                if message.author.roles[index].id == 191162764033523712:
                    await message.guild.get_member(message.author.id).remove_roles((message.author.roles[index]))
                inactiveRole = discord.utils.get(message.server.roles, id=254207687242285066)
                if inactiveRole.id != 254207687242285066:
                    await client.get_channel(loggingchannel).send('*Looks like the inactive role on code is not the same as the actual inactive role. Not going to add inactive role to user...*')
                else:
                    await message.guild.get_member(message.author.id).add_roles((message.author, inactiveRole))
                await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :swimmer: ' + f'**{user.name}**' + '#' + user.discriminator + f' (ID: {user.id})' + f' has indicated that they went inactive. \n**Absence Message**: {message.clean_content}')
                return
    await client.process_commands(message)
@client.command(name='shutdown')
async def cmd_shutdown(ctx):
    """
    Usage: tunk.shutdown
    Shuts down the bot mercilessly. Can only be used by Tenj. Either way, it will probably come back up in a few seconds after shutdown...
    That is, IF it does...
    """
    print ('Reached here')
    if ctx.author.id == 153273725666590720:
        await ctx.send('Shutting down...')
        restartRole = discord.utils.get(client.get_guild(226835458552758275).roles, id=370339592055947266)
        await client.get_channel(322466466479734784).send(f'Tunk is {restartRole.mention}')
        await client.logout()
@client.command(name='addgamerole')
@commands.check(is_edenServer)
async def cmd_addgamerole(ctx, gameName, roleID):
    """
    Usage: tunk.addgamerole <game name> <roleID>
    Replace:
    <Game Name> - The game name you want to be tracked. Note that this is letter by letter, case sensitive, etc. Everything. even if one letter is missing a symbol or something it will not be tracked. To add a game that isn't one word (most of them), add quotes for the name. Like "FINAL FANTASY XIV: A REALM REBORN"
    <Role ID> - The ID of the role you want to associate with the game. The bot checks if the role ID is in the system, but not against the game role list. This allows you to associate one role with multiple games.
    However, a game name may not be used multiple times. Each game can only have one role associated with it.
    Example: tunk.addgamerole "MONSTER HUNTER: WORLD" 480600255012929536
    """
    if ctx.author.guild_permissions.administrator :
        if type(gameName) is not None and len(roleID) == 18 and roleID.isdigit():
            roleToBeDel = int(roleID)
            if gameName in gameRoleJson:
                await ctx.send('The game name is already in the list!')
                return
            foundRole = discord.utils.get(ctx.guild.roles, id=int(roleID))
            if foundRole is not None:
                pass
            else:
                await ctx.send('The role ID specified is not in the server role list!')
                return
            gameRoleJson[gameName] = roleToBeDel
            try:
                with open('gameRoles.json', 'w') as fp:
                    json.dump(gameRoleJson, fp)
                fp.close()
                loadGameRoles()
                await ctx.send(f'Game {gameName} added with role ID {str(roleID)}')
                return
            except Exception as e:
                print (e)
                await ctx.send('An internal error has occurred.\nError Code: HUNGRYHUNGRYHIPPOS')
                return
        else:
            await ctx.send('Invalid arguements provided.\nUsage: tunk.addgamerole <gamename> <roleid>')
            return
    else:
        await ctx.send('You do not have permissions to do this.')
        return
@client.command(name='removegamerole')
@commands.check(is_edenServer)
async def cmd_removegamerole(ctx, gameName):
    """
    Usage: tunk.removegamerole <game name>
    Replace <game name> with the name of the game you would like to disassociate. Use the listgameroles command to find that name out.
    Example: tunk.removegamerole "MONSTER HUNTER: WORLD"
    """
    if ctx.author.guild_permissions.administrator:
        if gameName in gameRoleJson:
            try:
                del gameRoleJson[gameName]
                with open('gameRoles.json', 'w') as fp:
                    json.dump(gameRoleJson, fp)
                fp.close()
                loadGameRoles()
                await ctx.send(f'Removed {gameName} from the role list.')
                return
            except Exception as e:
                print (e)
                await ctx.send('An internal error has occurred. No changes have been made.\nError Code: HUNTSKETCHUP')
                return
        else:
            await ctx.send('Could not find the specified game name in the list!')
            return
@client.command(name='listgameroles')
@commands.check(is_edenServer)
async def cmd_listgamerole(ctx):
    """
    Usage: tunk.listgameroles
    Shows the list of the registered game roles that Tunk will automatically give out to people.
    """
    if ctx.author.guild_permissions.administrator:
        roleList = ''
        for key, value in gameRoleJson.items():
            roleList += f'\n{key} (ID: {value})'
        em = discord.Embed(description=roleList, color=0x0099FF)
        em.set_author(name='List of games and their Role IDs')
        await ctx.send('',embed=em)
    else:
        await ctx.send('You lack permissions to do this command.')
@cmd_addgamerole.error
async def cmd_addgamerole_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('This command cannot be used in this server.')
@cmd_removegamerole.error
async def cmd_removegamerole_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('This command cannot be used in this server.')
@cmd_listgamerole.error
async def cmd_listgamerole_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('This command cannot be used in this server.')
# Calls when a server role gains the administrator permissions or has their administrator permissions removed.
@client.event
async def on_guild_role_update(before, after):
    global serverIDDict
    if before.guild.id == serverIDDict['Ishana']:
        currentTime = time.strftime('%H:%M:%S')
        if before.permissions.administrator == False and after.permissions.administrator == True:
            loggingchannel = getSplunkChannel(before.guild.id)
            async for entry in before.guild.audit_logs(limit=1,action=discord.AuditLogAction.role_update, after=datetime.now()):
                await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'**{entry.user}** (ID: {str(entry.user.id)}) has added **Administrator** permissions to the **{entry.target}** role.')
                break
        if before.permissions.administrator == True and after.permissions.administrator == False:
            loggingchannel = getSplunkChannel(before.guild.id)
            async for entry in before.guild.audit_logs(limit=1,action=discord.AuditLogAction.role_update, after=datetime.now()):
                await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'**{entry.user}** (ID: {str(entry.user.id)}) has removed **Administrator** permissions from the **{entry.target}** role.')
                break
# Startup tasks
@client.event
async def on_ready():
    connectedServers = 0
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print ('Logged in to servers:')
    for item in client.guilds:
        print (item)
        connectedServers += 1
    end = time.time()
    loadupTime = (end - start)
    print ('Tunk is now ready\nFinished loadup in ' + time.strftime('%H hours, %M minutes, %S seconds', time.gmtime(loadupTime)))
    print('------')
    game = discord.Game(name='always watching')
    await client.change_presence(activity=game, status=discord.Status.online)
    onlineRole = discord.utils.get(client.get_guild(226835458552758275).roles, id=370337403769978880)
    await client.get_channel(322466466479734784).send(f'Tunk is now {onlineRole.mention}' + '\nStartup time: ' + time.strftime('%H hours, %M minutes, %S seconds', time.gmtime(loadupTime)) + '\nConnected to **' + str(connectedServers) + '** servers' + '\nLast Restarted: ' + lastRestart)

@client.event
async def on_resumed():
    print ('Tunk has resumed from a disconnect.')
    resumeRole = discord.utils.get(client.get_guild(226835458552758275).roles, id=405620919541694464)
    await client.get_channel(322466466479734784).send(f'Tunk has {resumeRole.mention}')
   
client.run('')
