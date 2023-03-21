from typing import Dict, List, Union
from config import dbname

filtersdb = dbname.filters

def _get_filters(chat_id: int) -> Dict[str, int]:
    filters = filtersdb.find_one({"chat_id": chat_id})
    return filters["filters"] if filters else {}

def del_filter(chat_id: int, name: str) -> bool:
    filtersd = _get_filters(chat_id)
    name = name.lower().strip()
    if name in filtersd:
        del filtersd[name]
        filtersdb.update_one(
            {"chat_id": chat_id},
            {"$set": {"filters": filtersd}},
            upsert=True,
        )
        return True
    return False 

def get_filter(chat_id: int, name: str) -> Union[bool, dict]:
    name = name.lower().strip()
    _filters = _get_filters(chat_id)
    return _filters[name] if name in _filters else False

def get_filters_names(chat_id: int) -> List[str]:
    return list(_get_filters(chat_id))

def save_filter(chat_id: int, name: str, _filter: dict):
    name = name.lower().strip()
    _filters = _get_filters(chat_id)
    _filters[name] = _filter
    filtersdb.update_one(
        {"chat_id": chat_id},
        {"$set": {"filters": _filters}},
        upsert=True,
    )
