import time
import json
import random
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# =====================================================================
# BANCO DE VARIABLES BIZARRAS (8 OPCIONES POR COLOR)
# =====================================================================

LUGARES = {
    "Verde": [
        "en un potrero abandonado de la villa 31",
        "en el pasillo de ofertas de un supermercado chino apagado",
        "adentro de un contenedor de reciclaje de plástico en Palermo",
        "en la mina donde estaban los 33 mineros",
        "en la fila interminable para renovar el DNI",
        "en un bosque de lechugas mutantes de Chernobyl",
        "en el techo de un vagón de la línea C del subte",
        "en una convención clandestina de duendes de jardín"
    ],
    "Azul": [
        "en el VIP de una discoteca de mala muerte en el año 2099",
        "en el fondo de una pileta de lona pinchada",
        "adentro de un servidor refrigerado por agua destilada",
        "en una oficina pública que todavía usa disquetes",
        "en la fosa de las Marianas comiendo un choripán",
        "en una nube de tormenta que huele a suavizante de ropa",
        "en la Antártida, arriba de un glaciar con forma de carpincho",
        "en una fábrica de hielo seco que opera en el Metaverso"
    ],
    "Rojo": [
        "dentro de un reactor nuclear manejado por Windows 98",
        "en una pizzería que usa lava volcánica en vez de horno",
        "en el medio de un piquete liderado por robots oxidados",
        "adentro de un volcán activo lleno de salsa picante",
        "en una estación de servicio a las 3 de la mañana",
        "en el set de grabación de una película de terror de bajísimo presupuesto",
        "en una dimensión paralela donde todo está hecho de ladrillos de Lego rojos",
        "en la sala de servidores de una startup que se está incendiando"
    ]
}

ANTAGONISTAS = {
    "Verde": [
        "un clon malvado de la Joaqui",
        "un Shrek de un universo paralelo que habla con acento cordobés",
        "un vegetariano militante armado con un apio gigante",
        "el Increíble Hulk pero debilitado por una alergia al polen",
        "un vendedor ambulante de plantas carnívoras emocionales",
        "un elfo doméstico despedido por mal rendimiento",
        "un Grinch miniatura que vive en tu billetera",
        "un lagarto overo entrenado en artes marciales mixtas"
    ],
    "Azul": [
        "Kratos (de God of War) pero en versión contador público",
        "un Avatar de James Cameron que te debe dos meses de alquiler",
        "el pitufo filósofo con un megáfono oxidado",
        "un tiburón de call center hiperactivo",
        "un holograma de un mimo cibernético",
        "Megamind sufriendo un bloqueo de escritor",
        "un dispenser de agua mineral con inteligencia artificial psicópata",
        "un cobrador de impuestos ludópata"
    ],
    "Rojo": [
        "un ejército de carpinchos armados con navajas",
        "el diablo de las galletitas Sonrisas",
        "un clon furioso de Terminator hecho de plástico reciclado",
        "un Papá Noel en pleno mes de julio sufriendo un golpe de calor",
        "un tomate asesino con un doctorado en abogacía",
        "un Power Ranger rojo atrapado en una crisis de mediana edad",
        "un cangrejo gigante con cuchillos de carnicero",
        "un dragón de komodo que escupe fuego artificial"
    ]
}

MASCOTAS = {
    "Verde": [
        "un caniche toy que escupe fuego verde",
        "una tortuga ninja jubilada con reuma",
        "un loro que solo sabe insultar en código binario",
        "un camaleón daltónico crónico",
        "una planta de albahaca con ojos saltones que llora por las noches",
        "un saltamontes gigante con complejo de caballo de carrera",
        "un sapo Pepe real y bastante resentido con la fama",
        "un ganso cleptómano que roba llaves"
    ],
    "Azul": [
        "un Tamagotchi poseído por el espíritu de un pirata",
        "un pez dorado que tiene amnesia cada 3 segundos exactos",
        "un pingüino con bufanda que sabe hackear redes Wi-Fi públicas",
        "un delfín con rueditas para caminar en el asfalto",
        "un gato azul ruso que solo duerme sobre teclados mecánicos",
        "un pavo real que se cree agente secreto de la CIA",
        "una medusa inflable que flota en el aire",
        "un oso polar miniatura adicto al café frío"
    ],
    "Rojo": [
        "un caracol gigante con problemas de ansiedad",
        "un chihuahua con sobredosis de cafeína",
        "un zorro rojo que sabe bailar breakdance",
        "un hámster mutante que corre a la velocidad del sonido",
        "una langosta de agua dulce entrenada para desactivar explosivos",
        "un hurón piromaníaco",
        "un panda rojo flojo de papeles",
        "un escarabajo pelotero que transporta dinamita"
    ]
}

ALMAS_GEMELAS = {
    "Verde": [
        "Maradona sospechozamente lucido",
        "una lechuga orgánica con una personalidad arrolladora",
        "Yoda pero joven y desempleado",
        "una cosplayer de hiedra venenosa que solo habla de criptomonedas",
        "un alienígena del Área 51 que busca asilo político",
        "Fiona antes de transformarse en ogro",
        "un jardinero zen obsesionado con los cactus",
        "una estatua viviente de la Plaza de Mayo"
    ],
    "Azul": [
        "un bot de atención al cliente que aprendió a amar",
        "la estatua de la Libertad en versión miniatura y de plástico",
        "una sirena de agua dulce que trabaja en un acuario de shopping",
        "un pitufo rebelde que escucha heavy metal",
        "un astronauta que se quedó varado en la tierra por perder el pasaporte",
        "una IA generativa de imágenes que solo dibuja gatos tristes",
        "un buzo táctico con miedo al agua",
        "el genio de la lámpara pero sin presupuesto para conceder deseos"
    ],
    "Rojo": [
        "Maluma, pero transformado en un tacho de basura inteligente",
        "una llama de la Puna con peluca roja",
        "el doble de acción fallido de Spiderman",
        "una influencer de TikTok que solo sube videos comiendo ajíes picantes",
        "un bombero voluntario que le teme a las chispas",
        "Carmen Barbieri en una realidad alternativa de ciencia ficción",
        "un fantasma atrapado en una luz de giro de un Fiat Uno",
        "la personificación humana de una alerta roja del servicio meteorológico"
    ]
}

COMPAÑEROS_VIDEOJUEGOS = {
    "Verde": [
        "Mario bross (traumatizado por los deudas)",
        "Yoshi sufriendo una crisis de identidad",
        "Link (de Zelda) pero perdió la espada y usa una espátula",
        "Creeper de Minecraft reformado y pacifista",
        "Taylor Swift llegando de la panaderia en su jet",
        "Bulbasaur con insomnio",
        "Milei haciendo yoga",
        "Lionel Messi errando penales a lo bestia"
    ],
    "Azul": [
        "Sonic el Erizo con severos problemas de ciática",
        "Sub-Zero congelando fernet en una hielera",
        "Mega Man con la batería al 3%",
        "SANS de Undertale contándote chistes malos al oído",
        "Marcus Fenix quejándose de la inflación",
        "Gyarados atrapado en una pecera redonda",
        "Squirtle con anteojos negros truchos",
        "Arthur Morgan confundido por la tecnología moderna"
    ],
    "Rojo": [
        "Pac-Man sufriendo una indigestión existencial",
        "Mario Bros enojado porque se le inundó el sótano",
        "Kratos usando cremitas para las arrugas",
        "Charizard con dolor de garganta",
        "Spider-Man con el traje encogido por el lavarropas",
        "Trevor Philips (de GTA V) tomando un té de tilo",
        "Knuckles el Equidna perdido en la General Paz",
        "Scorpion gritando 'Get over here' en la fila del banco"
    ]
}

HEROES_INESPERADOS = {
    "Verde": [
        "algun turro con un doctorado en física cuántica",
        "un guardabosques con un soplador de hojas supersónico",
        "Auron Play jubilado",
        "Robin Hood pero roba datos de internet",
        "un vendedor de palitos helados de limón",
        "el increíble Hulk todo chikito, todo panzon",
        "un ninja camuflado en una planta de interior",
        "Alberto haciendose el canchero con todo lo que proyecte sombra"
    ],
    "Azul": [
        "Ricardo Fort en un meca gigante de oro",
        "un capitán de barco que se marea en la bañera",
        "el mismísimo Neptuno armado con un tenedor parrillero",
        "un pibe que maneja un camión de la Serenísima",
        "un reparador de módems de internet a domicilio",
        "un limpiador de piletas con superpoderes hidráulicos",
        "un doble de riesgo de Aquaman",
        "un vendedor de garrapiñadas espaciales"
    ],
    "Rojo": [
        "Goku, pero se olvidó cómo convertirse en Super Saiyajin",
        "un bombero jubilado con un matafuegos de cotillón",
        "Thor pero el martillo es de goma espuma",
        "un cocinero experto en asado con un tenedor gigante",
        "el mismísimo Iron Man pero sin batería en el traje",
        "un motoquero de delivery con escape libre ruidoso",
        "un torero que le tiene fobia a las vacas",
        "un gladiador romano desorientado en Buenos Aires"
    ]
}

PODERES_ABSURDOS = {
    "Verde": [
        "la capacidad de digerir telgopor como si fuera pizza",
        "hacer crecer el pasto 1 milímetro por hora con la mirada",
        "olfatear el miedo de los vegetales",
        "invocar un enjambre de mosquitos que solo te pican a vos",
        "transformar billetes de mil pesos en billetes del Estanciero",
        "estornudar confeti verde ecológico",
        "cambiar el canal de la tele del vecino parpadeando fuerte",
        "detectar si una palta está madura a 5 kilómetros de distancia"
    ],
    "Azul": [
        "invocar un olor a tostadas quemadas cada vez que mientes",
        "hacer que el agua de la canilla salga tibia tirando un centro",
        "adivinar el saldo de la tarjeta SUBE de desconocidos",
        "llorar cubitos de hielo para el Fernet",
        "hacer que los semáforos se pongan en azul mágicamente",
        "levitar exactamente a 2 centímetros del suelo si estás descalzo",
        "hablar el idioma de los lavarropas automáticos",
        "enfriar una lata de cerveza en 45 minutos usando telepatía"
    ],
    "Rojo": [
        "hacer que los pantalones de la gente se vuelvan invisibles con la mente",
        "calentar empanadas con la fricción de tus manos",
        "hacer sonar una alarma de auto cada vez que pestañeas",
        "hacer que a tu enemigo le pique la espalda justo donde no llega",
        "hacer que la pizza siempre caiga del lado del queso",
        "invocar un chorro de kétchup desde tu dedo índice",
        "encender fósforos con el chasquido de tus dedos (pero te quemas)",
        "hacer que la gente cante el himno nacional si los miras fijo"
    ]
}

# =====================================================================
# VARIABLES NUMÉRICAS (8 OPCIONES PARA PAR E IMPAR)
# =====================================================================

OBJETOS_CLAVE = {
    "par": [
        "una baguette dura de hace cuatro días", "un sacacorchos oxidado", 
        "una crocs izquierda color amarillo patito", "un mouse de computadora con ruedita mugrienta",
        "un paraguas roto que solo se abre al revés", "un termo Stanley trucho",
        "una revista Billiken de 1994", "un cargador de celular que hace falso contacto"
    ],
    "impar": [
        "un destornillador de plástico de juguete", "un paquete de galletitas surtidas vacío",
        "un Nokia 1100 con la linterna encendida", "un cepillo de dientes eléctrico sin pilas",
        "una entrada vieja para ver a ricky maravilla", "un spinner oxidado",
        "un frasco de mermelada usado como vaso", "un rulemán de skate lleno de grasa"
    ]
}

ACCIONES_BIZARRAS = {
    "par": [
        "vender medias en el subte", "explicarle física cuántica a un gato de la calle",
        "comprar un terreno en la luna con la tarjeta de crédito", "organizar un torneo de piedra, papel o tijera por plata",
        "limpiar la pantalla del monitor con la manga del buzo", "discutir el precio del queso con el fiambrero",
        "intentar lamerte el codo en público", "hacer un asado usando folletos de supermercado como carbón"
    ],
    "impar": [
        "bailar un tango con un dispenser de agua", "hacer un speedrun de armar un rompecabezas de 4 piezas",
        "buscar tu propio nombre en Google a las 4 de la mañana", "intentar convencer a la AFIP de que eres un elfo",
        "gritar los goles de los partidos diferidos", "hacerle RCP a un electrodoméstico roto",
        "escribir un poema de amor dedicado a la milanesa de pollo", "correr carreras de caracoles en el patio"
    ]
}

SACRIFICIOS = {
    "par": [
        "tu cuenta de Netflix compartida", "el dedo chiquito del pie izquierdo",
        "tu historial de navegación de Google", "el último pedazo de pizza fría de la heladera",
        "tu capacidad de recordar contraseñas", "tu dignidad en la próxima cena familiar",
        "el derecho a usar el asiento del medio en los aviones", "tu colección secreta de stickers de WhatsApp"
    ],
    "impar": [
        "el ligamento cruzado de tu rodilla izquierda", "la clave de tu homebanking",
        "el peluche favorito de tu infancia", "tu memoria a corto plazo para los nombres",
        "tu paciencia con la gente que camina lento", "las plantillas de tus zapatillas favoritas",
        "el orgullo de haber terminado la secundaria", "tu habilidad para abrir frascos de mermelada"
    ]
}

RECOMPENSAS = {
    "par": [
        "tres empanadas de humita frías", "un vale por un helado que venció ayer",
        "un billete de dos pesos firmado por el Diego", "la mitad de un alfajor de maizena seco",
        "un aplauso incómodo de tres personas desconocidas", "una moneda de 25 centavos de la suerte",
        "un folleto de cerrajería 24 horas", "el respeto temporal de un perro de la calle"
    ],
    "impar": [
        "un sticker brillante de un Pikachu gordo", "un llavero con forma de destapador de cerveza",
        "una tuerca dorada que calza en ningún tornillo", "un paquete de pañuelos descartables usado",
        "la admiración eterna de un mimo", "un cupón de descuento del 5% en una carnicería espacial",
        "un DVD pirata de Shrek 2 rayado", "una medialuna de manteca aplastada"
    ]
}

def obtener_variables_numericas(numero):
    ahora = datetime.now()
    segundos_offset = int((numero * 54321) % 100000000)
    fecha_futura = ahora + timedelta(seconds=segundos_offset)
    fecha_exacta = fecha_futura.strftime("%d/%m/%Y a las %H:%M:%S")

    # Determinar tipo de número
    tipo = "par" if numero % 2 == 0 else "impar"

    return {
        "fecha": fecha_exacta,
        "objeto_clave": random.choice(OBJETOS_CLAVE[tipo]),
        "accion_bizarra": random.choice(ACCIONES_BIZARRAS[tipo]),
        "sacrificio": random.choice(SACRIFICIOS[tipo]),
        "recompensa": random.choice(RECOMPENSAS[tipo])
    }

# =====================================================================
# PROTOTIPOS DE HISTORIAS (Estructuras fijas elegidas al azar)
# =====================================================================

PROTOTIPOS_HISTORIAS = [
    "El {fecha}, el universo colapsará cuando {nombre} sea reclutado para ir a la guerra {lugar}. Tu único aliado será {companero_videojuego} y tu arma secreta será {objeto_clave}. Tras vencer a {antagonista}, tu recompensa final será {recompensa}.",
    "El destino dicta que el {fecha}, {nombre} encontrará a su alma gemela: {alma_gemela}. El encuentro ocurrirá {lugar}, pero todo se complicará cuando {antagonista} intente arruinar la boda. Por suerte, tu mascota, {mascota}, usará {poder_absurdo} para salvar el día.",
    "Alerta de paradoja temporal. El {fecha}, {nombre} sufrirá una muerte ridícula {lugar} tras intentar {accion_bizarra}. En el más allá, {antagonista} te ofrecerá revivir a cambio de {sacrificio}. Volverás a la vida acompañado por {hero_inesperado}.",
    "Preparate, {nombre}. El {fecha} planearás el robo de {recompensa} {lugar}. El plan maestro incluye usar {poder_absurdo} y la distracción de {companero_videojuego}. Si fallas, pasarás el resto de tus días alimentando a {mascota} con {objeto_clave}.",
    "El {fecha} se celebrará el torneo intergaláctico de {accion_bizarra}. {nombre} de la Tierra peleará usando {objeto_clave}. En las semifinales te enfrentarás a {antagonista}. Justo antes de perder, {hero_inesperado} bajará del cielo para regalarte {recompensa}."
]

# ---- RUTAS ----

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "resultado": None})

@app.post("/oracle", response_class=HTMLResponse)
def oracle(request: Request, nombre: str = Form(...), numero: int = Form(...), color: str = Form(...)):
    
    # 1. Extraer una opción al azar de las 8 disponibles usando random.choice()
    lugar = random.choice(LUGARES.get(color))
    antagonista = random.choice(ANTAGONISTAS.get(color))
    mascota = random.choice(MASCOTAS.get(color))
    alma_gemela = random.choice(ALMAS_GEMELAS.get(color))
    companero_videojuego = random.choice(COMPAÑEROS_VIDEOJUEGOS.get(color))
    hero_inesperado = random.choice(HEROES_INESPERADOS.get(color))
    poder_absurdo = random.choice(PODERES_ABSURDOS.get(color))
    
    var_numeros = obtener_variables_numericas(numero)
    
    # 2. Elegir la plantilla narrativa
    plantilla_elegida = random.choice(PROTOTIPOS_HISTORIAS)
    
    # 3. Formatear la historia final
    historia_final = plantilla_elegida.format(
        nombre=nombre.strip().upper(),
        lugar=lugar,
        antagonista=antagonista,
        mascota=mascota,
        alma_gemela=alma_gemela,
        companero_videojuego=companero_videojuego,
        hero_inesperado=hero_inesperado,
        poder_absurdo=poder_absurdo,
        fecha=var_numeros["fecha"],
        objeto_clave=var_numeros["objeto_clave"],
        accion_bizarra=var_numeros["accion_bizarra"],
        sacrificio=var_numeros["sacrificio"],
        recompensa=var_numeros["recompensa"]
    )

    return templates.TemplateResponse("index.html", {
        "request": request,
        "resultado": {"nombre": nombre, "mensaje": historia_final}
    })