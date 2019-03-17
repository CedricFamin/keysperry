import download
import get_sounds
import join


def add_all_commands(client):
    join.add_commands(client)
    get_sounds.add_commands(client)
    download.add_commands(client)
