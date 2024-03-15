import requests
from bs4 import BeautifulSoup
import json
from datetime import date as Date
from datetime import datetime as DateTime
import discord


# PARTIE 1: Récupérer les liens des rewards

#Headers pour simuler une requête d'un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


# L'URL de la page à scraper
url = 'https://monopolygo.wiki/latest-reward-links'

# Effectue une requête GET pour récupérer le contenu de la page
reponse = requests.get(url, headers=headers)

# Liste pour recueillir les données
data = []

# Vérifie si la requête a réussi
if reponse.status_code == 200:
    # Parse le contenu HTML de la page
    soup = BeautifulSoup(reponse.content, 'html.parser')

    # Sélectionne les divs qui correspondent au style donné
    divs = soup.find_all('div', style="display: flex; margin-bottom: 1em; justify-content: space-between; padding:1em;background-color:#f4f4f4;border-radius:5px;")

    for div in divs:
        # Nom
        nom = div.find('span').text
        # Date
        date = div.find('span', style="opacity:0.5;").text
        # Sépare la date en date de début et date de fin et retire ce qu'il y'a après la virgule
        date_debut, date_fin = date.split(' - ')
        date_fin = date_fin.split(',')[0]
        # Nombre de rewards
        rewards = div.find('span', style="display: flex;gap: 10px;align-items: center;").text
        # Remplacer le X par 🎲
        rewards = rewards.replace('✕', '🎲')
        # Lien
        lien = div.find('a')['href']
        # Ajoute les données à la liste
        data.append({
            "Nom": nom,
            "Date debut": date_debut,
            "Date fin": date_fin,
            "Rewards": rewards,
            "Lien": lien
        })

        # Écrit les données dans un fichier JSON
        with open('reward_links.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
else:
    print("Erreur lors de la récupération de la page.")
    print ("Code d'erreur:", reponse.status_code)



# PARTIE 2: Recuperer les special events
    #Date d'aujourd'hui format : MMM DD YYYY
today = Date.today().strftime("%b %d %Y").lower()
month, day, year = today.split(' ')

#Headers pour simuler une requête d'un navigateur
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#url de la page
url = f'https://monopolygo.wiki/todays-events-{month}-{day}-{year}'

# Effectue une requête GET pour récupérer le contenu de la page
reponse = requests.get(url, headers=headers)

# Liste pour recueillir les données
data = []

# Vérifie si la requête a réussi

if reponse.status_code == 200:
    soup = BeautifulSoup(reponse.content, 'html.parser')
    
    # Trouve tous les 'div' avec la classe 'event-container'
    events = soup.find_all('div', class_='event-container')
    
    for event in events:
        # Nom de l'événement
        event_name = event.find('span', style="font-weight:bold;").text
        
        # Trouve les dates et heures de début et de fin
        dates = event.find_all('span', class_='local-date')
        start_datetime = dates[0]['data-date']
        end_datetime = dates[1]['data-date']

        # Conversion des timestamps UNIX (si nécessaire)
        start_date_time = DateTime.fromtimestamp(float(start_datetime)).strftime('%d/%m/%Y %H:%M:%S')
        end_date_time = DateTime.fromtimestamp(float(end_datetime)).strftime('%d/%m/%Y %H:%M:%S')

        
        # Trouve tous les éléments 'span'
        spans = event.find_all('span')
        for span in spans:
            # Vérifie si le span contient un élément 'b' avec le texte 'Duration:'
            if span.find('b', string='Duration:'):
                # Si trouvé, extrait la durée
                duration = span.text.split("Duration:")[1].strip()
                break
        else:
            # Si aucun span contenant 'Duration:' n'est trouvé
            duration = "Not specified"

        
        # Ajoute les informations à la liste 'data'
        data.append({
            'Event Name': event_name,
            'Start DateTime': start_date_time,
            'End DateTime': end_date_time,
            'Duration': duration
        })

    # Sauvegarde des données dans un fichier JSON
    with open('special_events.json', 'w') as file:
        json.dump(data, file, indent=4)
else:
    print(f"Failed to retrieve the page, status code: {reponse.status_code}")



# Partie 3: Générer les messages Discord
    
# Initialiser le client Discord
TOKEN = 'YOUR TOKEN HERE'
CHANNEL_ID_REWARD = 00000000
CHANNEL_ID_EVENT = 00000000

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True
intents.guilds = True
intents.reactions = True

client = discord.Client(intents=intents)

# Lire les données des fichiers JSON
with open('reward_links.json', 'r', encoding='utf-8') as f:
    reward_data = json.load(f)

with open('special_events.json', 'r', encoding='utf-8') as file:
    event_data = json.load(file)


# Initialiser un message formaté pour Discord
discord_message_rewards = "**🎉 Liens dés ! 🎉**\n\n"
# Générer les messages Discord
for reward in reward_data:
    discord_message_rewards += (
        f"**Date de fin:** {reward['Date fin']}\n"
        f"**Récompenses:** {reward['Rewards']}\n"
        f"**Lien pour réclamer:** [Cliquez ici]({reward['Lien']})\n\n"
    )



# Initialiser un message formaté pour Discord
discord_message_events = "**🌟 Événements Spéciaux à Venir ! 🌟**\n\n"

# Générer le message pour chaque événement
for event in event_data:
    discord_message_events += (
        f"**Événement:** {event['Event Name']}\n"
        f"**Début:** {event['Start DateTime']}\n"
        f"**Fin:** {event['End DateTime']}\n"
        f"**Durée:** {event['Duration']}\n\n"
    )

#Connecter
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    # Envoyer les message sur Discord
    channel = client.get_channel(CHANNEL_ID_REWARD)
    await channel.send(discord_message_rewards)
    channel = client.get_channel(CHANNEL_ID_EVENT)
    await channel.send(discord_message_events)

client.run(TOKEN)