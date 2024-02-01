import os
from pathlib import Path

REDIS = {
    "host": os.environ.get("REDIS_HOST") or "localhost",
    "port": os.environ.get("REDIS_PORT") or 6379,
    "unix_socket_path": os.environ.get("REDIS_SOCKET"),
    "indexes": {
        "db": os.environ.get("REDIS_DB_INDEXES") or 0,
    },
    "documents": {
        "db": os.environ.get("REDIS_DB_DOCUMENTS") or 1,
    },
}

# Min/max number of results to be retrieved from db and scored.
BUCKET_MIN = 10
BUCKET_MAX = 100

# Above this threshold, terms are considered commons.
COMMON_THRESHOLD = 10000

# Above this threshold, we avoid intersecting sets.
INTERSECT_LIMIT = 100000

# Min score considered matching the query.
MATCH_THRESHOLD = 0.9

# Do not consider result if final score is below this threshold.
MIN_SCORE = 0.1

QUERY_MAX_LENGTH = 200

GEOHASH_PRECISION = 7

MIN_EDGE_NGRAMS = 3
MAX_EDGE_NGRAMS = 20

SYNONYMS_PATHS = []

# Pipeline stream to be used.
PROCESSORS_PYPATHS = [  # Rename in TOKEN_PROCESSORS / STRING_PROCESSORS?
    "geocode.helpers.text.tokenize",
    "geocode.helpers.text.normalize",
    "geocode.helpers.text.flag_housenumber",
    "geocode.helpers.text.synonymize",
]
QUERY_PROCESSORS_PYPATHS = [
    "geocode.helpers.text.check_query_length",
]
# Remove SEARCH_PREFIXES.
SEARCH_PREPROCESSORS_PYPATHS = [
    "geocode.helpers.search.tokenize",
    "geocode.helpers.search.search_tokens",
    "geocode.helpers.search.select_tokens",
    "geocode.helpers.search.set_should_match_threshold",
]
BATCH_PROCESSORS_PYPATHS = [
    "geocode.core.batch.to_json",
    "geocode.helpers.index.prepare_housenumbers",
    "geocode.core.ds.store_documents",
    "geocode.helpers.index.index_documents",
]

BATCH_FILE_LOADER_PYPATH = "geocode.helpers.load_file"
BATCH_CHUNK_SIZE = 1000
# During imports, workers are consuming RAM;
# let one process free for Redis by default.
BATCH_WORKERS = max(os.cpu_count() - 1, 1)

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
SEARCH_RESULT_PROCESSORS_PYPATHS = [
    "geocode.helpers.results.match_housenumber",
    "geocode.helpers.results.make_labels",
    "geocode.helpers.results.score_by_importance",
    "geocode.helpers.results.score_by_autocomplete_distance",
    "geocode.helpers.results.score_by_ngram_distance",
    "geocode.helpers.results.score_by_geo_distance",
    "geocode.helpers.results.adjust_scores",
]
REVERSE_RESULT_PROCESSORS_PYPATHS = [
    "geocode.helpers.results.load_closer",
    "geocode.helpers.results.make_labels",
    "geocode.helpers.results.score_by_geo_distance",
]
RESULTS_FORMATTERS_PYPATHS = [
    "geocode.helpers.formatters.geojson",
]
INDEXERS_PYPATHS = [
    "geocode.helpers.index.HousenumbersIndexer",
    "geocode.helpers.index.FieldsIndexer",
    # Pairs indexer must be after `FieldsIndexer`.
    "geocode.core.pairs.PairsIndexer",
    # Edge ngram indexer must be after `FieldsIndexer`.
    "geocode.core.autocomplete.EdgeNgramIndexer",
    "geocode.helpers.index.FiltersIndexer",
    "geocode.helpers.index.GeohashIndexer",
]
# Any object like instance having `loads` and `dumps` methods.
DOCUMENT_SERIALIZER_PYPATH = "geocode.helpers.serializers.ZlibSerializer"

DOCUMENT_STORE_PYPATH = "geocode.core.ds.RedisStore"

# Fields to be indexed
# If you want a housenumbers field but need to name it differently, just add
# type="housenumbers" to your field.
FIELDS = [
    {"key": "name", "boost": 4, "null": False},
    {"key": "street"},
    {
        "key": "postcode",
        "boost": lambda doc: 1.2 if doc.get("type") == "municipality" else 1,
    },
    {"key": "city"},
    {"key": "housenumbers"},
    {"key": "context"},
]
ID_FIELD = "_id"

# Sometimes you only want to add some fields keeping the default ones.
EXTRA_FIELDS = []

# Weight of a document own importance:
IMPORTANCE_WEIGHT = 0.1

# Geographical distance importance on final score
GEO_DISTANCE_WEIGHT = 0.1

# Default score for the relation token => document
DEFAULT_BOOST = 1.0

# Data attribution
# Can also be an object {source: attribution}
ATTRIBUTION = "Geosolution Consulting S.A.C."

# Available filters (remember that every filter means bigger index)
FILTERS = ["type", "postcode"]

LOG_DIR = os.environ.get("ADDOK_LOG_DIR", Path(__file__).parent.parent.parent)

LOG_QUERIES = False
LOG_NOT_FOUND = False
SLOW_QUERIES = False  # False or time in ms to consider query as slow

INDEX_EDGE_NGRAMS = True

# surrounding letters on a standard keyboard (default french azerty)
FUZZY_KEY_MAP = {
    "a": "ezqop",
    "z": "aqse",
    "e": "azsdryu",
    "r": "edft",
    "t": "rfgy",
    "y": "teghu",
    "u": "yehji",
    "i": "ujko",
    "o": "iaklp",
    "p": "oalm",
    "q": "azsw",
    "s": "qzedxw",
    "d": "serfcx",
    "f": "drtgvc",
    "g": "ftyhbv",
    "h": "gyujnb",
    "j": "huikn",
    "k": "jil",
    "l": "kom",
    "m": "lpu",
    "w": "qsx",
    "x": "wsdc",
    "c": "xdfvio",
    "v": "cfgb",
    "b": "vghn",
    "n": "bhj",
}
