# SDR_InVEST_Bug_Fix
Este código realiza la corrección del modelo SDR-InVEST para un esquema comparativo entre escenario BaU y NBS.
Básicamente, este código garantiza que, la exportación de sedimentos del escenario de intervención de Soluciones Basadas en la Naturaleza (NBS) sea siempre menor o igual al escenario degradado (BaU).
Esta corrección fue necesario realizarla debido a que el modelo de SDR realiza la asignación espacial de los parámetros **usle_c** y **usle_p** en un ráster que tiene la misma dimensión del Modelo de Elevación Digital (DEM). En principio, la tabla de parámetros biofísicos, solicita para cada cobertura estos dos parámetros. En este sentido, cuando la cobertura tiene un tamaño de pixel menor al DEM, el SDR realiza una estadística tomando como valor de estos dos parámetros, el que mayor proporción represente al interior del pixel del DEM. Para ejemplificar esto, imaginemos que el DEM que introducimos al SDR presenta una resolución espacial de **1000 metros** y el raster de cobertura una resolución de **250 metros**. En total, 1 pixel del DEM contendría 16 pixeles de cobertura. Ahora bien, supongamos que 10 pixeles tienen un valor de **usle_c = 0.001** y los 6 restantes tienen un valor de **usle_c = 0.0005**. Lo que hace el SDR es tomar el valor que presentan la mayor cantidad de pixeles, este caso seria 0.001. Esto trae una complicación y es que, si las implementaciones no cambian la proporción del pixel mas grande, no se genera un beneficio.

Para ejecutar este código en waterproof, es necesario tener las rutas de salida del SDR para los escenarios BaU y NBS, así como también el sufijo de la región de trabajo. La configuración se realiza de la siguiente manera:

	# ----------------------------------------------------------------------------------------------------------------------
	# Tester
	# ----------------------------------------------------------------------------------------------------------------------
	# Input Data
	FilePath_BaU = r'C:\Users\TNC\Box\Tmp\00-Tester_Final_WaterProof\La_Colorada\Step-04_InVEST-BaU\03-SDR'
	FilePath_NBS = r'C:\Users\TNC\Box\Tmp\00-Tester_Final_WaterProof\La_Colorada\Step-05_InVEST-NBS\YEAR_5\SbN_Year_5\03-SDR'
	Region       = r'Tester'

	# Run
	SDR_BugFix(FilePath_BaU, FilePath_NBS, Region)
