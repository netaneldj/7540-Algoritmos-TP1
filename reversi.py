DIMENSION=8 #Si la dimension del tablero es es menor a 2 o la dimension es mayor a 26 se producira un error
VERIFICAR=0 #VERIFICAR y ESCRIBIR son los dos estados que uso en la variable momento a lo largo del programa
ESCRIBIR=1
ABECEDARIO=("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z")

def bienvenida():
	"""Le da la bienvenida al usuario y le explica como sera el juego"""
	print("Bienvenido al reversi!!!")
	print("A continuacion se mostrara el tablero del juego:")

def generar_tablero():
	"""Crea el tablero usando LIST COMPREHENSIONS con un for anidado, devuelve el tablero"""
	return [["" for casillero in range(DIMENSION)] for casillero in range(DIMENSION)] 	

def imprimir_tablero(tablero):
	"""Imprime posicion por posicion del tablero con un for anidado (a cada posicion le resto uno porque para el usuario
		la posicion empieza desde uno y para el programa la posicion empieza desde cero), ademas imprime las 
		letras que le corresponden a las columnas y los numeros que le corresponden a las filas, no devuelve nada"""	
	for numero_letra in range(DIMENSION):
		#Imprime DIMENSION letras, una por cada casillero
		if(DIMENSION>=2 and DIMENSION<=len(ABECEDARIO)):
			print("   "+ABECEDARIO[numero_letra],end="")
		else:
			raise IndexError("La dimension del tablero no puede ser menor que 2 ní mayor que 26 ;)")
	print("")
	for num_fila in range(1,DIMENSION+1):
		if (num_fila<10):
			print("0"+str(num_fila),end="")
		else:
			print(num_fila,end="")
		print("|",end="")
		for num_col in range(1,DIMENSION+1):
			if(tablero[num_fila-1][num_col-1]!=""):
				print(" "+tablero[num_fila-1][num_col-1],end=" |")
			else:
				print("",end="   |")
		print("")
		
def	ingreso_ficha():
	"""El usuario ingresa las coordenadas donde va a querer posicionar su ficha,primero la columna y luego la fila, devuelve lo ingresado"""
	x=input("Ingrese la letra de la columna donde quiere posicionar su ficha: ")
	x=x.lower()
	posy=input("Ingrese el numero de fila donde quiere posicionar su ficha(cero o negativo para salir): ")
	return x,posy
		
def validar_ingreso_ficha():
	"""Llamo a una funcion que pide el ingreso de las posiciones,llamo a otra funcion que verifique que la coordenada 
		sea valida, si lo es devuelve la fila y columna ingresada, sino le comenta al usuario que la coordenada no existe 
		y le pide que ingrese otra, devuelve la posicion de la ficha"""
	x,posy=ingreso_ficha()
	if not(verificar_ingreso_valido(x,posy)):
		while(verificar_ingreso_valido(x,posy)==False):
			print("La posicion ingresada no existe...")
			x,posy=ingreso_ficha()
	posy=int(posy)
	for letra in range (len(ABECEDARIO)):
		if(x==ABECEDARIO[letra]):
			posx=letra+1
	return posx,posy

def verificar_ingreso_valido(x,posy):
	"""Verifica que la coordenada sea valida, que exista dentro de las dimensiones del tablero"""
	if(len(x)==1 and x.isalpha() and posy.isdigit()):
		if x in ABECEDARIO:
			for letra in range(len(ABECEDARIO)):
				if(x==ABECEDARIO[letra] and letra+1>=1 and letra+1<=DIMENSION and int(posy)<=DIMENSION):
					return True
	return False
			
def es_jugada_valida(tablero,posx,posy,ficha,momento):
	"""Si el momento es VERIFICAR se fija si hay una jugada posible en la posx, posy que se le ingresa.
		Si el momento es ESCRIBIR se fija en que direcciones se puede comer, come las fichas y te devuelve el 
		tablero con la jugada ya hecha"""
	if(tablero[posy-1][posx-1]!=""):
		if(momento==VERIFICAR):
			return False
		return tablero
	for dx in range(1,-2,-1):
		for dy in range(1,-2,-1):
			if (dx==0 and dy==0):
				continue	
			px=posx
			py=posy
			while(px+dx>=1 and px+dx<=DIMENSION and py+dy>=1 and py+dy<=DIMENSION):
				px+=dx
				py+=dy
				if(tablero[py-1][px-1]!=ficha and tablero[py-1][px-1]!="" and tablero[py-1+dy][px-1+dx]==ficha):
					if(momento==VERIFICAR):
						return True
					else:
						casillerox=posx
						casilleroy=posy
						while(casillerox+dx>=1 and casillerox+dx<=DIMENSION and casilleroy+dy>=1 and casilleroy+dy<=DIMENSION):
							casillerox+=dx
							casilleroy+=dy
							if(tablero[casilleroy-1][casillerox-1]!=ficha):
								tablero[casilleroy-1][casillerox-1]=ficha
							else:
								break
						break								
	if(momento==VERIFICAR):
		return False
	return	tablero

def jugada_posible(tablero,ficha,momento):
	"""Se fija si la ficha que se le pasa por parametro tiene una jugada posible, tomando 
		a los espacios vacios como jugadas potenciales"""
	for fila in range(DIMENSION):
		for columna in range(DIMENSION):
			if (tablero[fila][columna]==""):
				if(es_jugada_valida(tablero,columna+1,fila+1,ficha,momento)):
					return True
	return False
	
def condiciones_iniciales(tablero):
	"""Son las cuatro fichas que se ponen en el centro al comenzar el juego"""
	tablero[DIMENSION//2-1][DIMENSION//2-1]="B"
	tablero[DIMENSION//2-1][DIMENSION//2]="N"
	tablero[DIMENSION//2][DIMENSION//2-1]="N"
	tablero[DIMENSION//2][DIMENSION//2]="B"

def posicionar_ficha_tablero(tablero,posx,posy,ficha):
	"""Es la funcion que posiciona las fichas en el tablero"""
	tablero=es_jugada_valida(tablero,posx,posy,ficha,ESCRIBIR)
	tablero[posy-1][posx-1]=ficha

def contador_fichas(tablero):
	"""Cuenta las fichas de cada color para saber al finalzar la partida que jugador gano"""
	contN=0
	contB=0
	for columna in range(DIMENSION):
		for fila in range(DIMENSION):
			if(tablero[columna][fila]=="N"):
				contN+=1
			elif(tablero[columna][fila]=="B"):
				contB+=1
	return contN,contB
	
def cambiar_de_ficha(ficha):
	"""Recibe una ficha y la devuelve cambiada, pasa de turno"""
	if(ficha=="N"):
		ficha="B"
	else:
		ficha="N"
	return ficha
	
def quien_gano(tablero):
	"""Recibe el tablero, llama a la funcion que cuenta las fichas de cada jugador, imprime quien gano"""
	cantN,cantB=contador_fichas(tablero)
	if(cantN>cantB):
		print("Gano el jugador negro con {} fichas contra {} fichas".format(cantN,cantB))
	elif(cantN==cantB):
		print("Empate de {} fichas".format(cantN))
	else:
		print("Gano el jugador blanco con {} fichas contra {} fichas".format(cantB,cantN))
	
def ciclo_juego(tablero):
	"""Es la funcion que se repite en cada jugada, tiene toda la logica del juego"""
	ficha="N"
	cont_jugadas=0
	print("Es el turno del jugador: {}".format(ficha))
	if(jugada_posible(tablero,ficha,VERIFICAR)):
		print("Hay jugadas posibles para el jugador: {}".format(ficha))
	posx,posy=validar_ingreso_ficha()
	while(posx>0 and posy>0 and cont_jugadas<60):
		if not(jugada_posible(tablero,"B",VERIFICAR) and jugada_posible(tablero,"N",VERIFICAR)):
			print("No hay jugadas posibles para ninguno de los dos jugadores, el juego ha tarminado")
			quien_gano(tablero)
			return 0
		if(jugada_posible(tablero,ficha,VERIFICAR)):
			if(es_jugada_valida(tablero,posx,posy,ficha,VERIFICAR)):
				posicionar_ficha_tablero(tablero,posx,posy,ficha)
			else:
				print("Jugada no valida!")
				while not(es_jugada_valida(tablero,posx,posy,ficha,VERIFICAR)):
					print("Hay jugadas posibles para el jugador: {}".format(ficha))
					posx,posy=validar_ingreso_ficha()
					if(es_jugada_valida(tablero,posx,posy,ficha,VERIFICAR)):
						posicionar_ficha_tablero(tablero,posx,posy,ficha)
						break
		imprimir_tablero(tablero)
		ficha=cambiar_de_ficha(ficha)
		print("Es el turno del jugador: {}".format(ficha))
		if(jugada_posible(tablero,ficha,VERIFICAR)):
			print("Hay jugadas posibles para el jugador: {}".format(ficha))
		else:
			print("No hay jugadas posibles para el jugador: {}, se pasara el turno".format(ficha))
			ficha=cambiar_de_ficha(ficha)	
		posx,posy=validar_ingreso_ficha()
	print("Usted ha finalizado el juego")
	quien_gano(tablero)	
	
def main():
	"""Es lla funcion main, dentro de ella llamo a las funciones iniciales """
	bienvenida()
	tablero=generar_tablero()
	condiciones_iniciales(tablero)
	imprimir_tablero(tablero)
	ciclo_juego(tablero)
main()
