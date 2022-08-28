from discord import *
import discord
from discord.ext import commands, tasks
from discord.utils import get
import requests
from discord_components import *
import sqlite3
import datetime, pytz
from email.utils import parsedate_to_datetime
import aiohttp
import re

from bs4 import *
import asyncio
from asyncio import *

from re import compile

from random import randint

import AnnexePendu
import AnnexeCompteBon
import AnnexeCompare
import AopsCore

from traceback import format_exc
from yaml import safe_load
db=sqlite3.connect("db.sqlite3")
cur=db.cursor()
intents = Intents.default()
intents.members = True

description = 'Bot Mathraining.'
bot = commands.Bot(command_prefix='&', description='Bot Mathraining, merci aux génialissimes créateurs !',intents=intents)

#____________________CONSTANTES_______________________________

with open('options.yml', 'r') as options_file : options = safe_load(options_file)

with open("Problems.txt") as file:
    PROBLEMS_MT = { int(line.split()[0]): int(line.split()[1]) for line in file }

NomsRoles = ["Grand Maitre", "Maitre", "Expert", "Chevronné", "Expérimenté", "Qualifié", "Compétent", "Initié", "Débutant", "Novice"]

#colors = {'Novice' : 0x888888, 'Débutant' : 0x08D508, 'Débutante' : 0x08D508, 'Initié' : 0x008800, 'Initiée' : 0x008800,
#          'Compétent' : 0x00BBEE, 'Compétente' : 0x00BBEE, 'Qualifié' : 0x0033FF, 'Qualifiée' : 0x0033FF, 'Expérimenté' : 0xDD77FF,
#          'Expérimentée' : 0xDD77FF, 'Chevronné' : 0xA000A0, 'Chevronnée' : 0xA000A0, 'Expert' : 0xFFA000, 'Experte' : 0xFFA000,
#          'Maître' : 0xFF4400, 'Grand Maître' : 0xCC0000}


no_mention = AllowedMentions(users=False, roles=False, everyone=False)

msghelp = "\nTaper la commande `&help` pour plus d'informations."

errmsg ="Une erreur a été rencontrée, contactez un Admin ou un Modérateur."
perms="Vous n'avez pas les permissions pour effectuer cette commande."

points_combi=0
points_geo=0
points_tn=0
points_alg=0
points_ef=0
points_ine=0
dico={"1":15,"2":30,"3":45,"4":60,"5":75}
with open("Problems.txt","r") as f:
    content=f.read().split("\n")
for i in content:
    if i[0]=="1":
        points_combi+=dico[i[1]]
    elif i[0]=="2":
        points_geo+=dico[i[1]]
    elif i[0]=="3":
        points_tn+=dico[i[1]]
    elif i[0]=="4":
        points_alg+=dico[i[1]]
    elif i[0]=="5":
        points_ef+=dico[i[1]]
    elif i[0]=="6":
        points_ine+=dico[i[1]]

# get content of https://mathraining.be/users/1286
url="https://mathraining.be/users/1286"
print("page loading")
#t=requests.get(url)
with open("test.html") as f:
    t=f.read()
print("page loaded")
#with open("test.html","w") as f:
#    f.write(t.text)
soup=BeautifulSoup(t,"lxml")
# get <tr> element where there is a link contening "?link="
def GetLink(soup, link):
    list_tr=[]
    for tr in soup.find_all('tr'):
        for j in tr.find_all("td"):
            if "Exercice" in str(j):
                list_tr.append(tr)
    return list_tr

liste=GetLink(soup,"?type=")

with open("Exercices.txt") as f:
    exos=f.read().split("\n\n")

dicexo=dict()
for i in exos:
    k=i.split("\n")
    dicexo[k[0]]=k[1]

for j in liste[1:]:
    i=str(j)
    i1=i.index("Exercice")+23
    #print(i,i[i1:])
    i2=i1
    while i[i2:i2+5]!="</td>":
        i2+=1
    matiere=dicexo[i[i1:i2-11].replace(" ","").replace("-","")]
    if matiere=="1":
        i3=i.index("+")
        if i[i3+3]=="<":
            points_combi+=int(i[i3+2])
        else:
            points_combi+=int(i[i3+2:i3+4])
    elif matiere=="2":
        i3=i.index("+")
        if i[i3+3]=="<":
            points_geo+=int(i[i3+2])
        else:
            points_geo+=int(i[i3+2:i3+4])       
    elif matiere=="3":
        i3=i.index("+")
        if i[i3+3]=="<":
            points_tn+=int(i[i3+2])
        else:
            points_tn+=int(i[i3+2:i3+4])      
    elif matiere=="4":
        i3=i.index("+")
        if i[i3+3]=="<":
            points_alg+=int(i[i3+2])
        else:
            points_alg+=int(i[i3+2:i3+4])      
    elif matiere=="5":
        i3=i.index("+")
        if i[i3+3]=="<":
            points_ef+=int(i[i3+2])
        else:
            points_ef+=int(i[i3+2:i3+4])      
    elif matiere=="6":
        i3=i.index("+")
        if i[i3+3]=="<":
            points_ine+=int(i[i3+2])
        else:
            points_ine+=int(i[i3+2:i3+4])    

print(points_alg,points_combi,points_ef,points_geo,points_ine,points_tn,points_alg+points_combi+points_ef+points_geo+points_ine+points_tn)       

##_________________Fonctions_Annexes____________________

async def GetMTScore(idMT: int, ret_soup = False) :
    async with aclient.get(f"https://www.mathraining.be/users/{idMT}") as response: text = await response.text()
    soup = BeautifulSoup(text,"lxml")

    score = 0
    tds = soup.find_all('td', limit = 5)
    if len(tds) == 0: score = 2 # Identifiant non attribué
    elif len(tds) > 4: score = int(tds[4].getText().strip())
    elif tds[1].getText().strip() in ("Administrateur", "Administratrice"): score = 1 # Administrateur
    return (score, soup) if ret_soup else score

def roleScore(s):
    """Renvoie le role correspondant au score"""
    if s >= 7500:   return "Grand Maitre"
    elif s >= 5000: return "Maitre"
    elif s >= 3200: return "Expert"
    elif s >= 2000: return "Chevronné"
    elif s >= 1250: return "Expérimenté"
    elif s >= 750:  return "Qualifié"
    elif s >= 400:  return "Compétent"
    elif s >= 200:  return "Initié"
    elif s >= 70:   return "Débutant"
    elif s == 2 :   return "Inconnu"
    elif s == 1 :   return "Administrateur"
    else:           return "Novice"

async def GetDiscordUser(ctx,user) :
    user1 = None
    if user.isdigit(): user1 = bot.get_user(int(user))
    if not user1:
        r = compile(r"<@(!|)([0-9]+)>").search(user)
        if r: user1 = bot.get_user(int(r.group(2)))
    if not user1:
        r = compile(r"^([^#]+)#([0-9]{4})$").search(user)
        if r: user1 = get(serveur.members, name=r.group(1), discriminator=r.group(2))
    if not user1:
        user1 = get(serveur.members, nick=user)
    if not user1:
        user1 = get(serveur.members, name=user)
    return user1

def FindUser(user: Member, en_attente=False) :
    id=str(user.id)
    results=cur.execute("SELECT mt FROM idMT WHERE `discord` = "+id+";").fetchall()
    if len(results)>0:
        return results[0][0]
    return 0

async def FindMTUser(user_str : str, ctx, print_msgs = True):
    if user_str.isdigit() and len(user_str) <= 5:
        return int(user_str)
    else:
        user = await GetDiscordUser(ctx, user_str)
        if not user and print_msgs:
            await ctx.channel.send(f"**{user_str}**: Utilisateur introuvable."+msghelp, allowed_mentions=no_mention)
            return 0
        id = FindUser(user)
        if not id and print_msgs:
            await ctx.channel.send(f"L'utilisateur {user.mention} n'est pas rattaché à un compte Mathraining.\nTapez la commande `&ask id` (en remplaçant id par votre id mathraining) pour relier votre compte et la commande `&help` pour en savoir plus", allowed_mentions=no_mention)
            return 0
        return id

class MTid(commands.Converter):
    async def convert(self, ctx, user_str):
        id = await FindMTUser(user_str or str(ctx.author.id), ctx)
        if id: return id
        else: raise Exception # on quitte la commande
    async def me(ctx):
        id = await FindMTUser(str(ctx.author.id), ctx)
        if id: return id
        else: raise Exception

def FindMT(idMT: int, en_attente=False) :
    idMT = int(idMT)
    results=cur.execute("SELECT discord FROM idMT WHERE `mt` = "+str(idMT)+";").fetchall()
    if len(results)>0:
        return results[0][0]
    return 0

regex_auth_token = compile(r'<input type="hidden" name="authenticity_token" value="([A-Za-z0-9+/=]+)" />')

async def mt_connexion(aclient):
    try:
        resp = await aclient.get('https://www.mathraining.be/')
        authenticity_token = regex_auth_token.search(await resp.text()).group(1)
        await aclient.post('https://www.mathraining.be/sessions', data = {
            'utf8': "✓",
            'authenticity_token': authenticity_token,
            'session[email]': options['user'],
            'session[password]': options['password'],
            'session[remember_me]': "0",
        })
    except (IndexError, AttributeError): pass # déjà connecté

async def mt_send_mp(idMT, msg):
    resp = await aclient.get(f'https://www.mathraining.be/discussions/new')
    authenticity_token = regex_auth_token.search(await resp.text()).group(1)
    req = await aclient.post('https://www.mathraining.be/discussions', data = {
        'utf8': "✓",
        'authenticity_token': authenticity_token,
        'destinataire': f"{idMT}",
        'content': msg,
    }, allow_redirects=False)
    if req.status != 302:
        raise RuntimeError("Impossible d'envoyer un message privé sur mathraining. Vérifiez que le login/mot de passe sont corrects.")

async def erreur(e,ctx=None,switch=1) :
    try:
        err="- "+"[Erreur "+e+'] '+'-'*50+" [Erreur "+e+']'+" -"+'\n'+format_exc()+"- "+"[Erreur "+e+'] '+'-'*50+" [Erreur "+e+']'+" -";print(err)
        err="```diff\n"+err+"```"
        await canalLogsBot.send(err)
        if ctx:
            emb=Embed()
            emb.set_image(url=options['AdrienFail'] if switch == 2 else options['FirmaFail'])
            await ctx.send("**[Erreur "+e+']** '+"`"+errmsg+"`"+" **[Erreur "+e+']**', embed=emb)
    except Exception as e:
        print(format_exc())

import functools
def log_errors(name, switch=1): # use after @bot.command()
    def wrapper(func):
        @functools.wraps(func)
        async def f(*args, **kwargs):
            try: return await func(*args, **kwargs)
            except Exception as exc:
                if type(exc) != Exception:
                    if len(args) > 0 and type(args[0]) == commands.Context:
                        await erreur(name, args[0], switch=switch)
                    else:
                        await erreur(name, switch=switch)
        return f
    return wrapper

def admin_or_modo(arg):
    if hasattr(arg, '__call__'):
        @functools.wraps(arg)
        async def f(ctx, *args, **kwargs):
            if admin_or_modo(ctx): return await arg(ctx, *args, **kwargs)
            else: await send_message(ctx,perms)
        return f
    else:
        member = serveur.get_member(arg.author.id if type(arg) == commands.Context else arg.id)
        for i in member.roles:
            if i.name in ("Admin", "Modo"):
                return True
        return False

def serv_only(func):
    @functools.wraps(func)
    async def f(ctx, *args, **kwargs):
        if ctx.guild == serveur: return await func(ctx, *args, **kwargs)
    return f

##_________________________EVENT_______________________________________

@bot.event
async def on_ready():
    print('------')
    print('Connecté sous')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    global serveur
    global canalInfoBot, canalEnAttente, canalGeneral, canalResolutions, canalLogsBot, canalRoles, canalEntreesSorties
    global PenduRunner
    global msg_ids_links, msg_ids_links_tmp
    global solvedpbs_ping_settings
    global aclient

    print("Chargement ...", end="\r")
    DiscordComponents(bot)

    msg_ids_links, msg_ids_links_tmp = {}, {}

    aclient = aiohttp.ClientSession()

    PenduRunner = AnnexePendu.Pendu()

    serveur = bot.get_guild(options['IdServeur'])
    canalGeneral = serveur.get_channel(options['IdGeneral'])
    canalResolutions = serveur.get_channel(options['IdResolutions'])
    canalLogsBot = serveur.get_channel(options['IdLogsBot'])
    canalEntreesSorties = serveur.get_channel(options['IdEntreesSorties'])
    if not task.is_running(): task.start()

    print("Bot prêt !    ")
    # get user where id = 690125478958333956
    user = bot.get_user(690125478958333956)
    await user.send("Bot prêt !")
    await bot.change_presence(activity=Game(name="Mathraining | &help"))
@bot.event
@serv_only
async def on_member_update(before, after):
    role_verifie = get(serveur.roles, name = "Vérifié")
    if role_verifie not in before.roles and role_verifie in after.roles:
        fmt = 'Bienvenue '+ after.mention + " ! Pense à lier ton compte Mathraining avec la commande `&ask`. \n" + \
        "Si tu as des problèmes avec cette commande tape `&help` pour en savoir plus sur le bot ou va faire un tour dans <#726480900644143204>. :wink:"
        await canalEntreesSorties.send(fmt)

@bot.event
@serv_only
async def on_member_remove(member):
    await canalEntreesSorties.send(f"**{member}** a quitté le serveur.")

@bot.event
async def on_command_error(ctx, error):
    # if an exception is raised due to a to long message, send a pastebin

    if type(error) == commands.MemberNotFound:
        await ctx.channel.send(f"**{error.argument}**: Utilisateur introuvable."+msghelp, allowed_mentions=no_mention)
    elif type(error) != Exception and type(error) != commands.ConversionError and type(error) != commands.CommandNotFound:
        raise error
@bot.event
async def on_message(message):
    #_____COMMANDE POUR AFFICHER LES PROBLEMES_____
    if '#' in message.content and message.author != bot.user:
        msg = message.content.split()
        for i in msg:
            if i[0]== '#' and i[5:6]=='' and i[4:5]!='' and i[1:5].isdigit() : #On vérifie que le nombre a exactement 4 chiffres
                numeroPb = int(i[1:5])
                if numeroPb in PROBLEMS_MT:
                    aEnvoyer = f"Problème #{numeroPb} : https://www.mathraining.be/problems/{PROBLEMS_MT[numeroPb]}"
                    await message.channel.send(aEnvoyer)
    await bot.process_commands(message)

##_____________________COMMANDES___________________________________

@bot.command(pass_context=True)
@log_errors("ASK")
async def ask(ctx,idMTnew: int):
    '''Pour pouvoir utiliser le bot: ask @utilisateur idMathraining
    (idMathraining est le nombre dans l'url de votre page de profil sur le site)'''
    pascontent="Nicolas ne va pas être content si vous vous êtes fait un autre compte !! :sweat_smile:"
    contact="Contactez un Admin ou un Modo si vous souhaitez changer de compte."
    user=ctx.message.author
    idMTold, idMTatt = FindUser(user), FindUser(user, True)
    if idMTold == 0 and idMTatt == 0 :
        Score=await GetMTScore(idMTnew)
        UserId,UserIdatt = FindMT(idMTnew), FindMT(idMTnew, True)
        if UserId != 0 : await msay.edit(content="Ce compte Mathraining appartient déjà à "+str(bot.get_user(UserId))+" !")
        elif UserIdatt != 0: await msay.edit(content="Ce compte Mathraining a déjà été demandé à être relié par "+str(bot.get_user(UserIdatt))+" !")
        elif Score == 2 : await msay.edit(content="Le compte Mathraining renseigné n'existe pas !")
        else :
            await verify(ctx,idMT2=idMTnew)
    elif idMTold == idMTnew and idMTold != 0 : await msay.edit(content="Vous êtes déjà relié au bot avec le même id !")
    elif idMTatt == idMTnew and idMTatt !=0 : await msay.edit(content="Vous avez déjà fait une demande avec le même id !")
    elif idMTatt != idMTnew and idMTold ==0 : await msay.edit(content="Vous avez déjà fait une demande avec l'id "+str(idMTatt)+".\n"+pascontent+"\n"+contact)
    else : await msay.edit(content="Vous êtes déjà relié au bot avec l'id "+str(idMTold)+".\n"+pascontent+"\n"+contact)

@bot.command(pass_context=True)
@log_errors("VERIFY")
async def verify(ctx,user2: Member = None,idMT2: int = 0):
    """Lie le compte d'un utilisateur au bot (ajoute son id MT dans le canal Info-bot) """
    user=ctx.message.author
    msay = await send_message(ctx,"`Chargement en cours ...`")
    if idMT2!=0 :                            ##Sinon ignore les autres arguments ...

        verified=True
        if verified:
            msg="Vos comptes Discord et Mathraining sont désormais reliés !"
            role = roleScore(await GetMTScore(idMT2))
            servRole = get(serveur.roles, name = role)
            await user.add_roles(servRole)

            await msay.edit(content=f"La demande de lien a été acceptée par le compte Mathraining ! Vous obtenez le rôle {servRole.mention if ctx.guild == serveur else f'`{servRole}`'}! :clap:", allowed_mentions=no_mention)
            cur.execute("INSERT INTO idMT VALUES ("+str(user.id)+","+str(idMT2)+");")
            db.commit()
            print("utilisateur",user,"relié au bot avec l'ID",idMT2)
        else :
            msg="Les comptes Discord et Mathraining en question ne seront pas reliés."
            await mt_send_mp(idMT, msg)

            await msay.edit(content="La demande de lien a été refusée par le compte Mathraining.")

    elif FindUser(user) != 0 : await msay.edit(content="Vous êtes déjà lié avec l'id "+str(FindUser(user))+".")
    else : await msay.edit(content="Vous n'avez fait aucune demande pour lier vos comptes Discord et Mathraining.")

@bot.command(pass_context=True)
@log_errors("UPDATE")
async def update(ctx, user: Member = None):
    '''Pour mettre à jour son/ses roles'''
    if not user: user = serveur.get_member(ctx.author.id)
    idMT = await FindMTUser(str(user.id), ctx)

    if idMT != 0:
        role = roleScore(await GetMTScore(idMT))
        if role == -1: await erreur('ROLESCORE',ctx); return

        roles=user.roles
        for roleMembre in roles:
            if roleMembre.name in NomsRoles and roleMembre.name != role : await user.remove_roles(roleMembre)

        if role not in [r.name for r in roles] :
            role_to_add = get(serveur.roles, name = role)
            await user.add_roles(role_to_add)
            if user == ctx.message.author : await send_message(ctx,f"Bravo, vous obtenez le rôle {role_to_add.mention if ctx.guild == serveur else f'`{role_to_add}`'}! :clap:", allowed_mentions=no_mention)
            else : await send_message(ctx,str(user)+f" obtient désormais le rôle {role_to_add.mention if ctx.guild == serveur else f'`{role_to_add}'}! :clap:", allowed_mentions=no_mention)
        else : await send_message(ctx,"Déjà à jour !")

@bot.command(pass_context=True)
@log_errors("INFO")
async def info(ctx, idMT: MTid = None):
    """Affiche les stats d'un utilisateur lié"""
    if not idMT:
        idMT = await MTid.me(ctx)

    url="https://www.mathraining.be/users/"+str(idMT)
    async with aclient.get(url) as response: text = await response.text()
    soup = BeautifulSoup(text, "lxml")

    Infos=list(filter(None,[i.getText().strip() for i in soup.find_all('td', limit = 39)]))
    if len(Infos) == 3:
        country = soup.select_one("td img")['src'].split('/')[-1].split('-')[0]
        embed = Embed(title=f"{Infos[0]} - {Infos[1]} :flag_{country}:", url=url, description="Membre n°"+str(idMT))
        await ctx.send(embed=embed);return
    elif len(Infos) < 3:
        await send_message(ctx,content="Le compte Mathraining renseigné n'existe pas !");return

    country = soup.select_one("td img")['src'].split('/')[-1].split('-')[0]
    if country == "tp": country = "tl"
    elif country == "uk": country = "gb"

    embed = Embed(title=f"{Infos[0]} - {Infos[1]} :flag_{country}:", url=url, description="Membre n°"+str(idMT)+3*' '+"Rang : "+Infos[6]+"  Top  "+Infos[8]+(7-len(Infos[6]+Infos[8]))*' ' +" <:gold:979070616185487440> : "+Infos[9]+" <:silver:979070616118366298> : "+Infos[10]+" <:bronze:979070616118386768> : "+Infos[11]+" <:mh:979070615820574851> : "+Infos[12], color=int(soup.find('td').find_all('span')[-1]['style'].split('#')[1].split(';')[0], 16))
    embed.add_field(name="Score : ", value=Infos[4], inline=True)
    embed.add_field(name="Exercices résolus : ", value=''.join(Infos[14].split()), inline=True)
    embed.add_field(name="Problèmes résolus : ", value=''.join(Infos[16].split()), inline=True)
    for i in range(6): embed.add_field(name=Infos[17+2*i]+' :', value=Infos[18+2*i], inline=True)

    await ctx.send(embed=embed)

@bot.event
@log_errors("BUTTON")
async def on_button_click(interaction):
    #print(f"{interaction.author} a cliqué sur {interaction.custom_id}")
    if interaction.custom_id.startswith("aops-"):
        await AopsCore.process_click(interaction, aclient)

@bot.command(pass_context=True)
@log_errors("PROGRESS")
async def progress(ctx, idMT: MTid = None):
    if not idMT: idMT = await MTid.me(ctx)
    async with ctx.channel.typing():
        img, name, pts, color = await AnnexeCompare.progress_graph(ctx, idMT, aclient)
        if img:
            file = File(img)
            embed = Embed(title=f'Évolution de **{name} ({pts})**', color=color)
            embed.set_image(url=f"attachment://progress.png")
            await ctx.send(file=file, embed=embed)

@bot.command(pass_context=True)
async def domain(ctx, idMT: MTid = None):
    if not idMT: idMT = await MTid.me(ctx)
    async with ctx.channel.typing():
        img, name, pts, color = await AnnexeCompare.progress_domain(ctx, idMT, aclient)
        if img:
            file = File(img)
            embed = Embed(title=f'Évolution de **{name}**', color=color)
            embed.set_image(url=f"attachment://progress.png")
            await ctx.send(file=file, embed=embed)

@bot.command()
@log_errors("COMPARE")
async def compare(ctx, id1: MTid, id2: MTid = None):
    if not id2: id1, id2 = await MTid.me(ctx), id1
    if id1 == id2: await ctx.channel.send(f"Pourquoi se comparer avec soi même ?\nSi vous souhaitez afficher l'évolution d'un utilisateur, vous pouvez utiliser la commande `&progress`. :wink:")
    else:
        async with ctx.channel.typing():
            img, name, pts, name2, pts2 = await AnnexeCompare.compare_graph(ctx, id1, id2, aclient)
            if img:
                embed = Embed(title=f'**{name} ({pts})** vs **{name2} ({pts2})**', color=0x87CEEB)
                embed.set_image(url="attachment://compare.png")
                await ctx.send(file=File(img), embed=embed)

@bot.command()
@log_errors("CORRECTIONS")
async def corrections(ctx,switch=""):
    """Affiche la liste des correcteurs et leurs nombres de corrections"""
    async with aclient.get("https://www.mathraining.be/correctors") as response: text = await response.text()
    soup = BeautifulSoup(text, "lxml")

    sum1, sum2 = 0, 0
    rows = []
    max1, max2 = 0, 0
    for corrector in soup.find_all('table')[1].find_all('tr')[1:]:
        tds = corrector.find_all('td')
        if tds[2].text != '0' or switch == 'all':
            rows.append((tds[0].text, tds[1].text, tds[2].text))
            max1 = max(max1, len(tds[0].text))
            max2 = max(max2, len(tds[1].text))
        sum1 += int(tds[1].text)
        sum2 += int(tds[2].text)

    s = []
    format_str = f"{{:<{max1 + 3}}} {{:<{max2 + 3}}} {{}}\n"
    i = 0
    for row in rows:
        if i % 20 == 0:
            s.append("")
        s[-1] += format_str.format(*row)
        i += 1
    embed = Embed(title=f"Corrections ({sum1} corrections dont {sum2} les deux dernières semaines) : ", color=0xFF4400)
    for i in s:
        embed.add_field(name="\u200b", value="```"+i+"```", inline=False)
    await ctx.send(embed=embed)



@bot.command()
@log_errors("SOLVED")
async def solved(ctx, idMT: MTid, idpb: int):
    """Indique si le problème numéro numPb a été résolu par l'utilisateur"""
    async with aclient.get(f"https://www.mathraining.be/users/{idMT}") as resp : response = await resp.text()
    namepb = '#' + str(idpb)
    await send_message(ctx,"Problème"+[" non "," "][namepb in response]+"résolu par l'utilisateur.")

@bot.command()
async def hi(ctx):
    await send_message(ctx,"Salut ! Comment vas-tu ?")

@bot.command(pass_context = True)
@admin_or_modo
async def say(ctx, *, arg):
    await canalGeneral.send(arg)

@bot.command()
@log_errors("COMPTE")
async def compte(ctx, tuile: tuple = (-1,-1,-1,-1,-1,-1),trouver: int = -1,sols=1):
    if (tuile,trouver,sols) == ((-1,-1,-1,-1,-1,-1),-1,1) :
        resultat,tuiles = AnnexeCompteBon.compteBon()
        tirage="Tuiles : " + " ".join(map(str,tuiles)) +  "\nÀ trouver : " + str(resultat)
        embed = Embed( title = "Le compte est bon", color = 0xFF4400 )
        embed.add_field( name = "Tirage", value = tirage, inline = False )
    else:
        embed = Embed( title = "Le compte est bon", color = 0xFF4400 )
        tuile2 = list(map(int, "".join(tuile).split(",")))
        if len(tuile2)==6 :
            res=AnnexeCompteBon.Solve(trouver,tuile2,sols); msg = ''
            for s in res : msg+=s;msg+='\n'
            if msg : embed.add_field( name = "Voici "+str(len(res))+" solution(s) choisie(s) au hasard :", value = msg, inline = False)
            else : embed.add_field( name = "Mince !", value = "Il n'y a pas de solution ...", inline = False)
        else : embed.add_field( name = "Mince !", value = "Il n'y a pas le bon nombre de tuiles ...", inline = False)
    await ctx.send(embed=embed)

@bot.command()
@log_errors("LETTRES")
async def lettres(ctx):
    tirage="Tuiles : " + " ".join(AnnexeCompteBon.Lettres())
    embed = Embed( title = "Le mot le plus long", color = 0xFF4400 )
    embed.add_field( name = "Tirage", value = tirage, inline = False)
    await ctx.send(embed=embed)

@bot.command()
@log_errors("PENDU", 2)
async def pendu(ctx, tuile: str = ''):
    await AnnexePendu.pendu(ctx, tuile, PenduRunner)

@bot.command()
@log_errors("CITATION")
async def citation(ctx):
    async with aclient.get("http://math.furman.edu/~mwoodard/www/data.html") as response: text = await response.text()
    soup = BeautifulSoup(text, "lxml") #Penser à modifier la source soi-même ?
    bout = str(soup.find_all('p')[randint(0,756)]).replace("<br/>", "\n")
    citation = (BeautifulSoup(bout, "lxml").getText()).split('\n')
    c=''
    for s in citation[1:-2] : c+=(s+'\n')
    c+=citation[-2]
    embed = Embed(title=citation[0], colour=0x964b00, description='_'+c+'_')
    embed.set_author(name="Citations Mathématiques")
    embed.set_footer(text=citation[-1])
    await ctx.send(embed=embed)

@bot.command(pass_context = True)
@log_errors("AOPS")
async def aops(ctx):
    await AopsCore.aopscore(bot, ctx, aclient)

@bot.command()
async def _aops_cache(ctx): await send_message(ctx,f"Le cache contient actuellement {len(AopsCore.cache)} catégories, et au total {sum(len(i['items']) for i in AopsCore.cache.values())} items.")
@bot.command()
async def _aops_cache_clear(ctx): AopsCore.cache.clear()

@bot.command(pass_context = True)
async def oops(ctx):
    await ctx.message.add_reaction('😅')

@bot.command(pass_context = True)
async def trivial(ctx):
    await ctx.message.add_reaction('😒')
## TEST FUNCTION, DO NOT RUN ON PROD

@bot.command(pass_context = True)
async def sql(ctx,*message):
    if str(ctx.author.id) == "690125478958333956":
        msg=" ".join(message)
        return_value=db.execute(msg).fetchall()
        await send_message(ctx,return_value)
    else:
        await send_message(ctx,"Tu veux quoi là ?")

async def get_pays_name(id_pays:int):
    async with aclient.get(f"https://www.mathraining.be/users?title=0&country={id_pays}") as resp : response = await resp.text()
    soup = BeautifulSoup(response, "lxml")
    return soup.find_all('img',{'id':f'flag_1_{str(id_pays)}'})[0].get('title')

async def calc_moyenne(id_pays:int=97) -> (float,int):
    # to verify
    url='https://www.mathraining.be/users?country='+str(id_pays)+'&page=1&title=0'
    async with aclient.get(url) as response: t = await response.text()
    try:
        ind=t.index("pagination")
        while t[ind:ind+5]!="</ul>":
            if t[ind:ind+5]=="</li>" and t[ind+5:ind+10]!="</ul>":
                maxi=ind
            ind+=1
        nb_pages=int(t[maxi-7:maxi-4].replace(">","").replace(">","").replace("\"",""))
    except Exception as e:
        nb_pages=1
    liste_points=[]
    nb_joueurs=0
    liste_combi=[]
    liste_geo=[]
    liste_tn=[]
    liste_alg=[]
    liste_ef=[]
    liste_ine=[]
    for i in range(1,nb_pages+1):
        url='https://www.mathraining.be/users?country='+str(id_pays)+'&page='+str(i)+'&title=0'
        async with aclient.get(url) as response: text = await response.text()
        for j in range(len(text)):
            if text[j:j+6]=="score_":
                nb_joueurs+=1
                liste_points.append(int(text[j+17:j+22].replace("<","").replace("/","").replace("t","").replace("d","").replace("c","").replace(">","").replace("e","")))
            elif text[j:j+12]=="pct_section_":
                k=j+13
                while text[k]!="_":
                    k+=1
                if text[k+1]=="1":
                    liste_combi.append(int(text[k+46:k+55].replace("<","").replace("/","").replace("t","").replace("d","").replace("c","").replace(">","").replace("e","").replace("%","").replace(";","").replace("\"","").replace("-","0")))
                elif text[k+1]=="2":
                    liste_geo.append(int(text[k+46:k+55].replace("<","").replace("/","").replace("t","").replace("d","").replace("c","").replace(">","").replace("e","").replace("%","").replace(";","").replace("\"","").replace("-","0")))
                elif text[k+1]=="3":
                    liste_tn.append(int(text[k+46:k+55].replace("<","").replace("/","").replace("t","").replace("d","").replace("c","").replace(">","").replace("e","").replace("%","").replace(";","").replace("\"","").replace("-","0")))
                elif text[k+1]=="4":
                    liste_alg.append(int(text[k+46:k+55].replace("<","").replace("/","").replace("t","").replace("d","").replace("c","").replace(">","").replace("e","").replace("%","").replace(";","").replace("\"","").replace("-","0")))
                elif text[k+1]=="5":
                    liste_ef.append(int(text[k+46:k+55].replace("<","").replace("/","").replace("t","").replace("d","").replace("c","").replace(">","").replace("e","").replace("%","").replace(";","").replace("\"","").replace("-","0")))
                elif text[k+1]=="6":
                    liste_ine.append(int(text[k+46:k+55].replace("<","").replace("/","").replace("t","").replace("d","").replace("c","").replace(">","").replace("e","").replace("%","").replace(";","").replace("\"","").replace("-","0")))
    return sum(liste_points)/nb_joueurs,nb_joueurs,sum(liste_combi)/nb_joueurs,sum(liste_geo)/nb_joueurs,sum(liste_tn)/nb_joueurs,sum(liste_alg)/nb_joueurs,sum(liste_ef)/nb_joueurs,sum(liste_ine)/nb_joueurs

async def top_pays():
    async with aclient.get("https://www.mathraining.be/users?title=0&country=0") as response: text = await response.text()
    soup = BeautifulSoup(text, "lxml")
    return soup.find_all('img',{'id':'flag_1_0'})[0].get('title')


@bot.command(pass_context=True)
async def top(ctx,min_user:int=10):
    if min_user<5:
        await send_message(ctx,"Erreur, votre nombre minimum de membres est trop petit, cela prend trop de temps de calcul\nMerci de recommencer avec une valeur supérieure ou égale à **5**")
        return
    # TODO : get @list_of_countries with at least @min_user users
    list_of_countries=[97,122,117,177,35,39,88]
    classement=[]
    for i in list_of_countries:
        moy,nb,combi,geo,tn,alg,ef,ine=await calc_moyenne(i)
        classement.append((i,moy,nb,combi,geo,tn,alg,ef,ine))
    classement.sort(key=lambda n:-n[1])
    message="```\n                    Score Combi  Géo  TN   Algèbre EF   Inégalités\n"
    for i in range(len(classement)):
        j=classement[i]
        name=await get_pays_name(j[0])
        message+=f"{i+1}  {name}({j[2]}) "+" "*(10-len(name))+f": {int(j[1])}  {round(j[3])}%{' '*(5-len(str(round(j[3]))))} {round(j[4])}%{' '*(3-len(str(round(j[4]))))} {round(j[5])}%{' '*(3-len(str(round(j[5]))))} {round(j[6])}%{' '*(6-len(str(round(j[6]))))} {round(j[7])}%{' '*(3-len(str(round(j[7]))))} {round(j[8])}%{' '*(5-len(str(round(j[8]))))}\n"
    await send_message(ctx,message+"```")
@bot.command(pass_context = True)
async def moyenne(ctx,id_pays:int=97):
    if id_pays==64:
        await send_message(ctx,"NON")
    else:
        moy_pts,nb_joueurs,combi,geo,tn,alg,ef,ine = await calc_moyenne(id_pays)
        await send_message(ctx,"```\n                 Score Combi  Géo  TN   Algèbre EF   Inégalités\n"+str(await get_pays_name(id_pays))+f" ({nb_joueurs})"+" "*(10-len(str(await get_pays_name(id_pays))))+f": {int(moy_pts)}  {round(combi)}%{' '*(5-len(str(round(combi))))} {round(geo)}%{' '*(3-len(str(round(geo))))} {round(tn)}%{' '*(3-len(str(round(tn))))} {round(alg)}%{' '*(6-len(str(round(alg))))} {round(ef)}%{' '*(3-len(str(round(ef))))} {round(ine)}%\n```")
@bot.command(pass_context = True)
async def makeloose(ctx,user:Member = None):
    try :
        author = ctx.message.author
        await (ctx.message).delete()
        if not author == user : await send_message(ctx,str(user.mention)+" _a perdu ..._")
        else : await send_message(ctx,str(user.mention)+" _a perdu tout seul ..._")
        await user.send("_42_")
    except :
        try : await (ctx.message).delete();await send_message(ctx,'<:blurryeyes:622399161240649751>')
        except : await send_message(ctx,'<:blurryeyes:622399161240649751>')

bot.remove_command('help')
@bot.command(pass_context = True)
@log_errors("HELP")
async def help(ctx):
    embed = Embed(title="Mathraining bot", type="rich", description="Préfixe avant les commandes : &. \n [Le code source est disponible.](https://github.com/Firmaprim/MTbot/)", color=0x87CEEB)
    embed.add_field(name="ask idMathraining", value="Pour demander à rattacher votre compte Mathraining." +
    "\n idMathraining est le nombre dans l'url de votre page de profil sur le site.", inline=False)
    embed.add_field(name="verify", value="Pour valider le lien de votre compte Mathraining avec votre compte Discord.", inline=False)
    embed.add_field(name="update", value="Pour mettre à jour son rang.", inline=False)
    embed.add_field(name="info (utilisateur/idMathraining)", value="Donne le score et le rang Mathraining de l'utilisateur Discord ou Mathraining."
    +"\n Les mentions, les surnoms tout comme les id Mathraining fonctionnent.\n Par défaut prend la personne qui a envoyé la commande comme utilisateur.", inline=False)
    embed.add_field(name="progress (utilisateur)", value="Affiche la courbe d'évolution d'un utilisateur Mathraining. Par défaut prend la personne qui a envoyé la commande.", inline=False)
    embed.add_field(name="compare utilisateur1 (utilisateur2)", value="Pour se comparer avec un utilisateur, ou comparer deux utilisateurs.", inline=False)
    embed.add_field(name="corrections (all)", value="Affiche la liste des correcteurs (qui ont corrigé récemment ou pas avec \"all\") et leurs contributions.", inline=False)
    embed.add_field(name="solved utilisateur numPb", value="Indique si le problème numéro numPb a été résolu par l'utilisateur.", inline=False)
    embed.add_field(name="hi", value="Permet d'effectuer un ping avec le bot.", inline=False)
    embed.add_field(name="compte (a,b,c,d,e,f ÀTrouver NbrSolutions)", value="Effectue un tirage de chiffres si aucun argument n'est donné, résout le tirage sinon.", inline=False)
    embed.add_field(name="lettres", value="Effectue un tirage de lettres.", inline=False)
    embed.add_field(name="pendu", value="Pour jouer au pendu.", inline=False)
    embed.add_field(name="citation", value="Affiche une citation mathématique au hasard.\n Source : [Furman University, Mathematical Quotations Server](http://math.furman.edu/~mwoodard/mquot.html)", inline=False)
    embed.add_field(name="aops", value="Permet d'avoir accès aux problèmes AoPS et les afficher.", inline=False)
    embed.add_field(name="moyenne (id_pays)", value="Permet d'afficher la moyenne d'un pays à partir de son ID", inline=False)
    ambed.add_field(name="top (min_joueurs)", value="Permet d'afficher un classement des pays comportant plus qu'un certain nombre de membres (par défaut 10)", inline=False)
    embed.add_field(name="help", value="Affiche ce message en MP.", inline=False)
    try:
        await ctx.author.send(embed=embed)
    except Forbidden:
        await send_message(ctx,"Impossible de vous envoyer l'aide. Peut-être avez-vous bloqué les messages privés, ce qui empêche le bot de communiquer avec vous.")

@bot.command()
@admin_or_modo
async def resolutions_setup(ctx):
    ping_emoji = get(serveur.emojis, name="ping")
    if not ping_emoji:
        await send_message(ctx,f"Emoji ping introuvable. Avez-vous bien un emoji nommé \"ping\" ?")
        return
    try:
        msg = await canalRoles.send(f"Souhaitez-vous être ping pour les {canalResolutions.mention} ?")
        await msg.add_reaction(ping_emoji)
        await send_message(ctx,f"Mettez```IdMessageRoles: {msg.id}``` dans `options.yml` puis redémarrez le bot.")
    except Forbidden:
        await send_message(ctx,f"Erreur. Vérifiez que le bot a bien les permissions pour poster dans {canalRoles.mention}.")

##Tâches d'arrière-plan

last_submission_date = None
statistiques = [0, 0, 0, 0]
nbRequetes = 0

@tasks.loop(minutes = 5)
@log_errors("TASK")
async def task():
    global last_submission_date, nbRequetes, statistiques

    # Chiffres remarquables
    response = await aclient.get("https://www.mathraining.be/", timeout=5)
    soup = BeautifulSoup(await response.text(), "lxml")

    taillePaquet = [100, 1000, 10000, 50000] # paliers utilisateurs; problèmes; exercices; points

    table = soup.find("table")
    for i, stat in enumerate(table.find_all("tr")):
        nombre = int("".join(stat.find("td").text.split()))

        if nombre//taillePaquet[i] > statistiques[i]:
            if statistiques[i] == 0: # pour éviter de spam au lancement du bot
                statistiques[i] = nombre//taillePaquet[i]
            else:
                statistiques[i] = nombre//taillePaquet[i]
                if i == 0 : message = f"Oh ! Il y a maintenant {(nombre//taillePaquet[i])*taillePaquet[i]} utilisateurs sur Mathraining ! 🥳"
                elif i == 1 : message = f"Oh ! Il y a maintenant {(nombre//taillePaquet[i])*taillePaquet[i]} problèmes résolus ! 🥳"
                elif i == 2 : message = f"Oh ! Il y a maintenant {(nombre//taillePaquet[i])*taillePaquet[i]} exercices résolus ! 🥳"
                elif i == 3 : message = f"Oh ! Il y a maintenant {(nombre//taillePaquet[i])*taillePaquet[i]} points distribués ! 🥳"

                await canalGeneral.send(embed=Embed(description=message, color=0xF9E430))

    # Résolutions récentes
    response = await aclient.get("https://www.mathraining.be/solvedproblems", timeout=5)
    soup = BeautifulSoup(await response.text(), "lxml")

    if 'Date' in response.headers:
        now = parsedate_to_datetime(response.headers['Date']).replace(second = 0, tzinfo = None)
        now += datetime.timedelta(hours = int(datetime.datetime.now(pytz.timezone('Europe/Paris')).strftime('%z'))/100)
    else: # for local debug
        now = datetime.datetime.now()

    loop_until = last_submission_date or now
    last_submission_date = now

    liste = []

    table = soup.find("table")
    for resolution in table.find_all("tr"):
        elements = resolution.find_all("td")

        this_date = datetime.datetime.strptime(elements[0].decode_contents() + " " + elements[1].decode_contents().replace("h", ":"), '%d/%m/%y %H:%M')
        if this_date >= last_submission_date: continue
        if this_date < loop_until: break

        user = elements[2].find("a")["href"].split("/")[-1]
        probleme = elements[5].contents[-1].strip()[1:]

        discordUser = FindMT(user)
        if not discordUser: continue # on affiche que les utilisateurs du discord MT

        #ping_user = discordUser in solvedpbs_ping_settings
        ping_user=True
        try: the_user = bot.get_user(int(discordUser)) or await bot.fetch_user(int(discordUser))
        except NotFound: continue

        prefix = the_user.mention if ping_user else f"**{the_user.name}**`#{the_user.discriminator}`"

        liste.append(f"{prefix} a résolu le problème #{probleme} https://www.mathraining.be/problems/{PROBLEMS_MT[int(probleme)]} ! :clap:")

    for i in reversed(liste):
        await canalResolutions.send(i)

    await AopsCore.task(aclient)

##...
@bot.command(pass_context=True)
async def ping(ctx):
    await send_message(ctx,"Pong ! Ma latence est " + str(round(bot.latency * 1000)) + "ms.")

@bot.command(pass_context=True)
async def execute(ctx, *,code):
    if not str(ctx.author.id)=="690125478958333956":
        await send_message(ctx,"Vous n'avez pas les permissions pour faire cela.")
        return
    try:
        await send_message(ctx,f"```py\n{eval(code)}\n```")
    except Exception as e:
        await send_message(ctx,f"```py\n{e}\n```")

@bot.command(pass_context=True)
async def bakistan(ctx,nb=10):
    if nb>=10:
        nb=10
    for i in range(nb):
        await send_message(ctx,"Vive le bakistan ! :flag_la:")

@bot.command(pass_context=True)
async def spam(ctx,*,message):
    r=message.split()
    # test if r[0] is an integer
    try:
        nb=int(r[0])
        del r[0]
    except ValueError:
        nb=10
    if nb>=10:
        nb=10
    for i in range(nb):
        await send_message(ctx," ".join(r))

@bot.command(pass_context=True)
async def classement(ctx):
    mesg=await ctx.send("Chargement ...")
    users = sorted(ctx.guild.members, key=lambda x: x.joined_at)
    ids = []
    real_users=[]
    for user in users:
        if FindUser(user)!=0:
            ids.append(FindUser(user))
            real_users.append(user)
    scores=[]
    combi=[]
    geo=[]
    tn=[]
    alg=[]
    ef=[]
    ine=[]
    for id in ids:
        url="https://www.mathraining.be/users/"+str(id)
        async with aclient.get(url) as response: text = await response.text()
        soup = BeautifulSoup(text, "lxml")
        Infos=list(filter(None,[i.getText().strip() for i in soup.find_all('td', limit = 39)]))
        scores.append(Infos[4])
        combi.append(Infos[18])
        geo.append(Infos[20])
        tn.append(Infos[22])
        alg.append(Infos[24])
        ef.append(Infos[26])
        ine.append(Infos[28])
    # ask the user what domain to compare
    await mesg.delete()
    await send_message(ctx,"Quelle partie voulez-vous comparer ?\n1. Scores\n2. Combinatoire\n3. Géométrie\n4. Théorie des nombres\n5. Algèbre\n6. Équations fonctionelles\n7. Inégalités")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=30)
    except:
        await send_message(ctx,"Vous avez dépassé le temps imparti.")
        return
    if msg.content=="1":
        sorted_scores=sorted(scores,key=lambda n:-int(n))
        msg="```\n"
        for i in range(len(sorted_scores)):
            msg+=str(i+1)+" - "+str(real_users[scores.index(str(sorted_scores[i]))].name)+" - "+str(sorted_scores[i])+"\n"
            del real_users[scores.index(str(sorted_scores[i]))]
            del scores[scores.index(str(sorted_scores[i]))]
        await send_message(ctx,msg+"```")
    elif msg.content=="2":
        sorted_combi=sorted(combi,key=lambda n:-int(n.replace("%","").replace("-","0")))
        msg="```\n"
        for i in range(len(sorted_combi)):
            msg+=str(i+1)+" - "+str(real_users[combi.index(str(sorted_combi[i]))].name)+" - "+str(sorted_combi[i])+"\n"
            del real_users[combi.index(str(sorted_combi[i]))]
            del combi[combi.index(str(sorted_combi[i]))]
        await send_message(ctx,msg+"```")
    elif msg.content=="3":
        sorted_geo=sorted(geo,key=lambda n:-int(n.replace("%","").replace("-","0")))
        msg="```\n"
        for i in range(len(sorted_geo)):
            msg+=str(i+1)+" - "+str(real_users[geo.index(str(sorted_geo[i]))].name)+" - "+str(sorted_geo[i])+"\n"
            del real_users[geo.index(str(sorted_geo[i]))]
            del geo[geo.index(str(sorted_geo[i]))]
        await send_message(ctx,msg+"```")
    elif msg.content=="4":
        sorted_tn=sorted(tn,key=lambda n:-int(n.replace("%","").replace("-","0")))
        msg="```\n"
        for i in range(len(sorted_tn)):
            msg+=str(i+1)+" - "+str(real_users[tn.index(str(sorted_tn[i]))].name)+" - "+str(sorted_tn[i])+"\n"
            del real_users[tn.index(str(sorted_tn[i]))]
            del tn[tn.index(str(sorted_tn[i]))]
        await send_message(ctx,msg+"```")
    elif msg.content=="5":
        sorted_alg=sorted(alg,key=lambda n:-int(n.replace("%","").replace("-","0")))
        msg="```\n"
        for i in range(len(sorted_alg)):
            msg+=str(i+1)+" - "+str(real_users[alg.index(str(sorted_alg[i]))].name)+" - "+str(sorted_alg[i])+"\n"
            del real_users[alg.index(str(sorted_alg[i]))]
            del alg[alg.index(str(sorted_alg[i]))]
        await send_message(ctx,msg+"```")
    elif msg.content=="6":
        sorted_ef=sorted(ef,key=lambda n:-int(n.replace("%","").replace("-","0")))
        msg="```\n"
        for i in range(len(sorted_ef)):
            msg+=str(i+1)+" - "+str(real_users[ef.index(str(sorted_ef[i]))].name)+" - "+str(sorted_ef[i])+"\n"
            del real_users[ef.index(str(sorted_ef[i]))]
            del ef[ef.index(str(sorted_ef[i]))]
        await send_message(ctx,msg+"```")
    elif msg.content=="7":
        sorted_ine=sorted(ine,key=lambda n:-int(n.replace("%","").replace("-","0")))
        msg="```\n"
        for i in range(len(sorted_ine)):
            msg+=str(i+1)+" - "+str(real_users[ine.index(str(sorted_ine[i]))].name)+" - "+str(sorted_ine[i])+"\n"
            del real_users[ine.index(str(sorted_ine[i]))]
            del ine[ine.index(str(sorted_ine[i]))]
        await send_message(ctx,msg+"```")
    else:
        await send_message(ctx,"Erreur, veuillez réessayer.")
        
@bot.command(pass_context=True)
async def userinfo(ctx,user: discord.Member=None):
    if user==None:
        user=ctx.author
    # get info of discord account in an embed
    embed=discord.Embed(title=user.name, description=user.mention, color=0x00ff00)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Date de création", value=user.created_at, inline=True)
    embed.add_field(name="Roles", value=", ".join([r.name for r in user.roles]), inline=False)
    embed.add_field(name="Statut", value=user.status, inline=True)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def serverinfo(ctx):
    # get info of discord server in an embed
    embed=discord.Embed(title=ctx.guild.name, description=ctx.guild.name, color=0x00ff00)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="ID", value=ctx.guild.id, inline=True)
    embed.add_field(name="Date de création", value=ctx.guild.created_at, inline=True)
    embed.add_field(name="Nombre de membres", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Nombre de catégories", value=len(ctx.guild.categories), inline=True)
    embed.add_field(name="Nombre de salons", value=len(ctx.guild.channels), inline=True)
    embed.add_field(name="Nombre de rôles", value=len(ctx.guild.roles), inline=True)
    embed.add_field(name="Nombre de salons textuels", value=len([c for c in ctx.guild.channels if c.type==discord.ChannelType.text]), inline=True)
    embed.add_field(name="Nombre de salons vocaux", value=len([c for c in ctx.guild.channels if c.type==discord.ChannelType.voice]), inline=True)
    embed.add_field(name="Nombre de salons canaux", value=len([c for c in ctx.guild.channels if c.type==discord.ChannelType.category]), inline=True)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def ban(ctx,user: discord.Member=None,reason: str=None):
    #check highest role
    if ctx.author.top_role.position<=user.top_role.position:
        await send_message(ctx,"Vous n'avez pas la permission d'exécuter cette commande.")
        return
    # check permissions
    if not ctx.author.guild_permissions.ban_members:
        await send_message(ctx,"Vous n'avez pas la permission de bannir des membres.")
        return
    # check if user is specified
    if user==None:
        await send_message(ctx,"Veuillez spécifier un utilisateur.")
        return
    # check if user is not the bot
    if user==bot.user:
        await send_message(ctx,"Je ne peux pas me bannir.")
        return
    # ban user
    await user.ban(reason=reason)
    await send_message(ctx,"Utilisateur "+ user.name +" banni pour la raison suivante : "+reason)

@bot.command(pass_context=True)
async def kick(ctx,user: discord.Member=None,reason: str=None):
    #check highest role
    if ctx.author.top_role.position<=user.top_role.position:
        await send_message(ctx,"Vous n'avez pas la permission d'exécuter cette commande.")
        return
    # check permissions
    if not ctx.author.guild_permissions.kick_members:
        await send_message(ctx,"Vous n'avez pas la permission de kick des membres.")
        return
    # check if user is specified
    if user==None:
        await send_message(ctx,"Veuillez spécifier un utilisateur.")
        return
    # check if user is not the bot
    if user==bot.user:
        await send_message(ctx,"Je ne peux pas me kick.")
        return
    # kick user
    await user.kick(reason=reason)
    await send_message(ctx,"Utilisateur "+ user.name +" kick pour la raison suivante : "+reason)

@bot.command(pass_context=True)
async def clear(ctx,amount: int=None):
    # check if amount is specified
    if amount==None:
        await send_message(ctx,"Veuillez spécifier un nombre de messages à supprimer.")
        return
    # check if amount is between 1 and 100
    if amount<1 or amount>100:
        await send_message(ctx,"Veuillez spécifier un nombre entre 1 et 100.")
        return
    # check permissions
    if not ctx.author.guild_permissions.manage_messages:
        await send_message(ctx,"Vous n'avez pas la permission de supprimer des messages.")
        return
    # delete messages
    await ctx.channel.purge(limit=amount)
    message=await send_message(ctx,"Suppression de "+str(amount)+" messages.")
    await asyncio.sleep(3)
    await message.delete()

# BETA : non relu à la main, généré par GitHub Copilot
'''
@bot.command(pass_context=True)
async def wolframalpha(ctx,query: str):
    # get query
    if query==None:
        await send_message(ctx,"Veuillez spécifier une requête.")
        return
    # get result with wolframapha.com api
    url="https://api.wolframalpha.com/v1/result?appid=LJXQXQ-XQXQXQXQXQ&i="+query
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data=await resp.json()
    # check if result is empty
    if data["queryresult"]["@success"]=="false":
        await send_message(ctx,"Aucun résultat.")
        return
    # send result
    await send_message(ctx,data["queryresult"]["pod"][1]["subpod"]["plaintext"])'''

@bot.command(pass_context=True)
async def meme(ctx):
    import random
    # get a random meme as an image
    url="https://some-random-api.ml/meme"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data=await resp.json()
    # send the image
    await send_message(ctx,data["image"])
@bot.command(pass_context=True)
async def botinfo(ctx):
    # get bot info
    embed=discord.Embed(title="Informations sur le bot", description="Informations sur le bot", color=0x00ff00)
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name="Nom", value=bot.user.name, inline=True)
    embed.add_field(name="ID", value=bot.user.id, inline=True)
    embed.add_field(name="Date de création", value=bot.user.created_at, inline=True)
    embed.add_field(name="Nombre de serveurs", value=len(bot.guilds), inline=True)
    embed.add_field(name="Nombre de membres", value=len(set(bot.get_all_members())), inline=True)
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def baron(ctx):
    emoji="<:praige:938897124299509801>"
    for i in range(10):
        await send_message(ctx,"Vive le baron fou ! "+emoji)

@bot.command(pass_context=True)
async def calc(ctx,*,op):
    op=op.upper()
    for i in op:
        if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            await send_message(ctx,"Erreur, merci de rééssayer sans utiliser de lettres")
            return
    # if result is too big raise an error
    a=eval(op)
    await send_message(ctx,a)

@bot.command(pass_context=True)
async def comparepbs(ctx,user1:MTid=None,user2:MTid=None):
    if user1==None:
        await send_message(ctx,"Merci de spécifier un utilisateur à comparer")
        return
    if user2==None:
        user2=await MTid.me(ctx)
    if user1==user2:
        await send_message(ctx,"Pourquoi se comparer avec soi-même ?")
        return
    liste1=[]
    liste2=[]
    async with aclient.get(f"https://www.mathraining.be/users/{user1}") as resp : response1 = await resp.text()
    async with aclient.get(f"https://www.mathraining.be/users/{user2}") as resp : response2 = await resp.text()
    with open("Problems.txt") as f:
        text=f.read().split("\n")
    for i in text:
        namepb="#"+i[:4]
        a=namepb in response1
        b=namepb in response2
        if a and b:
            continue
        elif a:
            liste1.append(namepb)
        elif b:
            liste2.append(namepb)
    soup1 = BeautifulSoup(response1, "lxml")
    Infos1=list(filter(None,[i.getText().strip() for i in soup1.find_all('td', limit = 39)]))  
    soup2 = BeautifulSoup(response2, "lxml")
    Infos2=list(filter(None,[i.getText().strip() for i in soup2.find_all('td', limit = 39)]))
    await send_message(ctx,"```\nProblèmes résolus uniquement par "+Infos1[0]+" : "+" ".join(liste1)+"\n\nProblèmes résolus uniquement par "+Infos2[0]+" : "+" ".join(liste2)+"```")

# restart bot
@bot.command(pass_context=True)
async def restart(ctx):
    import os
    import sys
    # check if user is owner
    if ctx.author.id!=690125478958333956:
        await send_message(ctx,"Vous n'avez pas la permission de redémarrer le bot.")
        return
    # restart bot
    await send_message(ctx,"Redémarrage du bot...")
    await bot.logout()
    os.execv(sys.executable, ['python3'] + sys.argv)

# retourne les résolutions récentes sur Mathraining
@bot.command(pass_context=True)
async def problems(ctx):
    # get problems
    async with aclient.get("https://www.mathraining.be/solvedproblems") as resp : response = await resp.text()
    soup = BeautifulSoup(response, "lxml")
    # get problems
    problems=list(filter(None,[i.getText().strip() for i in soup.find_all('td', limit = 72)]))
    # send problems
    message="```\nProblèmes récemment résolus : \n\nDate     Heure  Utilisateur         Domaine   Niveau Problème"
    for i in range(len(problems)):
        if i%6==0:
            message+="\n"
        if i%6==0:
            message+=problems[i]+" "
        elif i%6==1:
            message+=problems[i]+" "*(7-len(problems[i]))
        elif i%6==2:
            message+=problems[i]+" "*(20-len(problems[i]))
        elif i%6==3:
            message+=problems[i]+" "*(10-len(problems[i]))
        elif i%6==4:
            message+=problems[i]+" "
        else:
            message+=problems[i]
    message+="\n```"
    await send_message(ctx,message)    

# search user
@bot.command(pass_context=True)
async def search(ctx,*,user):
    import unidecode
    await mt_connexion(aclient)
    #call js function showAllUsers() on the web page
    resp=await aclient.get(f'https://www.mathraining.be/discussions/new')
    #get the html of the page



    # get option where content is user
    soup = BeautifulSoup(await resp.text(), "lxml")
    options=soup.find_all('option')
    users=[]
    user=unidecode.unidecode(user).lower()
    for i in options:
        if user in unidecode.unidecode(i.string.lower()):
            users.append(i)
    if len(users)==0:
        await send_message(ctx,"Cet utilisateur n'existe pas")
        return
    # ask which user he want to display
    # check if length is greater than one
    if len(users)>1:
        await send_message(ctx,"Quel utilisateur voulez-vous afficher ?\n```\n"+"\n".join([f"{i} {users[i].string}" for i in range(len(users))])+"\n```")
        # get user
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            msg = await bot.wait_for('message', check=check, timeout=30)
        except:
            await send_message(ctx,"Vous avez dépassé le temps imparti.")
            return
        if not msg.content.isdigit():
            await send_message(ctx,"Vous devez entrer un nombre")
            return
        if int(msg.content)>=len(users):
            await send_message(ctx,"Vous devez entrer un nombre inférieur à "+str(len(users)))
            return
        user=users[int(msg.content)]['value']
        # call info function
    else:
        user=users[0]['value']
    await info(ctx,user)

# add an emoji to the server's one or convert an image to emoji
@bot.command(pass_context=True)
async def emoji(ctx,*,emoji):
    # check if user is owner
    if ctx.author.id!=690125478958333956:
        await send_message(ctx,"Vous n'avez pas la permission d'ajouter un emoji.")
        return
    # check if emoji is an image
    if emoji.endswith(".png") or emoji.endswith(".jpg") or emoji.endswith(".jpeg"):
        # get image
        async with aclient.get(emoji) as resp : response = await resp.read()
        # convert image to emoji
        await ctx.send(file=discord.File(BytesIO(response), "emoji.png"))
        await send_message(ctx,"Emoji ajouté !")
        return
    # check if emoji is a string
    if len(emoji)>=2:
        # check if emoji is already in the server
        if emoji in [i.name for i in ctx.guild.emojis]:
            await send_message(ctx,"Cet emoji existe déjà")
            return
        # add emoji
        await ctx.guild.create_custom_emoji(name=emoji, image=await aclient.get(emoji))
        await send_message(ctx,"Emoji ajouté !")
        return
    # check if emoji is a number
    if emoji.isdigit():
        # check if emoji is already in the server
        if emoji in [i.id for i in ctx.guild.emojis]:
            await send_message(ctx,"Cet emoji existe déjà")
            return
        # add emoji
        await ctx.guild.create_custom_emoji(name=emoji, image=await aclient.get(f"https://cdn.discordapp.com/emojis/{emoji}.png"))
        await send_message(ctx,"Emoji ajouté !")
        return
    # check if emoji is a url
    if emoji.startswith("https://cdn.discordapp.com/emojis/"):
        # check if emoji
        if emoji in [i.id for i in ctx.guild.emojis]:
            await send_message(ctx,"Cet emoji existe déjà")
            return
        # add emoji
        await ctx.guild.create_custom_emoji(name=emoji, image=await aclient.get(emoji))
        await send_message(ctx,"Emoji ajouté !")
        return
    # check if emoji is a discord emoji
    if emoji.startswith("<:"):
        # check if emoji is already in the server
        if emoji in [i.name for i in ctx.guild.emojis]:
            await send_message(ctx,"Cet emoji existe déjà")
            return
        # add emoji
        await ctx.guild.create_custom_emoji(name=emoji, image=await aclient.get(f"https://cdn.discordapp.com/emojis/{emoji[2:-1]}.png"))
        await send_message(ctx,"Emoji ajouté !")
        return

    await send_message(ctx,"Vous devez entrer un emoji valide")

# send a list with the members of the country laos (id=97)
@bot.command(pass_context=True)
async def membres(ctx,id=97):
    # to verify
    url='https://www.mathraining.be/users?country='+str(id)+'&page=1&title=0'
    async with aclient.get(url) as response: t = await response.text()
    try:
        ind=t.index("pagination")
        while t[ind:ind+5]!="</ul>":
            if t[ind:ind+5]=="</li>" and t[ind+5:ind+10]!="</ul>":
                maxi=ind
            ind+=1
        nb_pages=int(t[maxi-7:maxi-4].replace(">","").replace(">","").replace("\"",""))
    except Exception as e:
        nb_pages=1
    message=f"```Membres du {await get_pays_name(id)} :\n\n"
    for i in range(1,nb_pages+1):
        url='https://www.mathraining.be/users?country='+str(id)+'&page='+str(i)+'&title=0'
        resp = await aclient.get(url)
        soup = BeautifulSoup(await resp.text(), "lxml")
        tds=soup.find_all("td")
        for j in range(len(tds)):
            try:
                if "name" in tds[j]["id"]:
                    message+=tds[j].string+"\n"
            except KeyError:
                continue
            except:
                for i in tds[j].children:
                    for j in i.children:
                        message+=j.string
                message+="\n"
    message+="```"
    await send_message(ctx,message)

# execute a command in the cmd if user is owner
@bot.command(pass_context=True)
async def cmd(ctx,*,cmd):
    import subprocess
    if ctx.author.id!=690125478958333956:
        await send_message(ctx,"Vous n'avez pas la permission d'executer une commande.")
        return
    await send_message(ctx,"```"+subprocess.check_output(cmd,shell=True).decode("utf-8").replace("`","'")+"```")

@bot.command(pass_context=True)
async def screenfetch(ctx):
    import subprocess
    if ctx.author.id!=690125478958333956:
        await send_message(ctx,"Vous n'avez pas la permission d'executer une commande.")
        return
    await send_message(ctx,"```"+subprocess.check_output("screenfetch -N -D debian",shell=True).decode("utf-8").replace("`","'")+"```")

async def send_message(ctx,message):
    # if message is shorter than 2000 characters send it
    message=str(message)
    if len(message)<=2000:
        k= await ctx.send(message)
        return k
    # else send a .txt with the content of the message
    with open("message.txt","w") as f:
        f.write(message.replace("`",""))
    await ctx.send(file=discord.File("message.txt"))

try: bot.run(options['token']) #Token MT
except LoginFailure as e: print(e)
else: run(aclient.close())