from albert import *
from pydbus import SessionBus

__title__ = "Lollypop"
__version__ = "0.1.0"
__triggers__ = "llp"
__authors__ = "alande"

icon = iconLookup("lollypop")
bus = SessionBus()
search_provider = bus.get('org.gnome.Lollypop.SearchProvider', "/org/gnome/LollypopSearchProvider")

def handleQuery(query):
    query_str = query.string
    if len(query_str) <= 3 and not query.isTriggered:
        return

    result_set = search_provider.GetInitialResultSet(query_str.split())
    metadata = search_provider.GetResultMetas(result_set)

    items = []
    for entry in metadata:
        actions = [
            ProcAction(text="Text goes here",
                       commandline=[
                           'lollypop',
                           '--play-ids',
                           entry["id"]
                       ]),
            FuncAction(text='test',
                       callable=lambda: info(str(entry)))
        ]

        if entry["id"][0] == 'a':
            # Album
            items.append(Item(id=__title__,
                              text=entry["description"],
                              subtext=f"Album | {entry['name']}",
                              icon=entry["gicon"] or icon,
                              actions=actions))
        elif entry["id"][0] == 't':
            # Track
            items.append(Item(id=__title__,
                              text=entry["name"],
                              subtext=f"Song | {entry['description']}",
                              icon=entry["gicon"] or icon,
                              actions=actions))
        else:
            pass # what is this

    return items
