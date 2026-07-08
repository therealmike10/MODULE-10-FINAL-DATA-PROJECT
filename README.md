# MODULE-10-FINAL-DATA-PROJECT

Proyecto final del Módulo 10 del curso **Data & Analytics V3** de ThePower, desarrollado por **Miguel Encinas**.

Este proyecto se centra en el tratamiento completo de un conjunto de datos real relacionado con partidos de la **NBA**, combinando estadísticas de equipo por partido con información basada en el sistema **Elo**. El objetivo principal ha sido aplicar un flujo de trabajo completo de análisis de datos: obtención de datos, limpieza, transformación, unión de tablas, análisis descriptivo, análisis estadístico y creación de dashboards interactivos en **Power BI**.

Esto conjunto de datos ha sido elegido de manera deliberada, ya que uno de mis proyectos en este curso, en concreto el proyecto del Módulo 4 (Dashboards), consisitió en elaborar un Dashboard en Excel con datos de una temporada reciente de la NBA. Escogiendo este conjunto de datos, por tanto, he querido comprobar cómo han evolucionado mis conocimientos y habilidades durante el curso, aplicando esta vez análisis de datos avanzado mediante Python y Power BI.

El análisis parte de dos datasets principales: 'TeamStatistics.csv', con estadísticas de equipo por partido, y 'nbaallelo.csv', con información histórica de Elo, forecast y fuerza relativa de los equipos. Tras el proceso de limpieza y homogeneización, se generó un dataset final llamado '03_Merge_TeamStats_TeamElo.csv', con una estructura a nivel **equipo-partido**. Esto significa que cada partido real aparece normalmente dos veces: una fila desde el punto de vista de cada equipo.

## 🎯 Objetivo del proyecto

El objetivo del proyecto es analizar la evolución histórica del rendimiento de los equipos NBA, el estilo de juego y la capacidad predictiva del sistema Elo a partir de un conjunto de datos completo. Para ello, se han trabajado los siguientes bloques:
- Limpieza profunda de datos crudos.
- Homogeneización de variables y nombres de equipos.
- Creación de nuevas variables analíticas.
- Unión de dos fuentes de datos mediante una clave común ('Game_ID').
- Análisis descriptivo del conjunto de datos final final.
- Análisis estadístico de rendimiento, ventaja local, box score y Elo.
- Creación de un dashboard operativo en Power BI.
- Elaboración de conclusiones a partir de los resultados obtenidos.

## ℹ️ Datos utilizados

### 'TeamStatistics.csv' (Fuente: [Kaggle - NBA Dataset](https://www.kaggle.com/datasets/eoinamoore/historical-nba-data-and-player-box-scores))

Tabla con estadísticas de equipo a nivel partido. Incluye, entre otras variables:

- Fecha del partido.
- Equipo y rival.
- Condición local/visitante.
- Resultado del partido.
- Puntos anotados y recibidos.
- Asistencias.
- Rebotes ofensivos, defensivos y totales.
- Robos.
- Tapones.
- Faltas personales.
- Pérdidas.
- Tiros de campo, triples y tiros libres intentados/anotados.
- Tipo de partido: 'Regular Season' o 'Playoffs'.

### 'nbaallelo.csv' (Fuente: [DataHub - FiveThirtyEight](https://datahub.io/fivethirtyeight/nba-elo))

Tabla histórica con datos de Elo para partidos NBA. Incluye variables como:

- Elo del equipo antes del partido.
- Elo del rival antes del partido.
- Elo del equipo tras el partido.
- Variación de Elo.
- Forecast o probabilidad estimada de victoria.
- Clasificación del equipo como favorito o underdog.


## ⏩ Flujo de trabajo seguido

### 1. Exploración y limpieza de 'TeamStatistics.csv'

En el archivo '01_EDA_TeamStatistics.csv.py' se llevó a cabo la limpieza de la tabla principal de estadísticas de equipo; las principales tareas realizadas fueron:

- Carga inicial del conjunto de datos con 'pandas'.
- Revisión de dimensiones, tipos de datos y valores nulos.
- Conversión de fechas a formato 'datetime'.
- Creación de columnas temporales como 'Game_Day', 'Game_Month', 'Game_Year' y 'Season'.
- Eliminación de partidos All-Star o registros incompletos.
- Tratamiento específico de valores nulos en estadísticas de juego.
- Validación de la columna 'numMinutes', manteniendo valores coherentes con partidos NBA estándar y prórrogas.
- Eliminación de columnas con una proporción elevada de valores nulos o baja utilidad analítica.
- Conversión de variables binarias en categorías interpretables.
- Creación de un identificador propio de partido/equipo: 'Game_ID'.
- Renombrado final de columnas para hacerlas más claras y homogéneas.

### 2. Exploración y limpieza de 'nbaallelo.csv'

En el archivo '02_EDA_TeamElo.py' se realizó la preparación de la tabla Elo; las principales tareas realizadas fueron:

- Carga del conjunto de datos 'nbaallelo.csv'.
- Resolución de un problema de lectura del archivo debido a filas con columnas adicionales.
- Eliminación de columnas poco relevantes o redundantes para el análisis final.
- Conservación de las variables Elo más importantes.
- Creación de nuevas variables:
- Renombrado de columnas para homogeneizarlas con la tabla principal.

### 3. Unión de tablas y creación del conjunto de datos final

En el archivo '03_Merge_TeamStats_TeamElo.py' se realizó la unión de las dos tablas limpias creadas previamente.

La parte más importante de este proceso fue la homogeneización de nombres históricos de equipos y franquicias, ya que varios equipos cambiaron de nombre o ciudad a lo largo de los años. Después de cuadrar estos nombres, se creó un 'Game_ID' compatible entre ambas tablas y se realizó un 'merge()' interno sobre dicha columna.

Además, se crearon nuevas variables analíticas, como 'Score_Diff', 'Score_Diff_Classi', 'Result/Expect' y 'Result/Expect_Classi'.Finalmente, el conjunto de datos quedó compuesto por aproximadamente:

- **71.984 filas**.
- **47 columnas**.
- **31 temporadas**, desde '1984/1985' hasta '2014/2015'.
- **36 equipos/franquicias**.
- **35.992 partidos reales aproximados**, considerando que cada partido aparece dos veces en formato equipo-partido.

## 📊 Dashboards en Power BI
El archivo DASHBOARD_FINAL_PROJECT.pbix incluye cuatro dashboards, cada uno estudiando varios aspectos del conjunto de datos.
### Dashboard 1: NBA Overview
Este dashboard ofrece una visión general del conjunto de datos. Incluye KPIs principales como Total Team-Games, Total Seasons, Average Team Score, o Win %. También incluye visualizaciones sobre la evolución de la anotación media por temporada, la distribución por tipo de partido y la comparación de victorias entre local y visitante. Este dashboard sirve como página inicial del informe y da una perspectiva rápida de las principales tendencias del conjunto de datos.

### Dashboard 2: Team Performance
Este dashboard se centra en el rendimiento de los equipos. Incluye KPIs como número de victorias, derrotas, Win %, puntos anotados, puntos recibidos y margen medio de puntos. También incluye un ranking de equipos por porcentaje de victorias y un gráfico de dispersión que compara rendimiento ofensivo y defensivo. Este dashboard permite explorar qué equipos han rendido mejor en función de los filtros seleccionados, y si su rendimiento se explica más por capacidad ofensiva o defensiva.

### Dashboard 3: Game Style & Box Score Analysis
Este dashboard analiza el estilo de juego y las estadísticas de box score, que incluye KPIs de puntos, FG %, triples intentados, 3PT %, rebotes, asistencias y pérdidas.
Uno de los elementos principales es la evolución de los tiros de campo y triples intentados por temporada, donde se observa claramente el aumento del número de triples intentados conforme pasan los años. También se incluye una comparación de métricas de box score entre victorias y derrotas. Su objetivo es mostrar cómo se juega y qué estadísticas están asociadas con ganar.

### Dashboard 4: Elo & Forecast Accuracy
Este dashboard analiza la capacidad predictiva del sistema Elo. Incluye KPIs como Favorite Win %, Average Forecast, Average Score Diff. o Average Elo Variation.
También incluye un gráfico de Win % en función de la Favorite_Category, un recuento de resultados esperados e inesperados, y un gráfico de dispersión que relaciona Elo_Diff_PreGame con Score_Diff.
Este dashboard muestra que el sistema Elo no predice los resultados de manera perfecta, pero sí que ofrece una orientación clara: los favoritos ganan más y las diferencias mayores de Elo tienden a asociarse con márgenes mayores en el marcador.


## 🛠️ Herramientas y lenguajes utilizados

- **Python**
- **pandas**
- **NumPy**
- **Power BI**
- **DAX**
- **Power Query**
- **Visual Studio Code**
- **GitHub**

⚠️ Los scripts contienen rutas locales absolutas, por lo que para ejecutar el proyecto en otro ordenador sería necesario adaptar dichas rutas a la estructura local del nuevo equipo.\
\
⚠️ Para la elaboración del código, no se usaron herramientas de IA generativa, el código fue generado de manera íntegra por el usuario.\
\
⚠️ En ocasiones puntuales, se utilizó inteligencia artificial como asistente (sin generación directa de código) para enocontrar el fallo en un código que el usuario no fue capaz de encontrar por sí mismo.\
\
⚠️ Las herramientas de auto-completado de código, como la extensión 'auto​Docstring', fueron desactivadas para este ejercicio, favoreciendo la generación de código original por parte del usuario.\

## ↪️ Conclusiones

En general, este proyecto me ha permitido:

1. Trabajar con un flujo completo de análisis de datos usando Python en el entorno de Visual Studio Code para analizar dos conjuntos de datos reales, los cuales recopilaban datos históricos de la NBA.
2. Usar Python para cargar, limpiar, transformar y unir datos procedentes de archivos .csv de diferentes fuentes.
3. Seguir diferentes protocolos para tratar valores nulos, columnas redundantes y variables con formatos poco adecuados, analizando el conjunto de datos en general para cada decisión.
4. Crear nuevas variables categóricas para facilitar el análisis y la visualización de los datos.
5. Usar Power Bi para generar dashboards potentes orientados a estudiar varios aspectos del conjunto de datos que hemos creado al unir las dos tablas iniciales, enriqueciendo la información obtenida a partir de dichas tablas.
6. En general, comprender el ciclo de vida completo del dato y aplicar un flujo de trabajo extrapolable a un caso real.
