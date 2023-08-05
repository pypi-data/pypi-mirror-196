"""Riseact CLI"""

__version__ = "1.0.1"


from riseact.topics.settings.selectors import settings_load

SETTINGS = settings_load()
