import sys

import discord
from discord.ext import commands

import env
import pogoapi
from player import get_all_player_stats, get_current_player_stats
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

    # only watch the quiz channel
    if message.channel.name != "quiz":
        return

    # check answer if quiz is ongoing
    if quiz:
        await message.channel.send(
            quiz.answer(message.author, message.content)
        )
        if quiz.has_remaining_questions():
            await message.channel.send(quiz.ask_question())
        else:
            await message.channel.send(quiz.show_score())
            quiz = None
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
        f"{weather=}"
    )
    quiz = Quiz(
        questions=questions,
        super_eff=super_eff,
        not_very_eff=not_very_eff,
        weather=bool(weather),
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
        await ctx.send(get_current_player_stats(ctx.author))


bot.run(env.get("DISCORD_TOKEN"))
