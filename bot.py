# Importa el módulo correspondiente a el cálculo sobre el grafo y la información del proyecto.
import data

# Importa la API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

# Lista de funciones que puede ejecutar el bot.

# Primera función, sirve para activar el bot.
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola! Soc el bot Bicing.")


# Función para disponer las posibles comandas del bot.
def help(bot, update):
	help_text = 
	bot.send_message(chat_id=update.message.chat_id, text="Aquestes són les commandes disponibles: /start /help /")
	for command in commands:
		print()

# Función que escribe el nombre de los autores del proyecto.
def authors(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Aquest bot ha estat creat per Álvaro Ribot Barrado i Luis Sierra Muntané")

# Función que construye el grafo geométrico, tomando como argumento la distancia. Llama a la función
def graph(bot, update, args):
	try:
		distance = float(args[0])
		data.graph()
	except Exception as e:
		print(e)
		bot.send_message(chat_id=update.message.chat_id, text='💣')

# Función que nos da los nodos de nuestro grafo
def nodes(bot, update):
	missatge = "Aquestes estacions estan a la teva disposició:"
	bot.send_message(chat_id=update.message.chat_id, text=missatge)

# Función que nos da las aristas de nuestro grafo
def edges(bot, update):
	missatge = 
	bot.send_message(chat_id=update.message.chat_id, text=missatge)

#
def components(bot, update):

#
def plotgraph(bot, update):

# Función de ruta entre dos puntos de la ciudad.
def route(bot, update, args):
	try:
		while args[i] !=
		source = args[0]
		target = args[1]



###########################################################################################


# Código de entrada que guardamos en una variable para poder acceder al bot.
TOKEN = open('token.txt').read().strip()

# Crea los objectos para trabajar con Telegram.
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Indica que cuando el bot reciba una orden dada se ejecute su función correspondiente.
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('authors', authors))
dispatcher.add_handler(CommandHandler('graph', graph, pass_args=True))
dispatcher.add_handler(CommandHandler('nodes', nodes))
dispatcher.add_handler(CommandHandler('edges', edges))
dispatcher.add_handler(CommandHandler('components', components))
dispatcher.add_handler(CommandHandler('plotgraph', plotgraph))
dispatcher.add_handler(CommandHandler('route', route, pass_args=True))

# Enciende el bot
updater.start_polling()
