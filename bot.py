# Importa el mòdul corresponent al càlcul sobre el graf i la informació del proyecte.
import data

# Importa l'API pel tractament d'arxius bytes, com ara imatges.
from io import BytesIO

# Importa el mòdul per el tractament de dades en taules DataFrame.
import pandas as pd
from pandas import DataFrame

# Importa el mòdul per l'us de grafs.
import networkx as nx

# Importa l'API de Telegram, i funcions per l'ús del bot.
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

# Importa el mòdul per el seguiment de la sessió del bot.
import logging

# Configurem el seguiment de la sessió del bot.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


# Diccionari amb les funcions que pot executar el bot i una breu descripció de cadascuna d'elles.
commands = {"start": "Inicia la conversa amb el bot", "help": "Ensenya la llista de comandes d'aquest bot",
            "authors": "Coneix els autors d'aquest projecte",
            "graph": "Seguit de la distància que desitgis, es genera el graf geomètric de Barcelona",
            "nodes": "Consulta quantes estacions de bici tens a la teva disposició",
            "edges": "Consulta quants trajectes possibles tens a la teva disposició, segons els teus requiriments mètrics",
            "components": "Consultes quantes illes ciclistes hi ha segons els teus requeriments mètrics",
            "plotgraph": "Mira un mapa de les parades de bici i els trajectes entre elles",
            "route": "Consulta la ruta més ràpida entre dos direccions donades"}


# L'argument "user_data" fa referència a un diccionari amb les dades que es guardaran per l'usuari,
# així doncs es passaran el graf i la taula de dades sobre les que s'executen la resta de comandes.


# Primera funció, serveix per activar el bot. Envia un breu missatge de benvinguda.
def start(bot, update, user_data):
    # Missatje de benvinguda.
    message = "Hola! Soc el bot Bicing. Amb /help pots veure una llista amb les comandes disponibles."
    bot.send_message(chat_id=update.message.chat_id, text=message)

    # Guardem les següents dades en el "user_data" donat que es fan servir en altres commandes.
    # Direcció url de la pàgina de Bicing amb informació sobre bicis i parades.
    user_data['url'] = 'https://api.bsmsa.eu/ext/api/bsm/gbfs/v2/en/station_information'

    # Llegim les dades de l'url i construïm una DataFrame amb aquesta dades.
    user_data['bicing'] = DataFrame.from_records(pd.read_json(user_data['url'])['data']['stations'], index='station_id')

    # Creem el graf geomètric de les estacions amb distància inicial per defecte d'1km.
    user_data['Graph'] = data.geometric_graph(1000, user_data['bicing'])


# Funció d'ajuda a l'usuari que disposa les possibles comandas del bot.
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Aquestes són les commandes disponibles:")
    # Variable de tipus string de varies línies per composar el missatge amb un format adient.
    message = """"""
    for action, description in commands.items():
        command = '/' + action + ' - ' + description + '\n'
        message += command
    bot.send_message(chat_id=update.message.chat_id, text=message)


# Funció que escriu el nom dels autors del projecte i els seus correus.
def authors(bot, update):
    message = """Aquest bot ha estat creat per Álvaro Ribot Barrado i Luis Sierra Muntané\n
    alvaro.ribot@est.fib.upc.edu\n
    luis.sierra@est.fib.upc.edu"""
    bot.send_message(chat_id=update.message.chat_id, text=message)


# Funció que construeix el graf geomètric, prenent com argument la distància màxima del graf,
# mitjançant la funció externa eficient de complexitat O(V + E).
def graph(bot, update, args, user_data):
    try:
        # Comprovem que tenim un nombre correcte d'arguments.
        if len(args) == 1:
            distance = float(args[0])
            # Construïm el graf amb la distància que l'usuari demana.
            user_data['Graph'] = data.geometric_graph(distance, user_data['bicing'])
            message = 'Graf geomètric actualitzat exitosament! (Nova distància = %d metres)' % (distance)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            message = "Nombre invalid d'arguments (s'han donat %d i s'esperen 1)" % (len(args))
            bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funció que ens retorna el nombre de nodes del nostre graf.
def nodes(bot, update, user_data):
    try:
        # Obtenim el nombre de nodes amb la funció externa.
        n = data.get_nodes(user_data['Graph'])
        message = "Aquest nombre d'estacions estan a la teva disposició: %d" % (n)
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funció que ens retorna el nombre d'arestes del nostre graf.
def edges(bot, update, user_data):
    try:
        # Obtenim el nombre d'arestes amb la funció externa.
        m = data.get_edges(user_data['Graph'])
        message = "Aquest nombre de trajectes són viables sota la teva configuració: %d" % (m)
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funció que ens retorna el nombre de components connexes del nostre graf.
def components(bot, update, user_data):
    try:
        # Obtenim el nombre de components connexes amb la funció externa.
        c = data.connex_components(user_data['Graph'])
        message = "El nombre de zones de bicicletes Bicing sota les teves restriccions és: %d" % (c)
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funció que mostra el mapa de la ciutat amb les estacions de bici i les arestes que les connecten.
def plotgraph(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Si us plau, espera mentre es produeix la imatge...")
    try:
        # Creem un objecte de tipus "BytesIO" per guardar la imatge del graf.
        bio = BytesIO()
        # Creem i guardem la imatge amb una funció externa per seguidament enviar-la.
        imatge = data.plot_graph(user_data['Graph'])
        imatge.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(chat_id=update.message.chat_id, photo=bio)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funció que retorna la ruta entre dos punts de la ciutat, prenent com arguments dos direccions.
# Després es converteixen les direccions en coordenades i es calcula la ruta més ràpida amb la funció externa.
def route(bot, update, args, user_data):
    try:
        # Canviem el missatge per eliminar el "/route".
        address_info = update.message.text[7:]
        # Obtenim amb la funció externa el temps que es triga en fer el trajecte.
        time = data.ruta(address_info)
        if time == -1:
            # En aquest cas no s'ha trobat la direcció demanada i es retorna un avís a l'usuari.
            message = "Adreça no trobada, assegura't que tens l'adreça ben escrita"
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            # Quan es troben las direccions es retorna un mapa de la ruta més ràpida entre elles.
            # Creem un objecte de tipus "BytesIO" per guardar la imatge de la ruta en el graf.
            bio = BytesIO()
            # Creem i guardem la imatge amb una funció externa per seguidament enviar-la.
            imatge = data.plot_route(user_data['Graph'])
            imatge.save(bio, 'PNG')
            bio.seek(0)
            bot.send_photo(chat_id=update.message.chat_id, photo=bio)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funció que es crida quan es produeixen errors de sessió, enviant un avís.
def error(update, bot):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


###########################################################################################


# Codi d'entrada que guardem en una variable per poder accedir al bot.
TOKEN = open('token.txt').read().strip()

# Crea els objectes per treballar amb Telegram.
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Indica que quan el bot reb una ordre donada s'executi la seva funció corresponent.
dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args=True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', route, pass_args=True))

# Avís de qualsevol error que té lloc en una sessió del bot.
dispatcher.add_error_handler(error)

# Encén el bot.
updater.start_polling()
