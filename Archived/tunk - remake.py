import discord
import os
import asyncio
import time
import datetime
import sys
from datetime import datetime,tzinfo,timedelta

loggingchannels = []
ignoredchannels = []
ignoredservers = []

# A very simple logging bot written for Ishana to log and print edited and deleted messages in a specfic channel. For Ishana use only(?).
        
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

serverIDDict =  {
"Ishana": 159184581830901761,
"Eden": 82999036361048064
}
channelIDDict = {
"Ishana": 313703862798385162,
"Eden": 429425336204394506,
"IshanaSplunk": 477335474525175830
}

start = time.time()
lastRestart = str(datetime.now())
banned = False
client = discord.Client()

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
            # if message.content == '' and message.attachments[0] != None:
                # imageurl = message.attachments[0]['url']
                # em.set_image(url=imageurl)
                # await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':', embed=em)
               #await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + str(imageurl))
            if message.attachments[0] != None:
                imageurl = message.attachments[0]['url']
                if message.content != '':
                    em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
                em.set_image(url=imageurl)
                await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + f'**{message.author.name}**\'s message was deleted from ' + f'{message.channel.mention}' + ':', embed=em)
                #await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + message.clean_content + '\n' + str(imageurl))
        else:
            em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
            await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':', embed=em)
            #await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + message.clean_content)
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
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :warning: ' + '**{}** edited a message in '.format(before.author.name) + '{}'.format(before.channel.mention) + ':', embed=em)
       # await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :warning: ' + '**{}** edited a message in '.format(before.author.name) + '{}'.format(before.channel.mention) + ':' + '\n```fix\nFrom:\n```\n' + before.clean_content + '\n```fix\nTo:\n```\n' + after.clean_content)
@client.event
async def on_member_join(member):
    loggingchannel = getLoggingChannel(member.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    if member.guild.id in ignoredservers:
        return
    await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :inbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ str(member.id) + ') has joined the server.')
@client.event
async def on_member_remove(member):
    global banned
    if banned:
        banned = False
        return
    loggingchannel = getLoggingChannel(member.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    async for entry in member.guild.audit_logs(limit=1,action=discord.AuditLogAction.kick, after=datetime.now()):
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :boot: ' + f'**{entry.user}** has kicked **{entry.target}** (ID: {member.id})\n**Reason**: {entry.reason}')
        return
    else:
        return
    if member.guild.id in ignoredservers:
        return
    await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :outbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ str(member.id) + ') has left or been removed from the server.' + '\nJoined at: ' + str(member.joined_at) + '\nAvatar: ' + member.avatar_url)
@client.event
async def on_member_update(before, after):
    global serverIDDict
    loggingchannel = getLoggingChannel(before.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    if before.guild.id == serverIDDict['Ishana']:
        if before.guild_permissions.administrator == False and after.guild_permissions.administrator == True:
            loggingchannel = 477335474525175830
            differenceRole = 'None'
            for role in after.roles:
                if role not in before.roles and role in after.roles:
                    differenceRole = role.name + f' (ID: {role.id})'
                    break
            await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'{after.name} has been granted **Administrator** powers.\nLast role changed: {differenceRole}')
        elif str(after.guild_permissions.administrator) == 'False' and str(before.guild_permissions.administrator) == 'True':
            loggingchannel = 477335474525175830
            differenceRole = 'None'
            for role in before.roles:
                if role not in after.roles and role in before.roles:
                    differenceRole = role.name + f' (ID: {role.id})'
                    break
            await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'{after.name} has had their **Administrator** powers removed.\nLast role changed: {differenceRole}')
    if before.nick == after.nick:
        return
    else:
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :writing_hand: ' + f'**{before.name}**' + f' has changed nicknames from **{before.nick}**' + f' to **{after.nick}**')
@client.event
async def on_member_ban(guild, member):
    global banned
    loggingchannel = getLoggingChannel(guild.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    await asyncio.sleep(1)
    async for entry in member.guild.audit_logs(limit=1,action=discord.AuditLogAction.ban, after=datetime.now()):
        await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :hammer: ' + f'**{entry.user}** has banned **{entry.target}** (ID: {member.id})\n**Reason**: {entry.reason}')
        banned = True
    if member.guild.id in ignoredservers:
        return
    #await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :hammer: ' + f'**{member.name}**' + f'(ID: {member.id})' + ' has been banned from the server.')
@client.event
async def on_member_unban(guild, user):
    loggingchannel = getLoggingChannel(guild.guild.id)
    currentTime = time.strftime('%H:%M:%S')
    if guild.id in ignoredservers:
        return
    await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :hammer: ' + f'**{user.name}**' + f'(ID: {user.id})' + ' has been unbanned from the server.')
@client.event
async def on_message(message):
    loggingchannel = getLoggingChannel(message.guild.id)
    if message.content.startswith('tunk.'):
        if message.content.lower() == 'tunk.shutdown':
            if message.author.id == 153273725666590720:
                await message.channel.send('Shutting down...')
                await client.logout()
    elif message.channel.id == 309640943341142016:
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
@client.event
async def on_server_role_update(before, after):
    global serverIDDict
    if before.guild.id == serverIDDict['Ishana']:
        currentTime = time.strftime('%H:%M:%S')
        if before.permissions.administrator == False and after.permissions.administrator == True:
            loggingchannel = 477335474525175830
            await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'The role **{after.name}** has the **Administrator** permission added.')
        if before.permissions.administrator == True and after.permissions.administrator == False:
            loggingchannel = 477335474525175830
            await client.get_channel(loggingchannel).send('`[' + str(currentTime) + ']` :exclamation: ' + f'The role **{after.name}** has the **Administrator** permission removed.')
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
   
client.run('NDc3NTQzNjA3MDI5NTk2MjIx.DlKWTA.DKvGwURIwQjd9S0omcquImIJrf4')

# Requires Python 3.6 to run. Written by Tenj