from __future__ import annotations

import traceback
from datetime import datetime, time, timedelta
from random import choice, shuffle

from discord import Activity, ActivityType, Embed, Intents, Interaction
from discord.ext.commands import Bot

from .config import Config
from .database import Database
from .log import log


bot = Bot(
    command_prefix="/",
    intents=Intents.all(),
    owner_id=Config["owner_id"]
)

lunch_times = (
    (time(hour=12, minute=12), time(hour=18, minute=36)), # Monday
    (time(hour=12, minute=30), time(hour=19, minute=12)),
    (time(hour=12, minute=3 ), time(hour=19, minute=6 )), # ...
    (time(hour=11, minute=18), time(hour=19, minute=4 )),
    (time(hour=12, minute=12), time(hour=18, minute=25))  # Friday
)

night_time = (
    time(hour=23, minute=00),
    time(hour=6, minute=00),
)

lunch_sentences = (
    "Le prochain repas est à <t:{ts}:t> (<t:{ts}:R>).",
    "Tu pourras te rassasier <t:{ts}:R> (à <t:{ts}:t>).",
    "Ton estomac pourra se remplir <t:{ts}:R> (à <t:{ts}:t>)."
)

night_sentences = (
    "Si tu as si faim, ouvre ton frigo et arrète de spam.",
    "Gros morfal, attend encore quelques heures !",
    "A cette heure là ? Il serait temps d'aller dormir."
)

# events
@bot.event
async def on_ready():    
    # sync slash commands
    await bot.tree.sync()
    
    # change activity
    await bot.change_presence(activity=Activity(
        type=ActivityType.watching,
        name=Config["activity"]
    ))
    
    log.info("DATA :")
    s = Database.select("pairs")
    for pair in s:
        log.info(pair["from_id"], pair["to_id"])
    
    log.info("Bot ready !")
    
@bot.event
async def on_error(event, *args, **kwargs):
    log.error(traceback.format_exc())

@bot.tree.command(name="help", description="Affiche la liste des commandes")
async def help(interaction: Interaction):
        
    await interaction.response.send_message(embed=Embed(
        title="Liste des commandes",
        description= "\n".join([
            f"- {command.mention} : {command.description}" 
            for command in await bot.tree.fetch_commands()
            if command.id != 1025814910300594219
        ])
    ))

# Secret Santa
# @bot.tree.command(name="join", description="Participe au Secret Santa !")
# async def join(interaction: Interaction):
    
#     current_users = Database.select("users", ["user_id"])
#     for user in current_users:
#         if user["user_id"] == interaction.user.id:
#             await interaction.response.send_message("Tu participe déjà au Secret Santa", ephemeral=True)
#             return
    
#     Database.insert("users", {
#         "user_id": interaction.user.id,
#     })
#     await interaction.response.send_message("Ta participation a bien été prise en compte !", ephemeral=True)

# @bot.tree.command(name="leave", description="Supprime ta participation au Secret Santa")
# async def leave(interaction: Interaction):
#     current_users = Database.select("users", ["user_id"])
#     for user in current_users:
#         if user["user_id"] == interaction.user.id:
#             Database.delete("users", where=f"user_id='{interaction.user.id}'")
#             break

#     await interaction.response.send_message("Ta participation a bien été supprimée", ephemeral=True)

# @bot.tree.command(name="list", description="Affiche la liste des participants")
# async def list_users(interaction: Interaction):
        
#     current_users = Database.select("users", ["user_id"])
    
#     text = "Voici la liste des participants actuels :"    
#     for user in current_users:
#         text += f"\n\t-<@{user['user_id']}>"
        
#     await interaction.response.send_message(text, ephemeral=True)

# @bot.tree.command(name="roll", description="Lance le tirage au sort")
# async def roll(interaction: Interaction):
#     Database.delete("pairs")
    
#     current_users = Database.select("users", ["user_id"])
    
#     from_ids = [u["user_id"] for u in current_users]
#     shuffle(from_ids)
    
#     to_ids = from_ids[1:] + [from_ids[0]]
    
#     for from_id, to_id in zip(from_ids, to_ids):
#         Database.insert("pairs", {
#             "from_id": from_id,
#             "to_id": to_id,
#         })
        
#     await interaction.response.send_message("Les dés sont jetés !\nVous pouvez dès à présent voir la personne à que vous devez offrir un cadeau avec la commande /secret")

# @bot.tree.command(name="secret", description="Affiche le nom de la personne à qui tu vas offrir un cadeau")
# async def secret(interaction: Interaction):
#     if Database.select("pairs") == []:
#         await interaction.response.send_message("Le tirage n'a pas encore été effectué.", ephemeral=True)
#         return
    
#     data = Database.select("pairs", ["to_id"], where=f"from_id='{interaction.user.id}'")
#     await interaction.response.send_message(f"La personne qui t'a été attribuée est : <@{data[0]['to_id']}>", ephemeral=True)

# /manger
async def night_time_response(interaction: Interaction):
    await interaction.response.send_message(choice(night_sentences))

@bot.tree.command(name="manger", description="Affiche l'heure du prochain repas")
async def lunch(interaction: Interaction):    
    now = datetime.now()
    lunch, dinner = lunch_times[now.weekday()]
    
    if now.time() < lunch:
        if now.time() < night_time[1]:
            return await night_time_response(interaction)
        
        date = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=lunch.hour,
            minute=lunch.minute
        )
    elif now.time() < dinner:
        date = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=dinner.hour,
            minute=dinner.minute
        )
    else:
        if now.time() > night_time[0]:
            return await night_time_response(interaction)
        
        lunch, _ = lunch_times[(now.weekday() + 1) % 5]
        now += timedelta(days=1)
        
        date = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=lunch.hour,
            minute=lunch.minute
        )
    
    await interaction.response.send_message(choice(lunch_sentences).format(ts=int(date.timestamp())))
