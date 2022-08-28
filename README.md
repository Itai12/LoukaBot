# LoukaBot

Fork du MTbot modifié spécialement pour représenter aux mieux le Bakistan sur Mathraining.

Installation : 

```
$ git clone https://github.com/Itai12/LoukaBot.git
$ cd LoukaBot/
$ pip install -r requirements.txt
$ sudo apt-get install wkhtmltoimage sqlite3
$ cp options-template.yml options.yml
$ touch db.sqlite3
```

Il faut ensuite modifier le fichier options.yml avec les valeurs requises.

Lancement : 

```
$ python3 DiscordCommands.py
```

Principales fonctions rajoutées et description :
- &comparepbs : compare les problèmes résolus par 2 utilisateurs
- &spam : spam un message
- &domain : compare la progression par domaine avec un graphe
- &sql : injecte une commande sql (commande de test)
- &top : classement des meilleurs pays
- &moyenne : moyenne d'un pays
- &ping : Pong !
- &execute : execute un code python (commande de test)
- &bakistan : rappelle la superiorité du Bakistan
- &classement : classement des utilisateurs reliés du serveur par catégorie
- &userinfo : donne les informations sur un utilisateur
- &serverinfo : donne les informations sur un serveur
- &ban : Ban un utilisateur
- &kick : Kick un utilisateur
- &clear : supprime des messages
- &meme : envoie un meme random
- &botinfo : donne des informations sur le bot
- &baron : prie le baron fou
- &calc : effectue un calcul
- &restart : redémarre le bot
- &problems : 10 dernières résolutions récentes
- &search : recherche un utilisateur dans mathraining par nom
- &emoji : ajouter un emoji à ceux du serveur
- &membres : retourne les membres d'un pays
- &cmd : execute une commande dans le terminal (comande de test)
- &screenfetch : execute un screenfetch

Commande en cours :
- &setgame : permet de jouer au set
- &searchpays : cherche un pays par nom

Diverses améliorations : 
- création d'une base de donnée pour stocker les données (plus simple et plus efficace)

Si vous repérez des problèmes ou avez des idées de fonctionnalités à créér, merci d'ouvrir une issue ou de me contacter par Discord (itai#4242)


<!--# MTbot : &bijou ne sera jamais implémenté ;)

Code source du bot du Discord de Mathraining.

Dépendances sur pip :
 - discord.py
 - discord-components
 - aiohttp
 - bs4 (beautiful soup 4)
 - lxml
 - PyYAML
 - Matplotlib
 - pytz

Autres dépendances :
 - wkhtmltopdf : https://wkhtmltopdf.org/downloads.html 
 (Il faut pouvoir lancer la commande "wkhtmltoimage" directement : à installer directement avec apt par ex.)
-->