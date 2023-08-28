import discord
import env
import quiz_items
import random


from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
        command_prefix='?',
        intents=intents,
        proxy=env.get('https_proxy'))


# current quiz item
quiz_item = None


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
    global quiz_item

    # ignore when it's from us
    if message.author == bot.user:
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


bot.run(env.get('DISCORD_TOKEN'))
