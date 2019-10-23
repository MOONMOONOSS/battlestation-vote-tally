# -*- coding: utf-8 -*-

# Copyright (C) 2019 Moonmoon

import discord

from config import bot_config

sayo = None

class Sayo(object):
    client = discord.Client()

    def __init__(self):
        self.end_bot = False

        self.starts_with = bot_config['discord'].get('command', '$')

        self.commands = {
            self.starts_with + "count": self.count_votes,
            self.starts_with + "die": self.die
        }

    ### Client Events
    @client.event
    async def on_message(message):

        # we do not want the bot to reply to itself
        if message.author == Sayo.client.user or message.author.bot:
            return

        if message.content.startswith(sayo.starts_with):

            if message.author.id not in bot_config['discord'].get('user_ids', list()):
                await sayo.send_message(message.channel, "Sorry you're not authorized to use this bot.")
                return
            
            command = message.content
            params = list()

            if ' ' in message.content:
                command, params = (message.content.split()[0], message.content.split()[1:])

            command = command.lower()
            
            if command in sayo.commands:
                await sayo.commands[command](command, params, message)

    @client.event
    async def on_ready():
        print('Logged in as')
        print(Sayo.client.user.name)
        print(Sayo.client.user.id)
        print('------')

    ### RUN IT!
    def run(self):
        TOKEN = bot_config.get('bot_token')
        if not TOKEN:
            print("The provided token is either invalid or unspecified: ", TOKEN)
            return
        self.client.run(TOKEN)

    ### Helpers
    async def send_message(self, channel, message):
        await channel.send(message)

    async def send_embed_message(self, channel, message="", title="", colour=discord.Colour.dark_green(), fields=[], image=None):
        embed = discord.Embed(
            title=title,
            type="rich",
            colour=colour
        )
        for field in fields:
            embed.add_field(name=field['name'],
                            value=field['value'],
                            inline=field['inline'])

        if image:
            embed.set_image(url=image)
            
        await channel.send(content=message, embed=embed)

    ### Commands
    async def count_votes(self, command, params, message):

        voting_channel_id = bot_config.get("discord").get('voting_channel_id', None)
        results_channel_id = bot_config.get("discord").get('results_channel_id', None)

        if not voting_channel_id:
            await sayo.send_message(message.channel, "Voting channel ID was not properly configured. Aborting command.")
            return

        if not results_channel_id:
            await sayo.send_message(message.channel, "Results channel ID was not properly configured. Aborting command.")
            return

        voting_channel = sayo.client.get_channel(voting_channel_id)

        messages = await voting_channel.history(limit=100).flatten()
        messages = sorted(messages, key=lambda msg: sum([react.count for react in msg.reactions]), reverse=True)
        if len(messages) > 8: messages = messages[:8]

        results_channel = sayo.client.get_channel(results_channel_id)

        async with results_channel.typing():
            for msg in messages:
                if not msg.clean_content.startswith("https"):
                    # messages that are not links are not submissions, so skip
                    continue

                fields = [
                    {
                        'name': "Message Link",
                        'value': msg.jump_url,
                        'inline': False
                    },
                    {
                        'name': 'Vote Count',
                        'value': sum([react.count for react in msg.reactions]),
                        'inline': False
                    }
                ]

                await sayo.send_embed_message(results_channel, fields=fields, image=msg.clean_content)
            

    async def die(self, command, params, message):
        msg = 'Shutting down...'
        sayo.end_bot = True
        await sayo.send_message(message.channel, msg)
        await sayo.client.close()

if __name__ == '__main__':
    sayo = Sayo()
    sayo.run()
