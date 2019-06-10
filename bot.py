# Importa el módulo correspondiente a el cálculo sobre el grafo y la información del proyecto.
import data

# Importa el módulo de la librería estándar para obtener información temporal. 
import datetime

# Importa la API de Telegram
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

'''
# Creamos el grafo geométrico de las estaciones con distancia estándar 1km.
G = data.geometric_graph(1000)
'''

# Lista de funciones que puede ejecutar el bot.

commands = ["start", "help", "authors", "graph", "nodes", "edges", "components", "plotgraph", "route"]

# Primera función, sirve para activar el bot. Da un breve mensaje de bienvenida.
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hola! Soc el bot Bicing.")


# Función para disponer las posibles comandas del bot.
def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Aquestes són les commandes disponibles:")
	# String de varias líneas para componer el mensaje.
	message = """"""
	for action in commands:
		command = '/' + action + '\n'
		message += command
	bot.send_message(chat_id=update.message.chat_id, text=message)


# Función que escribe el nombre de los autores del proyecto.
def authors(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Aquest bot ha estat creat per Álvaro Ribot Barrado i Luis Sierra Muntané")


# Función que construye el grafo geométrico, tomando como argumento la distancia del grafo. Llama a la función
def graph(bot, update, args):
	try:
		distance = float(args[0])
	except Exception as e:
		print(e)
		bot.send_message(chat_id=update.message.chat_id, text='💣')


# Función que nos da el número de nodos de nuestro grafo.
def nodes(bot, update):
	try:
		# Obtenemos el número de nodos con la función externa.
		n = data.get_nodes()
		message = "Aquest nombre d'estacions estan a la teva disposició:"
		bot.send_message(chat_id=update.message.chat_id, text=message)
		bot.send_message(chat_id=update.message.chat_id, text=str(n))
	except Exception as e:
		print(e)
		bot.send_message(chat_id=update.message.chat_id, text='💣')


# Función que nos da el número de aristas de nuestro grafo.
def edges(bot, update):
	try:
		# Obtenemos el número de aristas con la función externa.
		n = data.get_edges()
		message = "Aquest nombre de trajectes són viables sota la teva configuració:"
		bot.send_message(chat_id=update.message.chat_id, text=message)
		bot.send_message(chat_id=update.message.chat_id, text=str(n))
	except Exception as e:
		print(e)
		bot.send_message(chat_id=update.message.chat_id, text='💣')


# Función que nos da el número de componentes conexas de nuestro grafo.
def components(bot, update):
	try:
		n = data.connex_components()
		message = "The number of bicycle zones under your restrictions is:"
		bot.send_message(chat_id=update.message.chat_id, text=message)
		bot.send_message(chat_id=update.message.chat_id, text=n)
	except Exception as e:
		print(e)
		bot.send_message(chat_id=update.message.chat_id, text='💣')


# Función que muestra el mapa de la ciudad con las estaciones de bicis y las aristas que las conectan.
def plotgraph(bot, update):
	try:
		# Obtenemos el nombre de la imagen con una función externa.
		image = data.plot_graph()
		fitxer = "%d.png" % image
		bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
	except Exception as e:
		print(e)
		bot.send_message(chat_id=update.message.chat_id, text='💣')


# Función que devuelve la ruta entre dos puntos de la ciudad, tomando como argumentos dos direcciones.
# Luego se convierten las direcciones en coordenadas y se calcula la ruta más rápida con la función externa.
def route(bot, update, args):
	try:
		# Cambiamos el mensaje para eliminar el /route.
		address_info = update.message.text[7:]
		# Obtenemos con la función externa el tiempo que tardará el trayecto.
		tiempo = ruta(address_info)
		if time == -1:
			# En este caso no se ha encontrado la dirección y se devuelve una excepción.
			bot.send_message(chat_id=update.message.chat_id, text="Adreça no trobada")
		else :
			# Si se encuentran las direcciones se devuelve un mapa de la ruta más rápida entre ellas.
			# Aquí se obtiene el nombre del fichero con la imagen del mapa.
			image = data.plot_route()
			fitxer = "%d.png" % image
			bot.send_photo(chat_id=update.message.chat_id, photo=open(fitxer, 'rb'))
			# Aquí se devuelve un mensaje con la hora aproximada de llegada.
			message = "ETA: "
			message.append(str(datetime.time.now() + timedelta(minutes=tiempo)))
			bot.send_message(chat_id=update.message.chat_id, text=message)
	except Exception as e:
		print(e)
		bot.send_message(chat_id=update.message.chat_id, text='💣')



###########################################################################################


# Código de entrada que guardamos en una variable para poder acceder al bot.
TOKEN = open('token.txt').read().strip()

# Crea los objectos para trabajar con Telegram.
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

# Indica que cuando el bot reciba una orden dada se ejecute su función correspondiente.
dispatcher.add_handler(CommandHandler('start', start, pass_user_data=True))
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
