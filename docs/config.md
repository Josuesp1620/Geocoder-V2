# Configuración del Geocoder

## Registrar tu archivo de configuración personalizado

Un archivo de configuración de geocoder es simplemente un archivo Python que define algunas claves. La ubicación predeterminada es `/etc/geocoder/geocoder.conf`. Pero puede estar en cualquier otro lugar de tu sistema, y necesitas definir una variable de entorno que apunte a él si quieres una ubicación especial:

    export geocoder_CONFIG_MODULE=path/to/local.py

También puedes usar el argumento `--config` al ejecutar la línea de comandos `geocoder`.

El archivo de configuración predeterminado está en `geocoder/config/default.py`.

## Usar variables de entorno

Cualquier clave de configuración específica se puede declarar usando una variable de entorno, usando la clave en sí, precedida por `geocoder_`. Por ejemplo, para anular `BATCH_WORKERS`, uno puede hacer algo como esto:

    geocoder_BATCH_WORKERS=12 geocoder batch

## Configuración del entorno

Algunas configuraciones se utilizan para definir cómo geocoder manejará el sistema en el que está instalado.

#### REDIS (dict)
Define la configuración de la base de datos Redis:

    REDIS = {
        'host': 'localhost',
        'port': 6379,
        'db': 0
    }

Por defecto, al usar el `RedisStore` para documentos, índices y documentos
se almacenarán en dos bases de datos Redis diferentes.
Puedes controlar esos detalles usando subdiccionarios `indexes` y/o `documents`, por ejemplo:

    REDIS = {
        'host': 'myhost',
        'port': 6379,
        'indexes': {
            'db': 11,
        },
        'documents': {
            'db': 12,
        }
    }

Si tus hosts son diferentes, puedes definirlos así:

    REDIS = {
        'port': 6379,
        'indexes': {
            'host': 'myhost1',
            'db': 11,
        },
        'documents': {
            'db': 12,
            'host': 'myhost2',
        }
    }

Y, por supuesto, lo mismo para el puerto.

Para usar Redis a través de un socket Unix, utiliza la clave `unix_socket_path`.

#### LOG_DIR (ruta)
Ruta al directorio donde geocoder escribirá sus archivos de registro e historial. También
se puede anular desde la variable de entorno `geocoder_LOG_DIR`.

    LOG_DIR = 'path/to/dir'

Esta configuración predeterminada es la carpeta raíz del paquete geocoder.

## Configuraciones básicas

Un montón de configuraciones que quizás quieras cambiar para adaptar tu instancia personalizada.

Advertencia: verás muchas configuraciones con el sufijo PYPATH(S), esas
esperan ruta(s) a llamables de Python. En el caso de una lista, el orden
importa dado que es una cadena de procesadores.

#### ATTRIBUTION (cadena o dict)

La atribución de los datos que se utilizarán en los resultados de la API. Puede ser una
cadena simple o un dict.

    ATTRIBUTION = "Geosolution S.A.C."    

#### BATCH_WORKERS (int)
Número de procesos en uso al paralelizar tareas como importaciones en lote o
cálculo de ngrams.

    BATCH_WORKERS = os.cpu_count() - 1

#### DOCUMENT_STORE_PYPATH (ruta de Python)
Ruta de Python a una clase de almacenamiento para guardar documentos usando otro motor de base de datos y ahorrar memoria.
Consulta la documentación dedicada en la página de [plugins](plugins.md).

#### EXTRA_FIELDS (lista de dicts)

A veces solo quieres extender [campos predeterminados](#fields-list-of-dicts).

    EXTRA_FIELDS = [
        {"key": "cod_departament"},
        {"key": "cod_province"},
        {"key": "cod_district"},
        {"key": "type"},
    ]

#### FIELDS (lista de dicts)
Los campos del documento *que quieres indexar*. Es una lista de dict, cada uno definiendo
un campo indexado. Claves disponibles:

- **key** (*obligatorio*): la clave del campo en el documento
- **boost**: impulso opcional del campo, define cuán importante es el campo
  en el índice, por ejemplo, usualmente se define un impulso mayor para el campo *name* que para el campo *city* (predeterminado: 1)
- **null**: define si el campo puede ser nulo (predeterminado: True)
- **type**: tipo opcional, puede ser `name` o `id`, para definir NAME_FIELD o ID_FIELD

```
FIELDS = [
    {'key': 'name', 'boost': 4, 'null': False},
    {'key': 'street'},
    {'key': 'postcode',
     'boost': lambda doc: 1.2 if doc.get('type') == 'municipality' else 1},
    {'key': 'city'},
    {'key': 'housenumbers'}
]
```

Puedes acceder a cualquier campo de tu fuente de datos original aquí. Por ejemplo, `doc.get('type')` se refiere a la propiedad `type` definida en el archivo json BAN.

Advertencia: Los índices se calculan durante la importación. Si ya has importado datos, necesitas restablecer y reimportar después de modificar este archivo de configuración.

Si deseas controlar el `id` del documento, por ejemplo, para anular documentos al reindexar, agrega un campo `_id` en el documento,
o define uno de los campos indexados con `type: "id"`.

#### FILTERS (lista)
Una lista de campos a ser indexados como filtros disponibles. Ten en cuenta que cada
filtro significa un índice más grande.

    FILTERS = ["type", "postcode", "cod_departament", "cod_province", "cod_district", "manzana", "lote", "id_urb"]


#### LOG_QUERIES (booleano)
Configúralo en `True` para registrar cada consulta recibida y el primer resultado si lo hay. *Nota:
solo se registran las consultas, no ninguno de los otros datos recibidos.*

    LOG_QUERIES = False

#### LOG_NOT_FOUND (booleano)
Configúralo en `True` para registrar cada consulta no encontrada tanto a través del punto de entrada `search`
como del de `csv`.

    LOG_NOT_FOUND = False

#### QUERY_MAX_LENGTH (int)
En caracteres, longitud máxima aceptada de la consulta. Evita que se procesen cadenas muy grandes.

    QUERY_MAX_LENGTH = 200

#### SLOW_QUERIES (entero)
Define el tiempo (en ms) para registrar una consulta lenta.

    SLOW_QUERIES = False  # Inactivo
    SLOW_QUERIES = 500  # Registrará cada consulta que dure más de 500 ms

#### SYNONYMS_PATHS (lista de rutas)
Rutas a archivos de sinónimos. Los archivos de sinónimos están en el formato `av, ave => avenue`.

    SYNONYMS_PATHS = ['/path/to/synonyms.txt']

## Configuraciones avanzadas

Estas son configuraciones internas. Cámbialas con precaución.

#### BATCH_CHUNK_SIZE (int)
Número de documentos a ser procesados juntos por cada trabajador durante la importación.

    BATCH_CHUNK_SIZE = 1000

#### BATCH_FILE_LOADER_PYPATH (ruta de Python)
Ruta de Python a un callable que será responsable de cargar el archivo en
la importación y devolver un iterable.

    BATCH_FILE_LOADER_PYPATH = "geocode.helpers.load_file"

geocoder proporciona tres cargadores: `load_file`, `load_msgpack_file`
(necesita `msgpack-python`) y `load_csv_file`. Pero puedes pasar cualquier ruta a
una función cargable. Esta función tomará una `filepath` como argumento, y
debería generar dicts.

#### BATCH_PROCESSORS_PYPATHS (iterable de rutas de Python)
Todos los métodos llamados durante el proceso por lotes.

    BATCH_PROCESSORS_PYPATHS = [
        "geocode.core.batch.to_json",
        "geocode.helpers.index.prepare_housenumbers",
        "geocode.core.ds.store_documents",
        "geocode.helpers.index.index_documents",
    ]

#### BUCKET_MIN (int)
El número mínimo de elementos que geocoder intentará buscar en Redis antes de calificar y
ordenarlos. Ten en cuenta que **este no es el número de resultados devueltos**.
Esto puede impactar mucho en el rendimiento.

    BUCKET_MIN = 10

#### BUCKET_MAX (int)
El número máximo de elementos que geocoder intentará buscar en Redis antes de calificar y
ordenarlos. Ten en cuenta que **este no es el número de resultados devueltos**.
Esto puede impactar mucho en el rendimiento.

    BUCKET_MAX = 100

#### COMMON_THRESHOLD (int)
Por encima de este umbral, los términos se consideran comunes y, por lo tanto, con menos importancia
en el algoritmo de búsqueda.

    COMMON_THRESHOLD = 10000

#### DEFAULT_BOOST (float)
Puntuación predeterminada para la relación

 token-documento.

    DEFAULT_BOOST = 1.0

#### DOCUMENT_SERIALIZER_PYPATH (ruta de Python)
Ruta al serializador que se utilizará para almacenar documentos. Debe tener métodos `loads` y
`dumps`.

    DOCUMENT_SERIALIZER_PYPATH = "geocode.helpers.serializers.ZlibSerializer"

Para una opción más rápida (pero usando más RAM), usa `marshal`.

    DOCUMENT_SERIALIZER_PYPATH = 'marshal'

#### GEOHASH_PRECISION (int)
Tamaño del geohash. Cuanto mayor sea la configuración, más pequeño será el hash.
Consulta [Geohash en Wikipedia](http://en.wikipedia.org/wiki/Geohash).

    GEOHASH_PRECISION = 8

#### IMPORTANCE_WEIGHT (float)
La puntuación inherente máxima de un documento en la puntuación final.

    IMPORTANCE_WEIGHT = 0.1

#### GEO_DISTANCE_WEIGHT (float)
La puntuación inherente máxima de la distancia geográfica al centro proporcionado (si lo hay) en la puntuación final.

    GEO_DISTANCE_WEIGHT = 0.1

#### INTERSECT_LIMIT (int)
Por encima de este umbral, evitamos la intersección de conjuntos.

    INTERSECT_LIMIT = 100000

#### MAX_EDGE_NGRAMS (int)
Longitud máxima de ngrams de borde calculados.

    MAX_EDGE_NGRAMS = 20

#### MIN_EDGE_NGRAMS (int)
Longitud mínima de ngrams de borde calculados.

    MIN_EDGE_NGRAMS = 3

#### MIN_SCORE (float)
Todos los resultados con una puntuación final por debajo de este umbral no se mantendrán. La puntuación es
entre 0 y 1.

    MIN_SCORE = 0.1

#### MATCH_THRESHOLD (float entre 0 y 1)
Puntuación mínima utilizada para considerar que un resultado puede *coincidir* con la consulta.

    MATCH_THRESHOLD = 0.9

#### PROCESSORS_PYPATHS (iterable de rutas de Python)
Define las diversas funciones para preprocesar el texto, antes de indexar y
buscar. Es un `iterable` de rutas de Python. Algunas funciones están integradas
(principalmente para el francés en este momento, pero puedes apuntar a cualquier función de Python que
esté en el pythonpath).

    PROCESSORS_PYPATHS = [
        "geocode.helpers.text.tokenize",
        "geocode.helpers.text.normalize",
        "geocode.helpers.text.flag_housenumber",
        "geocode.helpers.text.synonymize",
    ]

#### QUERY_PROCESSORS_PYPATHS (iterable de rutas de Python)
Procesadores adicionales que se ejecutan solo en el momento de la consulta. Por defecto, solo
`check_query_length` está activo, depende de `QUERY_MAX_LENGTH` para evitar DoS.

    QUERY_PROCESSORS_PYPATHS = (
        'geocode.helpers.text.check_query_length',
    )

#### RESULTS_COLLECTORS_PYPATHS (iterable de rutas de Python)
geocoder intentará cada uno de estos en el orden dado para buscar resultados coincidentes.

    RESULTS_COLLECTORS_PYPATHS = [
        "geocode.core.autocomplete.only_commons_but_geohash_try_autocomplete_collector",
        "geocode.helpers.collectors.no_tokens_but_housenumbers_and_geohash",
        "geocode.helpers.collectors.no_available_tokens_abort",
        "geocode.helpers.collectors.only_commons",
        "geocode.core.autocomplete.no_meaningful_but_common_try_autocomplete_collector",
        "geocode.core.autocomplete.only_commons_try_autocomplete_collector",
        "geocode.helpers.collectors.bucket_with_meaningful",
        "geocode.helpers.collectors.reduce_with_other_commons",
        "geocode.helpers.collectors.ensure_geohash_results_are_included_if_center_is_given",  # noqa
        "geocode.core.autocomplete.autocomplete_meaningful_collector",
        "geocode.core.fuzzy.fuzzy_collector",
        "geocode.helpers.collectors.extend_results_extrapoling_relations",
        "geocode.helpers.collectors.extend_results_reducing_tokens",
    ]

### SEARCH_RESULT_PROCESSORS_PYPATHS (iterable de rutas de Python)
Post procesamiento de cada resultado encontrado durante la búsqueda.

    SEARCH_RESULT_PROCESSORS_PYPATHS = [
        "geocode.helpers.results.match_housenumber",
        "geocode.helpers.results.make_labels",
        "geocode.helpers.results.score_by_importance",
        "geocode.helpers.results.score_by_autocomplete_distance",
        "geocode.helpers.results.score_by_ngram_distance",
        "geocode.helpers.results.score_by_geo_distance",
        "geocode.helpers.results.adjust_scores",
    ]