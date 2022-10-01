# Santa's Elf

Santa's Elf est un bot Discord destiné à organiser des Secrets Santa pour vos Noêl entre amis !
Le bot dispose de 6 commandes :
- `/help` (il y a t-il vraiment besoin d'expliciter ?)
- `/join` pour rejoindre le Secret Santa
- `/leave` pour le quitter
- `/list` pour voir la liste des personnes participantes
- `/roll` pour effectuer le tirage au sort
- `/secret` pour voir quelle personne nous a été attribuée une fois le tirage au sort effectué


## Installation
La seule dépendance et `discord.py 2.0.0` _(cf requirements.txt)_ .
Pour que le bot fonctionne correctement, il faut ajouter à la racine du projet un fichier nommé `config.json` contenant le token et l'activité du bot.

```json
{
    "token": "LE TOKEN VA ICI",
    "activity": "L ACTIVITE VA ICI"
}
```
