import sys

import discord
from discord.ext import commands

import env
import pogoapi
from player import (
    get_all_player_detail,
    get_all_player_stats,
    get_current_player_detail,
    get_current_player_stats,
)
from quiz import Quiz
from type import Type

command_prefix = "/"


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(
    command_prefix=command_prefix,
    intents=intents,
    proxy=env.get("https_proxy"),
)


# current quiz
quiz = None


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message):
    global quiz
    # ignore when it's from us
    if message.author == bot.user:
        return

    # handle commands
    if message.content.startswith(command_prefix):
        await bot.process_commands(message)
        return

    # handle commands
    if message.content.startswith("sam"):
        author = "sam"
    else:
        author = str(message.author)

    # only watch the quiz channel
    if message.channel.name != "quiz":
        return

    # check answer if quiz is ongoing
    if quiz and not quiz.is_finished:
        await message.channel.send(quiz.answer(author, message.content))
    else:
        await message.channel.send(
            "No quiz in progress, start a new quiz by using /start"
        )


@bot.command()
async def exit(ctx):
    await ctx.send("Goodbye.")
    sys.exit()


@bot.command()
async def start(
    ctx,
    questions: int = 5,
    super_eff: int = 1,
    not_very_eff: int = 0,
    weather: int = 0,
):
    global quiz
    await ctx.send(
        f"Starting quiz. {questions=} {super_eff=} {not_very_eff=} "
        f"{weather=}\n Other players can join by using /join"
    )
    quiz = Quiz(
        questions=questions,
        super_eff=super_eff,
        not_very_eff=not_very_eff,
        weather=bool(weather),
        player_name=str(ctx.author),
    )
    await ctx.send(quiz.ask_question())


@bot.command()
async def type(ctx, arg):
    arg = arg.capitalize()

    if arg not in pogoapi.get_type_effectiveness().keys():
        await ctx.send(f"I don't know {arg}")
        return

    type = Type(arg)
    for effect in ("super effective", "not very effective", "ineffective"):
        types = getattr(type, effect.replace(" ", "_"))()
        if types:
            types = ", ".join(map(str, types))
            await ctx.send(f"{arg} is {effect} against {types}")


@bot.command()
async def stats(
    ctx,
    everyone: int = 1,
):
    if everyone:
        await ctx.send(get_all_player_stats())
    else:
        await ctx.send(get_current_player_stats(str(ctx.author)))


@bot.command()
async def detail(
    ctx,
    everyone: int = 0,
):
    if everyone:
        await ctx.send(get_all_player_detail())
    else:
        await ctx.send(get_current_player_detail(str(ctx.author)))


@bot.command()
async def join(ctx, author=None):
    global quiz
    if quiz and not quiz.is_finished:
        quiz.join(author or str(ctx.author))
        await ctx.send("You join the current quiz")
    else:
        await ctx.send("No quiz in progress, use /start to start a quiz")


bot.run(env.get("DISCORD_TOKEN"))
