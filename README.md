# AP2_Bicing

Aquest projecte és el BicingBot de l'assignatura d'Algorísmia i Programació 2 del Grau en Ciència i Enginyeria de Dades de la UPC, any 2019. El projecte es basa en crear un bot per l'aplicació de missatgeria Telegram que informi sobre l'estat del servei de bicicletes Bicing a Barcelona en temps real.

## Introducció

Per fer servir el bot, els usuaris el poden buscar a telegram sota l'identificador @Bicing_AP2_bot.

Alternativament, es pot buscar en el web amb la direcció [t.me/Bicing_AP2_bot](https://t.me/Bicing_AP2_bot)

### Prerrequisits

El cos d'aquest projecte està escrit íntegrament en Python 3, a més d'utilitzar mòduls i interfícies externes. Per tal de poder fer-lo servir, un cop s'ha instal·lat Python 3, cal descarregar les components incloses en l'arxiu `requirements.txt`, on la manera més senzilla de fer-ho és amb la següent comanda a la terminal.

```sh
pip3 install -r requirements.txt
```

I així s'instal·les tots els mòduls i APIs necessàries pel funcionament del codi.

### Instal·lació

Per baixar-se el contingut d'aquest repositori, des de la terminal de comandes cal escriure:

```sh
git clone https://github.com/Sierra17/AP2_Bicing.git
```

I per actualitzar el contingut, mentre es trobi dins el directori

```sh
git pull
```

## Exemple d'utilització

Per util·litzar el bot, com s'ha indicat en la introducció, és preferible trobar-lo a Telegram com @Bicing_AP2_bot.
Per pujar el bot i control·lar el sue funcionament intern cal un `token` especific i, per tant, no és possible fer-ho sense el permís dels creadors del repositori. 
Un exemple d'util·lització que mostra la funcionalitat del bot és la següent:

## Autors

Els autors d'aquest projecte som dos estudiants del [CFIS](https://cfis.upc.edu/ca) que cursen el [Grau en Ciència i Enginyeria de Dades](http://dse.upc.edu/), a més del [Grau en Matemàtiques](https://fme.upc.edu/ca/estudis/graus/grau-en-matematiques), de la UPC.

- *Álvaro Ribot Barrado* <alvaro.ribot@est.fib.upc.edu>
- *Luis Sierra Muntané* <luis.sierra@est.fib.upc.edu>

## Agraïments

- Volem agraïr en primer lloc el resultat del nostre treball a Jordi Petit i Jordi Cortadella com els nostres docents, que han estat de molta ajuda a l'hora de resoldre dubtes i fer-nos veure els detallets més elegants i sofisticats de la programació orientada a objectes, i també en aquesta pràctica, les peculiaritats del Python.
- Un agraïment també a Telegram per la seva impresionant interfície i abast en possibilitats de producció amb tota la seva llibreria i documentació per bots, amb la qual ha estat un veritable plaer treballar, i encara més pel fet d'oferir exemples d'utilització de la llibreria que han estat molt útils.
