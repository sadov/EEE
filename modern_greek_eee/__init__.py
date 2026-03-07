"""Modern Greek EEE - Greek Language Educational Tools

Interactive Greek language learning tools for Modern Greek B (Ελληνικά Β) textbook.
Includes noun declension and verb conjugation exercises.
"""

__version__ = "0.1.0"

# Import submodules for easy access
from . import greek_nouns
from . import greek_verbs
from . import greek_utils

__all__ = [
    "greek_nouns",
    "greek_verbs",
    "greek_utils",
]
