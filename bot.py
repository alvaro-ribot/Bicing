# Importa el modul corresponent al calcul sobre el graf i la informacio del proyecte.
import data

# Importa l'API pel tractament d'arxius bytes, com ara imatges.
from io import BytesIO

# Importa el modul per el tractament de dades en taules DataFrame.
import pandas as pd
from pandas import DataFrame

# Importa el modul per l'us de grafs.
import networkx as nx

# Importa l'API de Telegram, i funcions per l'us del bot.
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

# Importa el modul per el seguiment de la sessio del bot.
import logging

# Configurem el seguiment de la sessio del bot.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


# Diccionari amb les funcions que pot executar el bot i una breu descripcio de cadascuna d'elles.
commands = {"start": "Inicia la conversa amb el bot", "help": "Ensenya la llista de comandes d'aquest bot",
            "authors": "Coneix els autors d'aquest projecte",
            "graph": "Seguit de la distància que desitgis, es genera el graf geomètric de Barcelona",
            "nodes": "Consulta quantes estacions de bici tens a la teva disposició",
            "edges": "Consulta quants trajectes possibles tens a la teva disposició, segons els teus requiriments mètrics",
            "components": "Consultes quantes illes ciclistes hi ha segons els teus requeriments mètrics",
            "plotgraph": "Mira un mapa de les parades de bici i els trajectes entre elles",
            "route": "Consulta la ruta més ràpida entre dos direccions donades, separades amb una coma"}


# L'argument "user_data" fa referencia a un diccionari amb les dades que es guardaran per l'usuari,
# aixi doncs es passaran el graf i la taula de dades sobre les que s'executen la resta de comandes.


# Primera funcio, serveix per activar el bot. Envia un breu missatge de benvinguda.
def start(bot, update, user_data):
    # Missatje de benvinguda.
    message = "Hola! Soc el bot Bicing. Amb /help pots veure una llista amb les comandes disponibles."
    bot.send_message(chat_id=update.message.chat_id, text=message)

    # Obtenim les dades del mòdul extern i guardem una DataFrame amb aquestes dades.
    user_data['bicing'] = data.dades_bicing()

    # Creem el graf geometric de les estacions amb distancia inicial per defecte d'1km.
    user_data['Graph'] = data.geometric_graph(1000, user_data['bicing'])


# Funcio d'ajuda a l'usuari que disposa les possibles comandas del bot.
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Aquestes són les commandes disponibles:")
    # Variable de tipus string de varies linies per composar el missatge amb un format adient.
    message = """"""
    for action, description in commands.items():
        command = '/' + action + ' - ' + description + '\n'
        message += command
    bot.send_message(chat_id=update.message.chat_id, text=message)


# Funcio que escriu el nom dels autors del projecte i els seus correus.
def authors(bot, update):
    message = """Aquest bot ha estat creat per Álvaro Ribot Barrado i Luis Sierra Muntané\n
    alvaro.ribot@est.fib.upc.edu\n
    luis.sierra@est.fib.upc.edu"""
    bot.send_message(chat_id=update.message.chat_id, text=message)


# Funcio que construeix el graf geometric, prenent com argument la distancia maxima del graf,
# mitjançant la funcio externa eficient de complexitat O(V + E).
def graph(bot, update, args, user_data):
    try:
        # Comprovem que tenim un nombre correcte d'arguments.
        if len(args) == 1:
            distance = float(args[0])
            # Construim el graf amb la distancia que l'usuari demana.
            user_data['Graph'] = data.geometric_graph(distance, user_data['bicing'])
            message = 'Graf geomètric actualitzat exitosament! (Nova distància = %d metres)' % (distance)
            bot.send_message(chat_id=update.message.chat_id, text=message)
        else:
            message = "Nombre invalid d'arguments (s'han donat %d i s'esperen 1)" % (len(args))
            bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funcio que ens retorna el nombre de nodes del nostre graf.
def nodes(bot, update, user_data):
    try:
        # Obtenim el nombre de nodes amb la funcio externa.
        n = data.get_nodes(user_data['Graph'])
        message = "Aquest nombre d'estacions estan a la teva disposició: %d" % (n)
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funcio que ens retorna el nombre d'arestes del nostre graf.
def edges(bot, update, user_data):
    try:
        # Obtenim el nombre d'arestes amb la funcio externa.
        m = data.get_edges(user_data['Graph'])
        message = "Aquest nombre de trajectes són viables sota la teva configuració: %d" % (m)
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funcio que ens retorna el nombre de components connexes del nostre graf.
def components(bot, update, user_data):
    try:
        # Obtenim el nombre de components connexes amb la funcio externa.
        c = data.connex_components(user_data['Graph'])
        message = "El nombre de zones de bicicletes Bicing sota les teves restriccions és: %d" % (c)
        bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funcio que mostra el mapa de la ciutat amb les estacions de bici i les arestes que les connecten.
def plotgraph(bot, update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Si us plau, espera mentre es produeix la imatge...")
    try:
        # Creem un objecte de tipus "BytesIO" per guardar la imatge del graf.
        bio = BytesIO()
        # Creem i guardem la imatge amb una funcio externa per seguidament enviar-la.
        imatge = data.plot_graph(user_data['Graph'])
        imatge.save(bio, 'PNG')
        bio.seek(0)
        bot.send_photo(chat_id=update.message.chat_id, photo=bio)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funcio que retorna la ruta entre dos punts de la ciutat, prenent com arguments dos direccions.
# Despres es converteixen les direccions en coordenades i es calcula la ruta mes rapida amb la funcio externa.
def route(bot, update, args, user_data):
    try:
        message = "Calculant la ruta més ràpida..."
        bot.send_message(chat_id=update.message.chat_id, text=message)
        # Comprovem que tenim un nombre correcte d'arguments.
        if len(args) > 1: 
            # Canviem el missatge per eliminar el "/route".
            address_info = update.message.text[7:]
            # Obtenim la millor ruta per fer el trajecte, guardant-la com imatge si ho fem amb exit.
            imatge = data.route(user_data['Graph'], address_info)
            if imatge == None:
                # En aquest cas no s'ha trobat la direccio demanada i es retorna un avis a l'usuari.
                message = "Adreça no trobada, assegura't que tens l'adreça ben escrita"
                bot.send_message(chat_id=update.message.chat_id, text=message)
            else:
                # Quan es troben las direccions es retorna un mapa de la ruta mes rapida entre elles.
                # Creem un objecte de tipus "BytesIO" per guardar la imatge de la ruta en el graf.
                bio = BytesIO()
                # Guardem la imatge amb una funcio externa per seguidament enviar-la.
                imatge.save(bio, 'PNG')
                bio.seek(0)
                bot.send_photo(chat_id=update.message.chat_id, photo=bio)
        else:
            message = "Sembla que t'ha faltat introduir una direcció...\nTorna-ho a intentar."
            bot.send_message(chat_id=update.message.chat_id, text=message)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=update.message.chat_id, text='💣')


# Funcio que es crida quan es produeixen errors de sessio, enviant un avis.
def error(update, bot):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


###########################################################################################


# Codi d'entrada que guardem en una variable per poder accedir al bot.
TOKEN = open('token.txt').read().strip()

# Crea els objectes per treballar amb Telegram.
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Indica que quan el bot rep una ordre donada s'executi la seva funcio corresponent.
dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args=True, pass_user_data=True))
dispatcher.add_handler(CommandHandler('nodes', nodes, pass_user_data=True))
dispatcher.add_handler(CommandHandler('edges', edges, pass_user_data=True))
dispatcher.add_handler(CommandHandler('components', components, pass_user_data=True))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph, pass_user_data=True))
dispatcher.add_handler(CommandHandler('route', route, pass_args=True, pass_user_data=True))

# Avis de qualsevol error que te lloc en una sessio del bot.
dispatcher.add_error_handler(error)

# Encen el bot.
updater.start_polling()
