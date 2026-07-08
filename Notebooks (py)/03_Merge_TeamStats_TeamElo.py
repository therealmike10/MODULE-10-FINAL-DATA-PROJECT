#Una vez hemos

#1. BLOQUE DE IMPORTACIÓN DE MÓDULOS
import pandas as pd
import numpy as np
import os

#2.BLOQUE DE CARGA DE NUESTROS DATOS E INFORMACIÓN BÁSICA
#En primer lugar, cargamos los .csv que hemos generado tras limpiar las dos tablas previamente
file1 = "D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS/02_EDA_TeamElo.csv"
file2 = 'D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS/01_EDA_TeamStatistics.csv'
df_elo = pd.read_csv(file1, index_col = 0)
df_teams = pd.read_csv(file2, index_col = 0)
pd.set_option('display.max_columns', None)
print(df_elo.head(10))
print(df_teams.head(10))

#3.AJUSTE DE FORMATOS PREVIOS A UNIÓN
#Antes de unir las tablas, hay que realizar un paso muy importante, que es igualar los formatos de la columna 'Game_ID'
#en ambas tablas para poder realizar el merge correctamente. Esta paso implica cierto conocimiento sobre los datos, ya que
#realizando un análisis de la segunda tabla (Elo) desde su archivo .csv, se puede observar que hay equipos que se llaman,
#igual (mismo Franchise_ID), pero que en cambio tiene valores diferentes en la columna Team_ID. Esto ocurre porque hay
#equipos que, con el paso de los años, cambiaron su nombre en algún momento. Vamos a comprobar esto:
lista1 = df_teams['Team_Name'].unique().tolist()
lista_temp = df_elo['Franchise_ID'].unique().tolist()
lista2 = []
for elemento in lista_temp:
    elemento1 = elemento.title()
    lista2.append(elemento1)
set1 = set(lista1)
set2 = set(lista2)
set_diff1 = set2.difference(set1)
set_diff2 = set1.difference(set2)
#Como podemos ver, hay varios elementos que figura entre los valores de la variable 'Team_Name' (tabla estadísticas), que
#no figuras entre los valores de 'Franchise_ID' de la tabla secundaria (tabla Elo). Al revés también ocurre, sin embargo,
#nos vamos a centrar en los equipos de la tabla principal, ya que por un lado, es la tabla más completa, y por otro lado,
#la tabla secundaria incluye datos de equipos que han durado unos pocos años en la NBA antes de disolverse, los cuales no
#nos interesan para este análisis (ej: 'Floridians', 'Rebels', 'Steamrollers', etc.). Así que nos vamos a ir fijando uno
#por uno en los equipos que están en la tabla principal pero no en la secundaria, para solucionar las disparidades.

#Este paso es muy imoportante, ya que los 3 últimos elementos del 'Game_ID' creado por mí, son las 3 primeras letras del
#equipo que lo juega; por lo tanto, es muy importante que los equipos se llamen igual en mabas tablas.

#SuperSonics: Los Seattle Supersonics desaparecen en 2008 y pasan a ser los Okalhoma City Thunder, pero en la tabla secundaria
#está reflejado como Franchise_ID = 'thunder' - Team_ID = 'sea'
condicion_thunder = ((df_elo['Franchise_ID'] == 'thunder') & (df_elo['Team_ID'] == 'sea'))
df_elo.loc[condicion_thunder, 'Franchise_ID'] = 'SuperSonics'

#Bullets: El nombre de Washington Bullets desaparecen en 1997 y pasan a llamarse Washington Wizards; antes de eso, se llamaron
#de varias maneras: 'Chicago Packers', 'Chicago Zephyrs', 'Baltimore Bullets' y 'Capital Bullets'. En la tabla secundaria,
#todo eso está reflejado como Franchise_ID = 'wizards' - Team_ID = ['bal', 'cap', 'chp', 'chz', 'wsb']
condicion_wizards = (df_elo['Franchise_ID'] == 'wizards') & ((df_elo['Team_ID'].isin(['bal', 'cap', 'chp', 'chz', 'wsb'])))
df_elo.loc[condicion_wizards, 'Franchise_ID'] = 'Bullets' #Por concordancia con la tabla principal, catalogamos a todos como 'Bullets'

#Bobcats: El equipo de Charlotte se llamó Charlotte Hornets en 1988-2002, Charlotte Bobcats en 2004-2014, y volvió a ser
#Charlotte Hornets a partir de 2014. Por ello, tenemos ambos Team_ID bajo el mismo Franchise_ID = 'hornets'
condicion_bobcats = ((df_elo['Franchise_ID'] == 'hornets') & (df_elo['Team_ID'] == 'cha'))
df_elo.loc[condicion_bobcats, 'Franchise_ID'] = 'Bobcats'

#Kings: Los Sacramento Kings se llamaron Rochester Royals en 1948-1957, y Cincinnati Royals en 1957-1972. En la tabla
#secundaria, estos equipos los catalogan como Franchise_ID = 'kings' - Team_ID = ['cin', 'roc']. Sin embargo, en nuestra
#tabla principal figuran como 'Royals'
condicion_kings = ((df_elo['Franchise_ID'] == 'kings') & (df_elo['Team_ID'].isin(['cin','roc'])))
df_elo.loc[condicion_kings, 'Franchise_ID'] = 'Royals'

#Clippers: Este equipo se llamó Buffalo Braves durante 1970-1978, pero en nuestra tabla secundaria se cataloga como
#Franchise_ID = 'clippers', Team_ID = 'buf', mientras que en nuestra tabla principal figura el nombre 'Braves'
condicion_clippers = ((df_elo['Franchise_ID'] == 'clippers') & (df_elo['Team_ID'] == 'buf'))
df_elo.loc[condicion_clippers, 'Franchise_ID'] = 'Braves'

#Los Philadelphia 76ers se llamaron Syracuse Nationals en 1946-1963, pero en nuestra tabla secundaria se cataloga como
#Franchise_ID = 'sixers' - Team_ID = 'syr'. En cambio, en nuestra tabla principal, tenemos a los Nationals.
condicion_sixers = ((df_elo['Franchise_ID'] == 'sixers') & (df_elo['Team_ID'] == 'syr'))
df_elo.loc[condicion_sixers, 'Franchise_ID'] = 'Nationals'

#En relación a este último equipo, es importante fijarse también que lo que la tabla principal cataloa como '76ers', la
#tabla secundaria lo cataloga como 'sixers', que son dos maneras de referirse al mismo equipo. Por tanto, eso hay que
#corregirlo también.
df_elo['Franchise_ID'] = df_elo['Franchise_ID'].replace('sixers', '76ers')

#Volemos a formar las listas y a imprimir las diferencias del set tras los cambios, para comprobar que se han aplicado:
lista1 = df_teams['Team_Name'].unique().tolist()
lista_temp = df_elo['Franchise_ID'].unique().tolist()
lista2 = []
for elemento in lista_temp:
    elemento1 = elemento.title()
    lista2.append(elemento1)
set1 = set(lista1)
set2 = set(lista2)
set_diff2 = set1.difference(set2)
print(set2)
print(set_diff2)
#Vemos que seguimos teniendo tres elementos de diferencia, pero es perfectamente normal, ya que son estos pares de nombres:
    #76ers vs 76Ers
    #Trail Blazers vs Trailblazers
    #Supersonics vs Supersonics
#Son pequeñas diferencias de formato entre nombres de ambas listas que no nos afectan, ya que vamos a usar únicamente las
#3 primeras letras de cada equipo para el Game_ID, así que en este caso las diferencias entre unos y otros no son importantes.

#De esta manera, definimos nuestro Game_ID para la tabla secundaria, tal y como lo habíamos planteado previamente. El gameId
#original de esta tabla tiene como formato 'yyyymmdd0ttt', siendo 'ttt' las primeras tres letras del equipo; por lo tanto,
#podemos reciclar parte de ese formato para crear el nuestro, conservando la fecha, eliminado el 0 que hay en medio y poniendo
#las 3 primeras letras en mayúsculas de los nombres de nuestros equipos modificados
df_elo['Game_ID'] = df_elo['Game_ID'].str[0:8] + df_elo['Franchise_ID'].str[0:3].str.upper()

#4. UNIÓN DE TABLAS CON MERGE()
df_final = df_teams.merge(df_elo, how = 'inner', on = 'Game_ID')
#Hacemos un print de .head() y .info() para comprobar que está todo correcto, y seguimos con las modificaciones
print(df_final.info())
print(df_final.head())

#Ahora que ya hemos unido las dos tablas podemos, en primer lugar, eliminar las variables 'Franchise_ID' y 'Team_ID' de la tabla
#secundaria, así como Team_Name de la tabla principal ya que ofrecen información redundante
df_final.drop(columns = ['Team_Name','Team_ID', 'Franchise_ID'], inplace = True)
df_final.rename(columns = {
    'Team_Name2': 'Team_Name'
}, inplace = True)
print(df_final.info())
print(df_final.head())

#Por último, antes de llevarnos esta tabla a la creación de dashboards, ahora que hemos combinado las dos tablas, podemos
#crear alguna variable más que nos puede resultar de utilidad en el futuro.
#COLUMNA Result vs expectation: Mide el grado de sorpresa de un resultado
df_final['team_won'] = df_final['Win/Loss'].replace('Win', 1).replace('Loss', 0)
df_final['Result/Expect'] = df_final['team_won'] - df_final['Forecast']
df_final.drop(columns = ['team_won'], inplace = True)

#COLUMNA Result_Expect_Classi: Clasifica el grado de sorpresa de un resultado
def classify_surprise(surprise):
    if 1 >= surprise >= 0.75:
        return 'Surprising win'
    elif 0.75 > surprise >= 0.50:
        return 'Unexpected win'
    elif 0.50 > surprise >= 0:
        return 'Expected win'
    if 0 > surprise >= (-0.50):
        return 'Expected loss'
    elif (-0.50) > surprise >= (-0.75):
        return 'Unexpected loss'
    elif (-0.75) > surprise >= (-1):
        return 'Suprising loss'
df_final['Result/Expect_Classi'] = df_final['Result/Expect'].apply(classify_surprise)

#COLUMNA Point margin: Mide la diferencia de puntos entre el equipo y su rival
new_col = df_final['Team_Score'] - df_final['Opponent_Score']
idx = 14
df_final.insert(loc = idx, column= 'Score_Diff', value = new_col)

#COLUMNA Margin category: Categorica la diferencia de puntos en el partido
def classify_margin(margin):
    if margin >= 20:
        return 'Blowout win'
    elif 20 > margin >= 10:
        return 'Comfortable win'
    elif 10 > margin > 0:
        return 'Close win'
    elif margin == 0:
        return 'Tie/Error'
    elif 0 > margin >= -10:
        return 'Close loss'
    elif -10 > margin > -20:
        return 'Comfortable loss'
    else:
        return 'Blowout loss'
new_col2 = df_final['Score_Diff'].apply(classify_margin)
idx2 = 15
df_final.insert(loc = idx2, column= 'Score_Diff_Classi', value = new_col2)
#Un último print para comprobar que está todo correcto:
print(df_final.info())
print(df_final.head())

#7. GUARDADO DE LA TABLA LIMPIA EN .CSV
#Una vez hemos terminado el EDA de nuestra tabla secundaria, guardamos los datos en formato .csv. Esto nos permitirá importar
#este .csv de nuevo como un dataframe en un nuevo archivo .py, que estará destinado a realizar el merge con la tabla principal.
os.makedirs('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS', exist_ok = True)
df_final.to_csv('D:/MIGUEL/DATA ANALYSIS/ThePower - Data Analysis/10.FINAL PROJECT/TABLAS LIMPIAS/03_Merge_TeamStats_TeamElo.csv')