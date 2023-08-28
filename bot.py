import discord
import env
import quiz_items
import random


intents = discord.Intents.default()
intents.message_content = True


client = discord.Client(intents=intents, proxy=env.get('https_proxy'))


# current quiz item
quiz_item = None


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    global quiz_item

    # ignore when it's from us
    if message.author == client.user:
        return
    # only watch the quiz channel
    if message.channel.name != 'quiz':
        return

    # check answer if quiz is ongoing
    if quiz_item:
        message.channel.send(quiz_item.answer(message.content))

    # start new item
    quiz_item = random.choice(quiz_items.get_all_quiz_item_classes())()
    await message.channel.send(quiz_item.ask_question())


client.run(env.get('DISCORD_TOKEN'))
