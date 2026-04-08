# RIC
Para extraer datos de la SEC (Superintendencia de Electricidad y Combustibles) en Chile de forma automatizada, el proceso tiene ciertos matices técnicos, ya que no existe una API pública abierta de tipo "REST" tradicional para búsquedas de texto libre dentro de documentos normativos como los RIC (Pliegos del Reglamento de Instalaciones de Consumo).

Aquí te presento la estrategia técnica para lograr lo que buscas:

1. El Desafío de los Datos
La SEC publica los RIC y RIN principalmente en formato PDF. Para buscar una frase exacta como "altura máxima de", no basta con una consulta de base de datos; necesitas un flujo de ETL (Extracción, Transformación y Carga).

Estructura de la solución:
Web Scraping / Descarga: Obtener los archivos PDF desde el portal normativo de la SEC.

Procesamiento de PDF: Convertir esos documentos a texto plano mediante librerías de Python.

Indexación y Búsqueda: Crear un script que recorra los textos buscando la coincidencia exacta.
