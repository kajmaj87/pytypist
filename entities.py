from collections import namedtuple

Transition = namedtuple("Transition", ["start", "end", "state", "time"])
Key = namedtuple("Key", ["char", "special"], defaults=["", ""])
