import discord
import os
import asyncio
import time

loggingchannels = []
ignoredchannels = []
ignoredservers = []

# A very simple logging bot written for Ishana to log and print edited and deleted messages in a specfic channel. For Ishana use only(?).
        
# Load Channels it will ignore
for line in open ("ignoredchannels.txt"):
    li = line.strip()
    if not li.startswith("#"):
        ignoredchannels.append(li)
# Load the servers that it will ignore
for line in open ("ignoredservers.txt"):
    li = line.strip()
    if not li.startswith("#"):
        ignoredservers.append(li)

client = discord.Client()

@client.event
async def on_message_delete(message):
    # global loggingchannels
    # global ignoredchannels
    # global ignoredservers
    if message.server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif message.server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    if message.channel.id in ignoredchannels or message.channel.name.startswith('mpa') or message.server.id in ignoredservers:
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
                # await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':', embed=em)
               #await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + str(imageurl))
            if message.attachments[0] != None:
                imageurl = message.attachments[0]['url']
                if message.content != '':
                    em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
                em.set_image(url=imageurl)
                await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':', embed=em)
                #await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + message.clean_content + '\n' + str(imageurl))
        else:
            em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
            await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':', embed=em)
            #await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + message.clean_content)
@client.event   
async def on_message_edit(before, after):
    if before.server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif before.server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    if before.channel.id in ignoredchannels or before.channel.name.startswith('mpa'):
        return
    elif (before.content == after.content):
        return
    elif (before.author.bot):
        return
    elif before.server.id in ignoredservers:
        return
    else:
        currentTime = time.strftime('%H:%M:%S')
        em = discord.Embed(colour=0xFFFF00)
        em.add_field(name='From', value=before.clean_content, inline=False)
        em.add_field(name='To', value=after.clean_content, inline=False)
        await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :warning: ' + '**{}** edited a message in '.format(before.author.name) + '{}'.format(before.channel.mention) + ':', embed=em)
       # await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :warning: ' + '**{}** edited a message in '.format(before.author.name) + '{}'.format(before.channel.mention) + ':' + '\n```fix\nFrom:\n```\n' + before.clean_content + '\n```fix\nTo:\n```\n' + after.clean_content)
@client.event
async def on_member_join(member):
    if member.server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif member.server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    currentTime = time.strftime('%H:%M:%S')
    if member.server.id in ignoredservers:
        return
    await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :inbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ member.id + ') has joined the server.')
@client.event
async def on_member_remove(member):
    if member.server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif member.server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    currentTime = time.strftime('%H:%M:%S')
    if member.server.id in ignoredservers:
        return
    await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :outbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ member.id + ') has left or been removed from the server.' + '\nJoined at: ' + str(member.joined_at) + '\nAvatar: ' + member.avatar_url)
@client.event
async def on_member_update(before, after):
    if before.server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif before.server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    currentTime = time.strftime('%H:%M:%S')
    # if after.id == '153273725666590720' and after.server.id == '159184581830901761':
        # for index in range(len(after.roles)):
            # if after.roles[index].id == '357155081512026125':
                # await client.remove_roles(after, after.roles[index])
    if before.nick == after.nick:
        return
    elif before.server.id in ignoredservers:
        return
    else:
        await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :writing_hand: ' + '**{}**'.format(before.name) + ' has changed nicknames from **{}**'.format(before.nick) + ' to **{}**'.format(after.nick))
@client.event
async def on_member_ban(member):
    if member.server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif member.server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    currentTime = time.strftime('%H:%M:%S')
    if member.server.id in ignoredservers:
        return
    await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :hammer: ' + '**{}**'.format(member.name) + '(ID: {})'.format(member.id) + ' has been banned from the server.')
@client.event
async def on_member_unban(server, user):
    if server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    currentTime = time.strftime('%H:%M:%S')
    if server.id in ignoredservers:
        return
    await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :hammer: ' + '**{}**'.format(user.name) + '(ID: {})'.format(user.id) + ' has been unbanned from the server.')
@client.event
async def on_message(message):
    if message.server.id == '159184581830901761':
        loggingchannel = '313703862798385162'
    elif message.server.id == '82999036361048064':
        loggingchannel = '429425336204394506'
    else:
        return
    if message.content.startswith('tunk.'):
        if message.content.lower() == 'tunk.shutdown':
            if message.author.id == '153273725666590720':
                await client.send_message(message.channel, 'Shutting down...')
                await client.logout()
    elif message.channel.id == '309640943341142016':
        currentTime = time.strftime('%H:%M:%S')
        user = message.author
        for index in range(len(message.author.roles)):
            if message.author.roles[index].id == '254207687242285066':
                return
            else:
                if message.author.roles[index].id == '191162764033523712':
                    await client.remove_roles(message.author, message.author.roles[index])
                inactiveRole = discord.utils.get(message.server.roles, id='254207687242285066')
                if inactiveRole.id != '254207687242285066':
                    await client.send_message(client.get_channel(loggingchannel), '*Looks like the inactive role on code is not the same as the actual inactive role. Not going to add inactive role to user...*')
                else:
                    await client.add_roles(message.author, inactiveRole)
                await client.send_message(client.get_channel(loggingchannel), '`[' + str(currentTime) + ']` :swimmer: ' + '**{}**'.format(user.name)+ '#' + user.discriminator + ' (ID: {})'.format(user.id) + ' has indicated that they went inactive. \n**Absence Message**: {}'.format(message.clean_content))
                return
@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('Logged into servers:')
    for item in client.servers:
        print (item)
    print ('Tunk is now ready')
    print('------')
    await client.change_presence(game=discord.Game(name='always watching'))
    
@client.event
async def on_resumed():
    connectedServers = 0
    print ('Tunk has resumed from a disconnect.')
    for item in client.servers:
        connectedServers += 1
    resumeRole = discord.utils.get(client.get_server('226835458552758275').roles, id='405620919541694464')
    await client.send_message(client.get_channel('322466466479734784'), 'Tunk has {}'.format(resumeRole.mention))
   
def run():
    client.run('MzE0NjU2MjA3NjM1NzQyNzIx.C_-UNA.ktJh8Ty-3kD4O2HM6qbIfcOBo30')

# Requires Python 3.5 to run. Written by Tenj