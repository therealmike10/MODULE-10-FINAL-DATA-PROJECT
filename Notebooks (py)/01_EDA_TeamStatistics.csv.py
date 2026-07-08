#DATA PROJECT: PROYECTO FINAL
#Autor: Miguel Encinas Gimenez

#En este primer archivo .py vamos a realizar la exploración y limpieza de los datos correspondientes a la primera tabla
#con la que vamos a trabajar: TeamStatistics.csv. Dicha tabla contiene las estadísticas actualizadas, a nivel de los
#equipos, de todos los partidos disputados en la NBA, desde 1946 hasta 2026.
#En la tabla, caben destacar datos muy relevantes: el id del partido, fecha y hora del partido, nombres e IDs del equipo
#y el equipo rival, estadísticas completas del equipo en el partido y tipo de partido, entre otras

#1. BLOQUE DE IMPORTACIÓN DE MÓDULOS
import pandas as pd
import numpy as np
import os

#2.BLOQUE DE CARGA DE NUESTROS DATOS E INFORMACIÓN BÁSICA
#En primer lugar, cargamos nuestro archivo csv en un dataframe de pandas.
file = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/DATOS/NBA/archive (1)/TeamStatistics.csv"
df_equipos = pd.read_csv(file)

#Tras esto, imprimimos las 10 primeras filas de nuestro dataframe para estudiar los datos. Como tenemos muchas columnas, le pedimos
#que nos las muestre tdoas con set_option.
pd.set_option('display.max_columns', None)
# print(df_equipos.head(10))

#También solicitamos a pandas la información principal de nuestro archivo, así como el número de datos faltantes.
print(df_equipos.info())
# print(df_equipos.isnull().sum())
print(df_equipos.isna().sum())
#Vemos que tenemos 44 columnas float64, 5 columnas int64 y 9 columnas str. Además, tenemos una gran variedad de de valores
#null/na en nuestras columnas, así que vamos a ir columna por columna estudiando cada caso particular.

#Por último, por costumbre con otros dataframes, no sé si me terminará siendo útil o no, pero ya que la fecha del partido
#está en un formato aceptable, voy a convertirla a datetime y a extraer el día, el nombre del mes y el año en el que se jugó
df_equipos['gameDateTimeEst'] = pd.to_datetime(df_equipos['gameDateTimeEst'])
df_equipos = df_equipos.assign(game_month = df_equipos['gameDateTimeEst'].dt.strftime("%B"),
                               game_year = df_equipos['gameDateTimeEst'].dt.year,
                               game_day = df_equipos['gameDateTimeEst'].dt.day)


#3. BLOQUE MODIFICACIÓN COLUMNAS + ELIMINACIÓN/SUSTITUCIÓN DE NaN, null
#COLUMNA 'gameDateTimeEst': No tiene valores null, así que por ahora no hacemos nada con ella

#COLUMNA 'teamCity' y 'opponentTeamCity':
print(df_equipos['teamCity'].isnull().sum())  #Observamos que tenemos 16 valores nulos
df_equipos1 = df_equipos[df_equipos['teamCity'].isna() == True] #Estudiando el tipo de partido al que se refiere, vemos que
#se tratan de partidos All-Star, los cuales no nos interesan para este análisis, y futuramente eliminaremos, así que podemos
#eliminar ya estas 16 filas con valor nulo
filas_eliminar = df_equipos[df_equipos['teamCity'].isna() == True].index
df_equipos.drop(filas_eliminar, axis = 0, inplace = True)
#Con este bloque parece que, de paso, nos hemos quitado también varios partidos que tenían valor null en otras columnas

#COLUMNA 'assists','blocks','steals', etc.
print(df_equipos['assists'].isnull().sum())
df_equipos2 = df_equipos[df_equipos['assists'].isna() == True] #Observamos que las 2 filas con valores nulos para 'assists' al parecer presenta
#también valores nulos para la mayoría de las estadísticas. Parece que ser que fue un partido jugado en febrero de 1963 para
#el cual, por algún motivo, no se recogieron las estadísticas. Por tanto, vamos a borrar las dos entradas de ese partido
#correspondientes a los dos equipos, y así limpiamos varias columnas de golpe)
filas_eliminar2 = df_equipos[df_equipos['assists'].isna() == True].index
df_equipos.drop(filas_eliminar2, axis = 0, inplace = True)
#Con este bloque también hemos dejado limpias varias columnas que tenían ese par de filas con valores nulos

#COLUMNA 'threePointersPercentage'
print(df_equipos['threePointersPercentage'].isnull().sum())
df_equipos3 = df_equipos[df_equipos['threePointersPercentage'].isna() == True] #Con esta variable ocurre algo curioso, y es que solamente
#hay una fila que presente valor nulo en esta variable. Si lo imprimimos y miramos los datos detalladamente, observamos que  es un partido
#jugado en diciembtre de 1988. No es que falte el dato, es que en ese partido, el equipo en cuestión no tiró ni un solo triple (un evento
#aislado bastante extraño). Por tanto, todo indica que la fórmula usada no estaba preparada para que la división entre los triples anotados
#y los triples intentados sea una división de 0/0. Lo mejor en este caso, por tanto, es sustituir el valor nulo por un 0
posicion1 = df_equipos[df_equipos['threePointersPercentage'].isna() == True].index #Averiguamos la posición de la fila en la tabla
print(posicion1)
df_equipos.loc[98263,'threePointersPercentage'] = 0 #Sustituimos el valor nulo por 0 en la posición que nos interesa

#COLUMNA 'numMinutes': Esta columna representa normalmente los minutos que un jugador pasa en pista. Siendo estas las estadísticas de un
#equipo, hay que contar con que hay 5 jugadores jugando en todo momento, por tanto: 5 jugadores * 4 cuartos * 12 minutos/cuarto = 240.
#Hay que considerar además, que las prórrogas son de 5 minutos, por lo que habría que sumar otros 25 minutos (5 minutos * 5 jugadores)
#por cada prórroga que se haya jugado. Por tanto, nos interesan los valores 240, 265, 290, 315, 340, etc.
print(df_equipos['numMinutes'].value_counts()) #Parece que tenemos una pequeña representación de otros valores diferentes a los mencionados.
#Como a prior son valores sin sentido, y son una ínfima parte del conjunto de datos, eliminaremos dichas filas.
valores_minutos = df_equipos['numMinutes'].unique().tolist() #Creamos una lista de todos los valores de la variables
lista_conservar = [240,265,290,315,340,365] #Definimos una lista de las variables que conservar
lista_eliminar = [] #Creamos una lista vacía
for valor in valores_minutos: #For loop con condicional: si el número no está en la lista de valores a conservar, lo añade a la lista de eliminar
    if valor in lista_conservar:
        pass
    else:
        lista_eliminar.append(valor)
filas_eliminar3 = df_equipos[df_equipos['numMinutes'].isin(lista_eliminar)].index #Sacamos los index de las filas con los valores a eliminar para
#la variable 'numMinutes'. Entre ellos se encuentra también el valor nulo, así que aprovechamos el mismo código para solucionar dos problemas
df_equipos.drop(filas_eliminar3, axis = 0, inplace = True) #Eliminamos dichas filas

#COLUMNA 'plusMinusPoints': En esta columna hay 52 valores nulos, a los cuales les faltan también multitud de estadísticas, como benchPoints,
#timesTied, biggesLead, gameType, etc. Asumimos que los datos han sido recogidos de manera incompleta, y por tanto eliminamos dichas filas
print(df_equipos['plusMinusPoints'].isnull().sum())
df_equipos4 = df_equipos[df_equipos['plusMinusPoints'].isna() == True]
filas_eliminar4 = df_equipos[df_equipos['plusMinusPoints'].isna() == True].index
df_equipos.drop(filas_eliminar4, axis = 0, inplace = True)

#COLUMNA 'q1Points','q2Points','q3Points','q4Points'
print(df_equipos[['q1Points','q2Points','q3Points','q4Points']].isnull().sum()) #Parece que las 4 columnas, indicando cada uno los puntos anotados
#por el equipo en el cuarto correspondiente, presentan 7119 nulos (seguramente en las mismas filas). He valorado qué información puede ser más
#valiosa: esos 4 partidos con valor nulo, o las variables de los puntos en cada cuarto en general. Para este conjunto de datos, creo que no merece
#mucho la pena estudiar con detalle los puntos en cada cuarto, y esos +7,000 partidos, a pesar de tener +146,000 en total, los considero una porción
#importante de la información. Por tanto, procedemos a eliminar las columnas de los puntos en cada cuarto.
df_equipos.drop(columns = ['q1Points','q2Points','q3Points','q4Points'], inplace = True)
print(df_equipos.isna().sum())

#COLUMNAS Estadísticas varias
print(df_equipos[['benchPoints', 'biggestLead', 'biggestScoringRun', 'leadChanges',
                  'pointsFastBreak', 'pointsFromTurnovers', 'pointsInThePaint','pointsSecondChance',
                  'timesTied','timeoutsRemaining','seasonWins','seasonLosses']].isnull().sum())
#Todas estas categorías tienen 7117 partidos con valores null. Veamos cómo se distribuyen esos partidos en función del equipo y los años (asumimos
#que todas faltan en los mismos partidos, ya que hay exactamente el mismo número de nulos):
df_equipos['gameDateTimeEst'] = pd.to_datetime(df_equipos['gameDateTimeEst'])
df_equipos = df_equipos.assign(game_month = df_equipos['gameDateTimeEst'].dt.strftime("%B"),
                               game_month_num = df_equipos['gameDateTimeEst'].dt.month, #Necesitaremos el mes en formato númerico más adelante
                               game_year = df_equipos['gameDateTimeEst'].dt.year,
                               game_day = df_equipos['gameDateTimeEst'].dt.strftime("%d"))
df_equipos5 = df_equipos[df_equipos['benchPoints'].isna() == True]
df_equipos5_1 = df_equipos5.groupby('teamName')['gameId'].count()
df_equipos5_2 =  df_equipos5.groupby('game_year')['gameId'].count()
#Lo que obtenemos es que, por un lado, parece que cada equipo tiene más o menos el mismo número de partidos con esas estadísticas con valores nulos,
#lo cual es asumible. Sin embargo, cuando agrupamos por años, vemos que hay años, como 2021 y 2022, en los que tenemos más de mil entradas con esos
#valores nulos. Considerando que cada partido está presente dos veces (para estudiar la estadística de ambos equipos), significa que perderíamos más
#de 500 partidos cada uno de esos años.
df_equipos.fillna(
    {'gameType': 'Not informed'},
    inplace = True)
#Hacemos una última comprobación, y vemos que los equipos que no tienen esas estadísticas informadas, tampoco tiene informado el tipo de partido que era.
df_equipos6 = df_equipos[df_equipos['benchPoints'].isna() == True]
df_equipos6_1 = df_equipos6.groupby('gameType')['gameId'].count()
#Con lo cual tenemos una serie de partidos de los últimos 20 años, de varios equipos, en los que la información es parcial.La decisión que tomamos es mixta.
#Por un lado, bajo el mismo razonamiento previo, considero inasumible perder tal cantidad de partidos, ya que los encuentro más valiosos para el análisis que
# queremos hacer, que estas estadísticas en concreto. Por tanto, las columnas que hemos mostrado previamente las vamos a eliminar.
df_equipos.drop(columns = ['benchPoints', 'biggestLead', 'biggestScoringRun', 'leadChanges',
                  'pointsFastBreak', 'pointsFromTurnovers', 'pointsInThePaint','pointsSecondChance',
                  'timesTied','timeoutsRemaining','seasonWins','seasonLosses'], inplace = True)
#Tras esto, vamos a escribir un código para intentar conservar la etiqueta 'gameType', ya que la considero bastante relevante para nuestro análisis
#Este es quizás el bloque más 'arriesgado', ya que nos estamos basando en las fechas aproximadas en las que comienzan los playoffs (aún así, las fechas
#conservan un patrón bastante fuerte):
#Creamos, en primer lugar, una máscara booleana para abarcar los partidos con el 'gameType' = 'Not informed', y que se juegan en fechas de playoffs
#(aprox de mediados de abril a junio)
condicion_playoffs = ((df_equipos['gameType'] == 'Not informed') & (
        ((df_equipos['game_month'] == 'April') & (df_equipos['game_day'].astype('int64') > 15)) |
        (df_equipos['game_month'] == 'May') |
        (df_equipos['game_month'] == 'June')))
#Asignamos "Playoffs" solo a esas filas
df_equipos.loc[condicion_playoffs, 'gameType'] = 'Playoffs'
#Creamos otr máscara para los casos restantes que, después de aplicar la primera, siguen siendo 'Not informed'
condicion_regular_season = df_equipos['gameType'] == 'Not informed'
#Asignamos "Regular season" a dichos partidos
df_equipos.loc[condicion_regular_season, 'gameType'] = 'Regular season'
#Y con esto hemos eliminado varias columnas que no necesitábamos, y hemos sustituidos los nulos de una columna relevante

#Columna 'coachId': Esta columna no aporta información relevante, y está compuesta casi íntegramente por valores nulos,
#así que la eliminamos directamente.
df_equipos.drop(columns = ['coachId'], inplace = True)

#Columna 'gameLabel', 'gamesubLabel, 'seriesGameNumber': Estas columnas aportan una información más específica del tipo de
#partido que se disputó, pero la situación real es la siguiente: el ~90% de los partidos que se juegan son de temporada regular,
#y por tanto no tienen una gameLabel o gameSubLabel asignada, ya que ésta sólo figuran para partidos especiales, como las fases
#de los playoffs y los partidos all-star (los cuales eliminaremos posteriormente). El seriesGameNumber, por su parte, indica el
#número de partido dentro de una serie de partidos, y ocurre un poco lo mismo que con las otras dos. Así que tomo la decisión de
#eliminar estas 3 columnas directamente
df_equipos.drop(columns = ['gameLabel', 'gameSubLabel', 'seriesGameNumber'], inplace = True)

#Columna 'seed': Esta columna sólo aporta la posición en la que termina el equipo la temporada regular, y por tanto la posición
#en la que entra en playoffs; por tanto, está compuesta casi íntegramente por valores nulos, así que la eliminamos directamente,
#ya que tampoco es información crítica.
df_equipos.drop(columns = ['seed'], inplace = True)

#Columnas 'reboundstTeam', 'TurnoversTeam: Como indico en el diccionario correspondiente de este conjunto de datos, desconozco el
#significado de estas dos columnas, ya que ya disponemos de columnas con los valores totales de rebotes y pérdidas. En la fuente
#de los datos tampoco se especifica su significado, así que decido eliminarlas directamente.
df_equipos.drop(columns = ['reboundsTeam', 'turnoversTeam'], inplace = True)

#Columnas 'ot1Points', 'ot2Points', 'otAllPoints': Columnas que hacen referencia a los puntos anotados por cada equipo en los diferentes
#tiempos de prórroga(en caso de que los haya habido). Siguiendo el razonamiento que hemos aplicado para las columnas 'q1Points' y similares,
#y considerando además la cantidad de valores nulos de estas columnas al ser la prórroga un evento poco probable, eliminamos también estas
#columnas
df_equipos.drop(columns = ['ot1Points', 'ot2Points', 'otAllPoints'], inplace = True)
# print(df_equipos.isna().sum())
# print(df_equipos.isnull().sum())
# print(df_equipos.shape)
#Vemos que, una vez finalizado este bloque, nos hemos quedado con un dataframe de 137,343 filas x 36 columnas, con un total de 0 valores nulos


#4. BLOQUE DE FILTRADO DE DATOS Y ELIMINACIÓN DE COLUMNAS (NO NULAS)
#Al ser un conjunto de datos de gran tamaño, vamos a aplicar ciertos filtros para acotar nuestro análisis, y poder quedarnos solamente con los
#que más nos interesan.
#COLUMNA 'game_year'
df_equipos_filtr1 = df_equipos[df_equipos['game_year'].between(1985,2026, inclusive = 'both')] #Vamos a estudiar este rango de años por un motivo:
    #Hasta 1985, varias de las estadísticas de equipo disponibles en la tabla se empiezan a medir a partir de X año, otras se van midiendo de manera
    #intermitente, otras se miden sólo en Playoffs, la línea de 3 no aparece hasta finales de los 60, etc. Esto nos valoers nulos, sino que son
    #valores 0 (no son celda vacía). Por el hecho de que varias de las estadísticas se miden de manera intermitente, no he querido eliminar partidos
    #de estos años, ya que no podía establecer el límite al no estar seguro si esa estadística no estaba medida o era 0; además, es interesante ver
    #cuándo se iban incorporando las diferentes estadísticas a lo largo del tiempo. Aún así, para un análisis más sólido, que además me permite
    #acotar un poco los datos, voy a tomar únicamente los partidos jugados a partir del 1985.

#COLUMNA 'gameType'
lista_games = ['Regular Season', 'Playoffs'] #Sólo queremos partidos de temporada regular y playoffs (el play-in tournament
#aún no existía en 2015)
df_equipos_final = df_equipos_filtr1[df_equipos_filtr1['gameType'].isin(lista_games)]

#COLUMNA 'teamId' y 'opponentTeamId': Clave ID interna del conjunto de datos. La tabla con la que vamos a unir no provienen de la misma fuente,
#así que no compartirán el ID; por tanto, las podemos eliminar
df_equipos_final.drop(columns = ['teamId', 'opponentTeamId'], inplace = True)

#COLUMNA 'gameDate': Columna duplicada con la fecha del partido, por tanto la eliminamos
df_equipos_final.drop(columns = ['gameDate'], inplace = True)


#5. BLOQUE DE MODIFICACIÓN DE VALORES Y CREACIÓN DE COLUMNAS
#COLUMNA 'teamCity' y 'teamName': Unimos estas dos columnas (sobreescrbiendo una de ellas para obtener el nombre completo del equipo
df_equipos_final['teamFullName'] = df_equipos_final['teamCity'] + ' ' + df_equipos_final['teamName']
df_equipos_final['opponentTeamFullName'] = df_equipos_final['opponentTeamCity'] + ' ' + df_equipos_final['opponentTeamName']
#Eliminamos por tanto las dos columnas correspondientes a la ciudad del equipo y el equipo rival. No eliminamos las de 'teamName' porque
#las necesitaremos posteriormente
df_equipos_final.drop(columns = ['teamCity', 'opponentTeamCity'], inplace = True)

#COLUMNAS 'home' y 'win': Ahora mismo las columnas están configuradas con valores binarios (0,1) para indicar si el equipo era local (1)
#o visitante(0), y para indicar si el equipo ganó (1) o perdió (0) el partido, respectivamente. Para facilitar futuras visualizaciones de
#los datos
df_equipos_final['home'] = df_equipos_final['home'].replace(1,'Home').replace(0,'Away')
df_equipos_final['win'] = df_equipos_final['win'].replace(1,'Win').replace(0,'Loss')

#COLUMNA TEMPORADA: Considerando que las temporadas abarcan desde octubre de un año hasta junio del siguiente, conociendo el mes y año de cada partido,
#podemos dividir dichos partidos por temporadas, creando una nueva columna para ello:
print(df_equipos_final['game_month'].value_counts()) #Nos aseguramos de los meses de los que disponemos en la lista
def temporada(row): #Definimos la función. Esta función irá por fila, estudiando los valores de game_year y game_month para esa fila. En caso
    #de que el mes esté en la lista de mes1, generará el valor de la temporada en formato "año-1/año"; si el mes está en la lista mes2, entonces
    #generará la temporada con el formato "año/año+1"
    month = row['game_month']
    year = row['game_year']
    mes1 = ['January','February','March','April','May','June']
    mes2 = ['October','November','December']
    if month in mes1:
        return f'{year - 1}/{year}'
    elif month in mes2:
        return f'{year}/{year + 1}'
    else:
        return 'Not informed'
df_equipos_final['Season']= df_equipos_final.apply(temporada, axis = 1) #Aplicamos al función a todo el df, especificando axis = 1, para indicarle a
#la función que debe ir fila por fila

#COLUMNA 'gameID': Con esta columna ocurre algo similar a la eliminada anteriormente 'coachId'; es un identificador interno del partido, que no se puede
#extrapolar a tablas que provengan de distintas fuentes. Por ello, vamos a crear nuestro propio ID, similar al que tenemos en la segunda tabla, para poder
#unirlas más fácilmente. Lo haremos combinando las siglas del equipo.
df_equipos_final['Game_ID'] = (df_equipos_final['game_year'].astype(str) +
                               df_equipos_final['game_month_num'].astype(str).str.zfill(2) +
                               df_equipos_final['game_day'].astype(str).str.zfill(2) + #Usamos zfill para llenar con un 0 los días que solo tengan un dígito
                               df_equipos_final['teamName'].str.upper().str[0:3])
#Una vez creado el nuevo 'Game_ID', podemos eliminar el 'gameId' interno que venía con la tabla; además, la columna game_month_num ya ha cumplido su función,
#que era asistir en la creación de este nuevo 'Game_ID', así que ya las podemos eliminar
df_equipos_final.drop(columns = ['gameId','opponentTeamName', 'game_month_num'], inplace = True)
#Por su parte, vamos a conservar la columna de 'teamName', para homogeneizar el gameID que crearemos en la segunda tabla
print(df_equipos_final.info())

#Finalmente, reorganizamos y renombramos las columnas en nuestro dataframe:
df_equipos_final = df_equipos_final[['Game_ID','gameDateTimeEst', 'game_day', 'game_month', 'game_year', 'Season', 'gameType',
                                     'teamName', 'teamFullName', 'home', 'opponentTeamFullName', 'win', 'teamScore', 'opponentScore',
                                     'assists', 'blocks', 'steals', 'fieldGoalsAttempted', 'fieldGoalsMade', 'fieldGoalsPercentage',
                                     'threePointersAttempted', 'threePointersMade', 'threePointersPercentage','freeThrowsAttempted',
                                     'freeThrowsMade', 'freeThrowsPercentage', 'reboundsDefensive','reboundsOffensive',
                                     'reboundsTotal', 'foulsPersonal', 'turnovers', 'plusMinusPoints', 'numMinutes']]

df_equipos_final.rename(columns = {
    'Game_ID': 'Game_ID',
    'gameDateTimeEst': 'Date_Time',
    'game_day': 'Game_Day',
    'game_month': 'Game_Month',
    'game_year': 'Game_Year',
    'Season': 'Season',
    'gameType': 'Game_Type',
    'teamName': 'Team_Name',
    'teamFullName': 'Team_Name2',
    'home': 'Home/Away',
    'opponentTeamFullName': 'Opponent_Name',
    'win': 'Win/Loss',
    'teamScore': 'Team_Score',
    'opponentScore': 'Opponent_Score',
    'assists': 'Assists',
    'blocks': 'Blocks',
    'steals': 'Steals',
    'fieldGoalsAttempted': 'FG_Attempted',
    'fieldGoalsMade': 'FG_Made',
    'fieldGoalsPercentage': 'FG_%',
    'threePointersAttempted': '3PT_Attempted',
    'threePointersMade': '3PT_Made',
    'threePointersPercentage': '3PT_%',
    'freeThrowsAttempted': 'FT_Attempted',
    'freeThrowsMade': 'FT_Made',
    'freeThrowsPercentage': 'FT_%',
    'reboundsDefensive': 'Rebounds_DEF',
    'reboundsOffensive': 'Rebounds_OFF',
    'reboundsTotal': 'Rebounds_TOT',
    'foulsPersonal': 'Personal_Fouls',
    'turnovers': 'Turnovers',
    'plusMinusPoints': '+/-_Score',
    'numMinutes': 'Total Minutes'
}, inplace = True)
#Ajustamos algunos formatos par aportarle mayor homogeneidad a los tipos dentro de la tabla
df_equipos_final['Game_Day'] = df_equipos_final['Game_Day'].astype('int64')
df_equipos_final['Game_Year'] = df_equipos_final['Game_Year'].astype('int64')
df_equipos_final['Home/Away'] = df_equipos_final['Home/Away'].astype(str)
df_equipos_final['Win/Loss'] = df_equipos_final['Win/Loss'].astype(str)
#Hacemos un reset_index al final (eliminando el antiguo), y tras esto un último print para confirmar que el código funciona en su totalidad
df_equipos_final = df_equipos_final.reset_index(drop = True)
print(df_equipos_final.info())
print(df_equipos_final.head(10))
#Y con esto tendríamos preparado nuestro primer conjunto de datos limpio y ordenado

#6. GUARDADO DE ESTADÍSTICAS DESCRIPTIVAS EN ARCHIVO .CSV
#En este paso he extraído las estadísticas descriptivas de todas las columnas numéricas, y tras esto, guardarlas en un archivo .csv.
descripcion_principal = df_equipos_final.select_dtypes('float64', 'int64').describe()
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS', exist_ok = True)
descripcion_principal.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS/descriptive_statistics_Teams.csv')

#7. GUARDADO DE LA TABLA LIMPIA EN .CSV
#Una vez hemos terminado el EDA de nuestra tabla principal, guardamos los datos en formato .csv. Esto nos permitirá importar
# este .csv de nuevo como un dataframe en un nuevo archivo .py, que estará destinado a realizar el merge con la tabla secundaria.
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS', exist_ok = True)
df_equipos_final.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS/01_EDA_TeamStatistics.csv')

