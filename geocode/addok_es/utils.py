import re
from . import phonetic_algorithms_es

_CACHE = {}

PA = phonetic_algorithms_es.PhoneticAlgorithmsES()

def phonemicize(s):
    if s not in _CACHE:
        if s.isnumeric():
            _s = s
        else:
            _s = PA.metaphone(s)
        _CACHE[s] = _s
    return s.update(_CACHE[s])
