# Copyright (C) 2023, IQMO Corporation [info@iqmo.com]
# All Rights Reserved

import logging
import pandas as pd

from dataclasses import dataclass
from pandas import DataFrame
from iql.iqmoql import IqlExtension, register_extension, SubQuery, CACHE

logger = logging.getLogger(__name__)


@dataclass
class CacheExtension(IqlExtension):
    keyword: str

    def allow_cache_save(self, sq: "SubQuery") -> bool:
        return False

    def executeimpl(self, sq: SubQuery) -> DataFrame:
        command = sq.get_query()
        if command == "clear_all":
            CACHE.clear_all()
            return pd.DataFrame([{"result:": True}])
        elif command == "clear":
            prefix = "default"
            if "prefix" in sq.options:
                prefix = sq.options["prefix"]
            if "key" in sq.options:
                CACHE.clear(sq.options["key"], prefix)
            else:
                return pd.DataFrame([{"result": False, "error:": "Cache key required"}])

            return pd.DataFrame([{"result:": True}])
        elif command == "get":
            prefix = "default"
            if "prefix" in sq.options:
                prefix = sq.options["prefix"]
            if "key" in sq.options:
                return CACHE.get(sq.options["key"], prefix)
            else:
                return pd.DataFrame([{"result": False, "error:": "Cache key required"}])

        return pd.DataFrame([{"result": False, "error:": "Unknown command"}])


def register(keyword):
    extension = CacheExtension(keyword=keyword)
    register_extension(extension)
