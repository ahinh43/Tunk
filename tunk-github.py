import discord
import os
import asyncio
import time

# A very simple logging bot written for Ishana to log and print edited and deleted messages in a specfic channel. For Ishana use only.


client = discord.Client()

@client.event
async def on_message_delete(message):
    if message.channel.id == '313703862798385162' or message.channel.id == '164755663464038400' or message.channel.name.startswith('mpa') or message.server.id == '226835458552758275':
        return
    elif (message.author.bot):
        return
    elif message.channel.id == '206673616060940288' and message.content.startswith('%'):
        return
    else:
        currentTime = time.strftime('%H:%M:%S')
        if len(message.attachments) > 0:
            if message.content == '' and message.attachments[0] != None:
                imageurl = message.attachments[0]['url']
                await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + str(imageurl))
            elif message.content != '' and message.attachments[0] != None:
                imageurl = message.attachments[0]['url']
                await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + message.clean_content + '\n' + str(imageurl))
        else:
            await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':' + '\n' + message.clean_content)
@client.event   
async def on_message_edit(before, after):
    if before.channel.id == '313703862798385162' or before.channel.id == '164755663464038400' or before.channel.name.startswith('mpa'):
        return
    elif (before.content == after.content):
        return
    elif (before.author.bot):
        return
    elif before.server.id == '226835458552758275':
        return
    else:
        currentTime = time.strftime('%H:%M:%S')
        await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :warning: ' + '**{}** edited a message in '.format(before.author.name) + '{}'.format(before.channel.mention) + ':' + '\n**From: **' + before.clean_content + '\n**To: **' + after.clean_content)
@client.event
async def on_member_join(member):
    currentTime = time.strftime('%H:%M:%S')
    if member.server.id == '226835458552758275':
        return
    await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :inbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ member.id + ') has joined the server.')
@client.event
async def on_member_remove(member):
    currentTime = time.strftime('%H:%M:%S')
    if member.server.id == '226835458552758275':
        return
    await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :outbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ member.id + ') has left or been removed from the server.' + '\nAvatar: ' + member.avatar_url)
@client.event
async def on_member_update(before, after):
    currentTime = time.strftime('%H:%M:%S')
    # if after.id == '153273725666590720' and after.server.id == '159184581830901761':
        # for index in range(len(after.roles)):
            # if after.roles[index].id == '357155081512026125':
                # await client.remove_roles(after, after.roles[index])
    if before.nick == after.nick:
        return
    elif before.server.id == '226835458552758275':
        return
    else:
        await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :writing_hand: ' + '**{}**'.format(before.name) + ' has changed nicknames from **{}**'.format(before.nick) + ' to **{}**'.format(after.nick))
@client.event
async def on_member_ban(member):
    currentTime = time.strftime('%H:%M:%S')
    if before.server.id == '226835458552758275':
        return
    await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :hammer: ' + '**{}**'.format(member.name) + '(ID: {})'.format(member.id) + ' has been banned from the server.')
@client.event
async def on_member_unban(server, user):
    currentTime = time.strftime('%H:%M:%S')
    if before.server.id == '226835458552758275':
        return
    await client.send_message(client.get_channel('313703862798385162'), '`[' + str(currentTime) + ']` :hammer: ' + '**{}**'.format(user.name) + '(ID: {})'.format(user.id) + ' has been unbanned from the server.')
@client.event
async def on_message(message):
    if message.content.startswith('tunk.'):
        if message.content.lower() == 'tunk.shutdown':
            if message.author.id == '153273725666590720':
                await client.send_message(message.channel, 'Shutting down...')
                await client.logout()
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
    
client.run('')

# Requires Python 3.5 to run. Written by Tenj