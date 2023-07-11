# Instrucciones para ejecutar  el proyecto:
Descargar y compilar glucose. Luego, pegar el archivo "glucose" dentro de la carpeta "Solver".

El proyecto ha sido desarrollado en Python. Se debe tener el interpretador de [Python](https://www.python.org/downloads/) instalado. Luego, instalar las dependencias ejecutando el comando: 
`pip install -r requirements.txt `

Para correr el proyecto, se necesita tener el json en un archivo .json. Luego, se mueve hacia la carpeta Solver usando:
`cd Solver`
y se ejecuta
`python3 main.py <ruta al json>`
El archivo cnf se genera como ¨cnf.cnf¨ y el archivo ics se genera con formato <nombre_del_troneo>.ics

### Ejemplo de ejecución
A continuación, se muestra un ejemplo para ejecutar el proyecto.

El archivo torneo.json contiene:

{
  "tournament_name": "tournamentname",
  "start_date": "2017-06-01",
  "end_date": "2017-06-13",
  "start_time": "07:00:20",
  "end_time": "18:23:09",
  "participants": ["leones","tiburones","aguilas","tigres"]
}


Se ejecuta:

`python3 main.py torneo.json`

Esto crea el archivo ¨cnf.cnf¨. Este archivo se le pasa a glucose y genera el archivo:
¨tournament.ics¨
# Objetivo

El objetivo de este proyecto es aprender a modelar un problema en CNF, y a usar un SAT solver para resolverlo, así como traducir la salida del SAT solver a un formato legible.
No solo se evaluará que la implementación funcione, sino la eficiencia de su traducción a CNF del problema.

# Problema a resolver

Imagine que se está organizando un torneo, y se le pide realizar un programa que encuentre una asignación de fecha y hora en la que los juegos van a ocurrir. Las reglas son las siguientes:

* Todos los participantes deben jugar dos veces con cada uno de los otros participantes, una como "visitantes" y la otra como "locales". Esto significa que, si hay 10 equipos, cada equipo jugará 18 veces.
* Dos juegos no pueden ocurrir al mismo tiempo.
* Un participante puede jugar a lo sumo una vez por día.
* Un participante no puede jugar de "visitante" en dos días consecutivos, ni de "local" dos días seguidos.
* Todos los juegos deben empezar en horas "en punto" (por ejemplo, las 13:00:00 es una hora válida pero las 13:30:00 no).
* Todos los juegos deben ocurrir entre una fecha inicial y una fecha final especificadas. Pueden ocurrir juegos en dichas fechas.
* Todos los juegos deben ocurrir entre un rango de horas especificado, el cuál será fijo para todos los días del torneo.
* A efectos prácticos, todos los juegos tienen una duración de dos horas.

# Formato de entrada

Su sistema debe recibir un JSON con el siguiente formato (asuma que siempre recibirá el formato correcto):

```
{
  "tournament_name": String. Nombre del torneo,
  "start_date": String. Fecha de inicio del torneo en formato ISO 8601,
  "end_date": String. Fecha de fin del torneo en formato ISO 8601,
  "start_time": String. Hora a partir de la cuál pueden ocurrir los juegos en cada día, en formato ISO 8601,
  "end_time": String. Hora hasta la cuál pueden ocurrir los juegos en cada día, en formato ISO 8601,
  "participants": [String]. Lista con los nombres de los participantes en el torneo
}
```

Asuma que todas las horas vienen sin zona horaria especificada, y asuma por lo tanto que su zona horaria es UTC.

# Actividad 1

Deben crear una traducción del problema a formato CNF, y luego deben crear un programa, en el lenguaje de programación que sea de su agrado, que traduzca cualquier JSON en el formato propuesto a la representación del problema en formato [DIMACS CNF](https://people.sc.fsu.edu/~jburkardt/data/cnf/cnf.html)

# Actividad 2

Usando la transformación creada en la parte anterior, los archvios en formato DIMACS CNF pueden ser usados como entrada para el SAT solver [Glucose](https://www.labri.fr/perso/lsimon/glucose/). Debe crear un programa, en el lenguaje de programación que sea de su agrado, que traduzca la salida de Glucose al resolver el problema en un archivo con el mismo nombre del torneo y extensión `.ics`, en formato de [iCalendar](https://en.wikipedia.org/wiki/ICalendar) de manera que sea posible agregar la asignación de los juegos a un gestor de calendarios. Para ello puede usar cualquier librería que considere necesaria. Los eventos del calendario deben tener ocurrir a la hora que fue asignada cumpliendo todas las reglas dadas, y deben indicar quiénes son los participantes en el juego, quién es el "local" y quién es el "visitante".

# Actividad 3

Debe crear un cliente que maneje todo el proceso. Es decir, reciba un JSON en el formato de entrada, ejecute el programa que lo transforma en CNF, introduzca el resultado  en Glucose, y se asegure de que se cree el archivo .ics con la respuesta, o falle en caso de ser UNSAT. Debe generar casos de prueba fáciles y difíciles, y medir el rendimiento de su solución.

# Entrega

Deben tener un repositorio con todo el código usado y un informe que describa su solución, sus resultados experimentales, así como instrucciones específicas para ejecutar todo el proceso.
