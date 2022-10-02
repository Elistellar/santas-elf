from __future__ import annotations

import traceback
from random import shuffle

from discord import Embed, Intents, Interaction, Activity, ActivityType  
from discord.ext.commands import Bot

from .config import Config
from .database import Database
from .log import log


bot = Bot(
    command_prefix="/",
    intents=Intents.all(),
    owner_id=Config["owner_id"]
)

# events
@bot.event
async def on_ready():
    
    bot.guild = bot.get_guild(Config["guild_id"])
    
    # sync slash commands
    await bot.tree.sync()
    
    # change activity
    await bot.change_presence(activity=Activity(
        type=ActivityType.watching,
        name=Config["activity"]
    ))
    
    log.info("Bot ready !")
    
@bot.event
async def on_error(event, *args, **kwargs):
    log.error(traceback.format_exc())

@bot.tree.command(name="help", description="Affiche la liste des commandes")
async def help(interaction: Interaction):
    
    await interaction.response.send_message(embed=Embed(
        title="Liste des commandes",
        description="- </join:1025814910300594216> : Participe au Secret Santa !\n" + \
                    "- </leave:1025814910300594217> : Supprime ta participation au Secret Santa\n" + \
                    "- </list:1025814910300594218> : Supprime ta participation au Secret Santa\n" + \
                    "- </secrect:1025814910300594220> : Supprime ta participation au Secret Santa"
    ))

@bot.tree.command(name="join", description="Participe au Secret Santa !")
async def join(interaction: Interaction):
    
    current_users = Database.select("users", ["user_id"])
    for user in current_users:
        if user["user_id"] == interaction.user.id:
            await interaction.response.send_message("Tu participe déjà au Secret Santa", ephemeral=True)
            return
    
    Database.insert("users", {
        "user_id": interaction.user.id,
    })
    await interaction.response.send_message("Ta participation a bien été prise en compte !", ephemeral=True)

@bot.tree.command(name="leave", description="Supprime ta participation au Secret Santa")
async def leave(interaction: Interaction):
    current_users = Database.select("users", ["user_id"])
    for user in current_users:
        if user["user_id"] == interaction.user.id:
            Database.delete("users", where=f"user_id='{interaction.user.id}'")
            break

    await interaction.response.send_message("Ta participation a bien été supprimée", ephemeral=True)

@bot.tree.command(name="list", description="Affiche la liste des participants")
async def list_users(interaction: Interaction):
        
    current_users = Database.select("users", ["user_id"])
    
    text = "Voici la liste des participants actuels :"    
    for user in current_users:
        text += f"\n\t-<@{user['user_id']}>"
        
    await interaction.response.send_message(text, ephemeral=True)

@bot.tree.command(name="roll", description="Lance le tirage au sort")
async def roll(interaction: Interaction):
    Database.delete("pairs")
    
    current_users = Database.select("users", ["user_id"])
    
    from_ids = [u["user_id"] for u in current_users]
    shuffle(from_ids)
    
    to_ids = from_ids[1:] + [from_ids[0]]
    
    for from_id, to_id in zip(from_ids, to_ids):
        Database.insert("pairs", {
            "from_id": from_id,
            "to_id": to_id,
        })
        
    await interaction.response.send_message("Les dés sont jetés !\nVous pouvez dès à présent voir la personne à que vous devez offrir un cadeau avec la commande /secret")

@bot.tree.command(name="secret", description="Affiche le nom de la personne à qui tu vas offrir un cadeau")
async def secret(interaction: Interaction):
    if Database.select("pairs") == []:
        await interaction.response.send_message("Le tirage n'a pas encore été effectué.", ephemeral=True)
        return
    
    data = Database.select("pairs", ["to_id"], where=f"from_id='{interaction.user.id}'")
    await interaction.response.send_message(f"La personne qui t'a été attribuée est : <@{data[0]['to_id']}>")
