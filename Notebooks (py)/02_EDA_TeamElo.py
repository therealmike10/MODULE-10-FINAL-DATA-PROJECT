#En este segundo archivo .py vamos a realizar la exploración y limpieza de los datos correspondientes a la segunda tabla
#con la que vamos a trabajar: nbaallelo.csv. Dicha tabla contiene las estadísticas, a nivel de los equipos, de todos los
#partidos disputados en la NBA, desde 1946 hasta 2015.
#En esta tabla podemos encontrar muchos datos que teníamos en nuestra tabla inicial: nombres de equipos, fecha, año, puntos
#totales, etc.
#Sin embargo, tenemos también varias estadísticas donde radica su interés, relacionadas con el Elo. El Elo es un sistema
#de puntuación que intenta medir la fuerza relativa de un equipo.Se aplica a multitud de deportes, y La idea básica es que
#cada equipo tiene una puntuación Elo; cuanto mayor es el Elo, más fuerte se considera el equipo. Por tanto antes de un partido,
#la diferencia entre los Elo de los dos equipos se puede transformar en una probabilidad de victoria; después del partido, los
#Elo se actualizan según el resultado. Por lo tanto, la idea central es que no todas las victorias valen lo mismo.

#1. BLOQUE DE IMPORTACIÓN DE MÓDULOS
import pandas as pd
import numpy as np
import os

#2.BLOQUE DE CARGA DE NUESTROS DATOS E INFORMACIÓN BÁSICA
#En primer lugar, cargamos nuestro archivo csv en un dataframe de pandas. Le indicamos que la primera columna va a ser nuestra columna de indexación,
#ya que es la columna con el número de la entrada de los datos.
file1 = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/DATOS/nbaallelo.csv"
#He dejado esta última línea comentada, ya que si aplico directamente el pd.read_csv, obtengo un error del siguiente tipo:
#"pandas.errors.ParserError: Error tokenizing data. C error: Expected 23 fields in line 36084, saw 24"
#Al parecer, algunas filas tienen más valores que el resto, por lo tanto, mientras pandas esperaba 23 variables por fila, en alguna recibe 24. Vamos a
#hacer una comprobación en el índice que indica, gracias al comando 'open' aplicado a nuestro archivo, combinado con un bucle for con condicional if:
with open("D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/DATOS/nbaallelo.csv", "r", encoding="utf-8") as file:
    for i, line in enumerate(file, start=1):
        if i in range(36080,36085):
            print(i, line.count(","), line)
#Efectivamente, en dicho índice (y de hecho en el siguiente) tenemos 23 comas, cuando en el resto tenemos 22. Si vamos al .csv y lo convertimos a .xlsx,
#corroboramos esto observando que las dos últimas columnas no tienen nombre, y que sólo hay valores en algunas filas. Por tanto, la primera limpieza que
#haremos en este conjunto de datos es cargarlo directamente sin las dos últimas columnas, que no parecen aportar información relevante vistas en Excel:
pd.set_option('display.max_columns', None)
df_elo = pd.read_csv(file1, index_col = 0, usecols=range(0,23))
print(df_elo.head(10))
print(df_elo.info())
print(df_elo.isna().sum())
print(df_elo.isnull().sum())

#Vamos a seguir el mismo procedimiento que en el dataframe anterior, y vamos a dividir el EDA en bloques.
#3. BLOQUE MODIFICACIÓN COLUMNAS + ELIMINACIÓN/SUSTITUCIÓN DE NaN, null
#COLUMNA 'notes': Con respecto a valores null, parece que esta tabla de datos no tiene una gran cantidad de valores null
#a priori, salvo en la columna 'notes'
df_elo['notes'].unique()
#Observando sus valores únicos, parece que son simples anotaciones añadidas en algunos de los partidos, pero como podemos
#comprobar, no son muy relevantes, y la mayoría de partidos tienen este valor nulo, así que procedemos a eliminar la columna
df_elo.drop(columns = ['notes'], inplace = True)
print(df_elo.isna().sum())
print(df_elo.isnull().sum())
#No hay más valores nulos en otras columnas, así que pasamos al siguiente bloque

#4. BLOQUE DE FILTRADO DE DATOS Y ELIMINACIÓN DE COLUMNAS (NO NULAS)
#COLUMNA 'lg_id': Nombre de la liga en el momento que se juega el partido. Aunque la mayoría del tiempo se ha llamado NBA,
#hubo momentos en los que se llamó ABA. No nos interesa esta variable, así que la eliminamos:
df_elo.drop(columns = ['lg_id'], inplace = True)

#COLUMNA '_iscopy': Para cada partido, tenemos dos filas de datos: la que estudia al equipo 'A' contra el equipo rival 'B,
#y por consecuencia, la que estudia al equipo 'B' con el equipo rival 'A'. Esta columna indica simplemente si la fila en
#cuestión ya ha aparecido (en referencia al otro equipo). Columna importane originalmente, pero con el sistema de 'Game_ID'
#que hemos planteado en la tabla anterior (y que vamos a extrapolar aquí), esta columna ya no hará falta.
df_elo.drop(columns = ['_iscopy'], inplace = True)

#COLUMNA 'year_id','date_game': Indica el año y la fecha en la que se jugó el partido. Estas columnas ya las traemos del
#primer conjunto de datos, así que no nos harán falta:
df_elo.drop(columns = ['year_id', 'date_game'], inplace = True)

#COLUMNA 'seasongame': Número de partido de ese equipo en la temporada. No aporta información relevante, así que la eliminamos
df_elo.drop(columns = ['seasongame'], inplace = True)

#COLUMNA 'is_playoff': Columna que nos indica si el partido es de playoffs (1) o no (0). Esta información ya está incluida
#en el Game_Type de nuestro primer conjunto de datos, así que también la eliminamos.
df_elo.drop(columns = ['is_playoffs'], inplace = True)

#COLUMNAS 'pts', 'opp_pts': Puntos totales anotados por el equipo y el equipo rival en el partido. Esta información también
#nos vendrá desde la primera tabla, así que eliminamos estas columnas para no solapar información
df_elo.drop(columns = ['pts', 'opp_pts'], inplace = True)


#COLUMNAS 'opp_id', 'opp_fran': Estas columnas se refieren a un ID de 3 letras del equipo rival, así como su nombre (sin
#incluir la ciudad). Esta información la tenemos en la tabla anterior, y no la vamos a necesitar para crear el 'Game_ID',
#así que podemos eliminar estas variables de la tabla
df_elo.drop(columns = ['opp_id', 'opp_fran'], inplace = True)

#COUMNAS 'game_location' y 'game_result': Nos aportan información acerca de si el equipo en cuestión era local (h) o era
#visitante (a), y nos dice si el equipo ganó (w) o perdió (l). Esta información nuevamente la traemos desde nuestra tabla
#anterior, así que la eliminamos de esta tabla:
df_elo.drop(columns = ['game_location', 'game_result'], inplace = True)

#COLUMNA 'win_equiv': Número equivalente de victorias (en una temporada de 82 partidos) para un equipo dado su valor
#de 'elo_n'. Es decir, una predicción o extrapolación de victorias esperadas con ese elo. No nos interesa tanto como las
#diferencias de elo, así que la podemos eliminar
df_elo.drop(columns = ['win_equiv'], inplace = True)


#5. BLOQUE DE MODIFICACIÓN DE VALORES Y CREACIÓN DE COLUMNAS
#El resto de columnas no nombradas anteriormente no necesitan modificación, ya que  la mayoría son númericas y están en
#el formato correcto. Adjunto breve explicación de las mismas:
    #COLUMNA 'team_id': ID del equipo, formado por un código de 3 letras
    #COLUMNA 'fran_id': ID de la franquicia, es decir, la parte del nombre del equipo que no es la ciudad
    #COLUMNA 'elo_i': Elo inicial del equipo en cuestión, es decir, su puntuación de 'fortaleza' antes de jugar el partido.
    #COLUMNA 'elo_n': Elo final del equipo en cuestión, es decir, su puntuación de 'fortaleza' después de jugar el partido.
    #COLUMNA 'opp_elo_i': Elo inicial del equipo rival, es decir, su puntuación de 'fortaleza' antes de jugar el partido.
    #COLUMNA 'opp_elo_n': Elo final del equipo rival, es decir, su puntuación de 'fortaleza' después de jugar el partido.
    #COLUMNA 'forecast': Oportunidades de ganar, basadas en el Elo, para el equipo en cuestión de esa fila, basado en las
    #clasificaciones de elo y en el lugar donde se juega el partido

#COLUMNA NUEVA 'elo_change': Diferencia de elo antes y después de disputar el partido para el equipo en cuestión
df_elo['elo_change'] = df_elo['elo_n'] - df_elo['elo_i']

#COLUMNA NUEVA 'elo_diff_pre': Diferencia de elo entre los dos equipos antes del partido
df_elo['elo_diff_pre'] = df_elo['elo_i'] - df_elo['opp_elo_i']


#COLUMNA NUEVA 'Favorite by elo': Determina, en base a la diferencia de elo inicial entre ambos equipos, si el equipo es
#'Favorite' (>0) o 'Underdog' (<0)
def favorite_elo(elo_dif):
    if elo_dif > 0:
        return 'Favorite'
    elif elo_dif < 0:
        return 'Underdog'
    else:
        return 'Even'
df_elo['Favorite_Elo']= df_elo['elo_diff_pre'].apply(favorite_elo)

#COLUMNA NUEVA 'Favorite by forecast': Determina, en base a la predicción, si el equipo es #'Favorite' (>0.5) o 'Underdog' (<0.5)
def favorite_forecast(forecast1):
    if forecast1 >= 0.5:
        return 'Favorite'
    elif forecast1 < 0.5:
        return 'Underdog'
    else:
        return 'Even'
df_elo['Favorite_Forecast']= df_elo['forecast'].apply(favorite_forecast)



#COLUMNA NUEVA 'Forecast_category': Determina, en base a la predicción, el grado de favorito o de underdog del equipo en cuestión.
def classify_forecast(forecast2):
    if forecast2 >= 0.75:
        return 'Strong favorite'
    elif 0.75 > forecast2 >= 0.60:
        return 'Favorite'
    elif 0.60 > forecast2 >= 0.40:
        return 'Even matchup'
    elif 0.40 > forecast2 >= 0.25:
        return 'Underdog'
    else:
        return 'Strong underdog'
df_elo['Forecast_category'] = df_elo['forecast'].apply(classify_forecast)

print(df_elo.head(10))
print(df_elo.info())

#Finalmente, reorganizamos y renombramos las columnas en nuestro dataframe:
df_elo = df_elo[['game_id', 'team_id', 'fran_id', 'elo_i', 'opp_elo_i', 'elo_diff_pre', 'Favorite_Elo', 'elo_n',
                 'elo_change', 'opp_elo_n', 'forecast', 'Favorite_Forecast', 'Forecast_category']]

df_elo = df_elo.rename(columns = {
    'game_id': 'Game_ID',
    'team_id': 'Team_ID',
    'fran_id': 'Franchise_ID',
    'elo_i': 'Elo_Before',
    'opp_elo_i':'Elo_Before_Rival',
    'elo_diff_pre':'Elo_Diff_PreGame',
    'Favorite_Elo':'Favorite_by_Elo',
    'elo_n':'Elo_After',
    'elo_change':'Elo_Variation',
    'opp_elo_n':'Elo_After_Rival',
    'forecast': 'Forecast',
    'Favorite_Forecast':'Favorite_by_Forecast',
    'Forecast_category':'Favorite_Category'
})
#Hacemos un reset_index al final (eliminando el antiguo), y tras esto un último print para confirmar que el código funciona en su totalidad
df_elo = df_elo.reset_index(drop = True)
print(df_elo.info())
print(df_elo.head(10))

#6. GUARDADO DE ESTADÍSTICAS DESCRIPTIVAS EN ARCHIVO .CSV
#En este paso he extraído las estadísticas descriptivas de todas las columnas numéricas, y tras esto, guardarlas en un archivo .csv.
df_stats = df_elo.select_dtypes('float64').describe()
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS', exist_ok = True)
df_stats.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS/descriptive_statistics_Elo.csv')


#7. GUARDADO DE LA TABLA LIMPIA EN .CSV
#Una vez hemos terminado el EDA de nuestra tabla secundaria, guardamos los datos en formato .csv. Esto nos permitirá importar
#este .csv de nuevo como un dataframe en un nuevo archivo .py, que estará destinado a realizar el merge con la tabla principal.
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS', exist_ok = True)
df_elo.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS/02_EDA_TeamElo.csv')