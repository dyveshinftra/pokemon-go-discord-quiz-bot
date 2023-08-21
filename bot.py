import discord
import env
import super_effective_attacker


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents, proxy=env.get('https_proxy'))


# current quiz item
item = None


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global item

    # ignore when it's from us
    if message.author == client.user:
        return
    # only watch the quiz channel
    if message.channel.name != 'quiz':
        return

    # check answer if quiz is ongoing
    if item:
        if item.is_answer_correct(message.content):
            await message.channel.send('That is correct!')
        else:
            await message.channel.send(item.correct_answer())

    # start new item
    item = super_effective_attacker.SuperEffectiveAttacker()
    await message.channel.send(item.question())


client.run(env.get('DISCORD_TOKEN'))
