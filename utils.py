import sqlite3


def get_result(query: str):
    with sqlite3.connect("netflix.db") as conn:
        conn.row_factory = sqlite3.Row
        result = []
        for item in conn.execute(query).fetchall():
            s = dict(item)
            result.append(s)
        return result


def get_one(query: str):
    with sqlite3.connect("netflix.db") as conn:
        conn.row_factory = sqlite3.Row
        res = conn.execute(query).fetchone()
        if res is None:
            return None
        else:
            return dict(res)


def search_by_cast(query_result, name1, name2):
    cast = []
    for item in query_result:
        cast += item['cast'].split(', ')
    all_actors = cast
    all_actors.remove(name1)
    all_actors.remove(name2)
    co_actors = []
    for actor in set(all_actors):
        if all_actors.count(actor) > 2:
            co_actors.append(actor)
    return co_actors