import discord
import env
import pogoapi
import quiz_items
import random
import sys


from type import Type


from discord.ext import commands


command_prefix = '/'


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
        command_prefix=command_prefix,
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

    # handle commands
    if message.content.startswith(command_prefix):
        await bot.process_commands(message)
        return

    # only watch the quiz channel
    if message.channel.name != 'quiz':
        return

    # check answer if quiz is ongoing
    if quiz_item:
        await message.channel.send(quiz_item.answer(message.content))

    # start new item
    quiz_item = random.choice(quiz_items.get_all_quiz_item_classes())()
    await message.channel.send(quiz_item.ask_question())


@bot.command()
async def exit(ctx):
    await ctx.send('Goodbye.')
    sys.exit()


@bot.command()
async def type(ctx, arg):
    arg = arg.capitalize()

    if arg not in pogoapi.get_type_effectiveness().keys():
        await ctx.send(f'I don\'t know {arg}')
        return

    type = Type(arg)
    for effect in ('super effective', 'not very effective', 'ineffective'):
        types = getattr(type, effect.replace(' ', '_'))()
        if types:
            types = ', '.join(map(str, types))
            await ctx.send(f'{arg} is {effect} against {types}')


bot.run(env.get('DISCORD_TOKEN'))
