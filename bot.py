import discord
import env


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents, proxy=env.get('https_proxy'))


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    # ignore when it's from us
    if message.author == client.user:
        return
    # only watch the quiz channel
    if message.channel.name != 'quiz':
        return
    await message.channel.send('I saw that!')


client.run(env.get('DISCORD_TOKEN'))
