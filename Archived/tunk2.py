import discord
import os
import asyncio
import time

loggingchannels = []
ignoredchannels = []
ignoredguilds = []

# A very simple logging bot written for Ishana to log and print edited and deleted messages in a specfic channel. For Ishana use only(?).
        
# Load Channels it will ignore
for line in open ("ignoredchannels.txt"):
    li = line.strip()
    if not li.startswith("#"):
        ignoredchannels.append(li)
# Load the guilds that it will ignore
for line in open ("ignoredservers.txt"):
    li = line.strip()
    if not li.startswith("#"):
        ignoredguilds.append(li)

class Tunk(discord.Client):
    async def on_message_delete(self, message):
        # global loggingchannels
        # global ignoredchannels
        # global ignoredguilds
        if message.guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif message.guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        if message.channel.id in ignoredchannels or message.channel.name.startswith('mpa') or message.guild.id in ignoredguilds:
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
                    imageurl = message.attachments[0]['url']
                    if message.content != '':
                        em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
                    em.set_image(url=imageurl)
                    await loggingchannel.send('`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':', embed=em)
            else:
                em.add_field(name='Deleted Message', value=message.clean_content, inline=False)
                await loggingchannel.send('`[' + str(currentTime) + ']` :x: ' + '**{}**\'s message was deleted from '.format(message.author.name) + '{}'.format(message.channel.mention) + ':', embed=em)
    async def on_message_edit(self, before, after):
        if before.guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif before.guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        if before.channel.id in ignoredchannels or before.channel.name.startswith('mpa'):
            return
        elif (before.content == after.content):
            return
        elif (before.author.bot):
            return
        elif before.guild.id in ignoredguilds:
            return
        else:
            currentTime = time.strftime('%H:%M:%S')
            em = discord.Embed(colour=0xFFFF00)
            em.add_field(name='From', value=before.clean_content, inline=False)
            em.add_field(name='To', value=after.clean_content, inline=False)
            await loggingchannel.send('`[' + str(currentTime) + ']` :warning: ' + '**{}** edited a message in '.format(before.author.name) + '{}'.format(before.channel.mention) + ':', embed=em)
    async def on_member_join(self, member):
        if member.guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif member.guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        currentTime = time.strftime('%H:%M:%S')
        if member.guild.id in ignoredguilds:
            return
        await loggingchannel.send('`[' + str(currentTime) + ']` :inbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ str(member.id) + ') has joined the guild.')
    async def on_member_remove(self, member):
        if member.guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif member.guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        currentTime = time.strftime('%H:%M:%S')
        if member.guild.id in ignoredguilds:
            return
        await loggingchannel.send('`[' + str(currentTime) + ']` :outbox_tray: ' + '**' + member.name + '#' + member.discriminator + '** (ID: '+ str(member.id) + ') has left or been removed from the guild.' + '\nAvatar: ' + member.avatar_url)
    async def on_member_update(self, before, after):
        if before.guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif before.guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        currentTime = time.strftime('%H:%M:%S')
        if before.nick == after.nick:
            return
        elif before.guild.id in ignoredguilds:
            return
        else:
            await loggingchannel.send('`[' + str(currentTime) + ']` :writing_hand: ' + '**{}**'.format(before.name) + ' has changed nicknames from **{}**'.format(before.nick) + ' to **{}**'.format(after.nick))
    async def on_member_ban(self, member):
        if member.guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif member.guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        currentTime = time.strftime('%H:%M:%S')
        if member.guild.id in ignoredguilds:
            return
    async def on_member_unban(self, guild, user):
        if guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        currentTime = time.strftime('%H:%M:%S')
        if guild.id in ignoredguilds:
            return
        await loggingchannel.send('`[' + str(currentTime) + ']` :hammer: ' + '**{}**'.format(user.name) + '(ID: {})'.format(user.id) + ' has been unbanned from the guild.')
    async def on_message(self, message):
        if message.guild.id == 159184581830901761:
            loggingchannel = 313703862798385162
        elif message.guild.id == 429434290443517963:
            loggingchannel = self.get_channel(429434343107067904)
        else:
            return
        if message.content.startswith('tunk.'):
            if message.content.lower() == 'tunk.shutdown':
                if message.author.id == 153273725666590720:
                    await message.channel.send('Shutting down...')
                    await self.logout()
        elif message.channel.id == 309640943341142016:
            currentTime = time.strftime('%H:%M:%S')
            user = message.author
            for index in range(len(message.author.roles)):
                if message.author.roles[index].id == '254207687242285066':
                    return
                else:
                    if message.author.roles[index].id == '191162764033523712':
                        await member.remove_roles(message.author, message.author.roles[index])
                    inactiveRole = discord.utils.get(message.guild.roles, id='254207687242285066')
                    if inactiveRole.id != '254207687242285066':
                        await loggingchannel.send('*Looks like the inactive role on code is not the same as the actual inactive role. Not going to add inactive role to user...*')
                    else:
                        await member.add_roles(message.author, inactiveRole)
                    await loggingchannel.send('`[' + str(currentTime) + ']` :swimmer: ' + '**{}**'.format(user.name)+ '#' + user.discriminator + ' (ID: {})'.format(user.id) + ' has indicated that they went inactive. \n**Absence Message**: {}'.format(message.clean_content))
                    return
    async def on_ready(self):
        print('Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('Logged into guilds:')
        for item in self.guilds:
            print (item)
        print ('Tunk is now ready')
        print('------')
        game = discord.Game("always watching")
        await self.change_presence(activity=game)
        
    async def on_resumed(self):
        connectedServers = 0
        print ('Tunk has resumed from a disconnect.')
        for item in self.guilds:
            connectedServers += 1
        await client.send_message(client.get_channel('322466466479734784'), 'Tunk has {}'.format(client.get_guild('226835458552758275').roles[29].mention))
client = Tunk()      
client.run('MzU5MTcwMzg4OTg4NTI2NTky.DaBLSw.kmmYv7V69cvFq6r0CuEjwBhUS5s')

# Requires Python 3.5 to run. Written by Tenj