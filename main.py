from logging import debug
import logging

from client.networking.Host import Host
from client.networking.NetworkHandler import NetworkHandler
from client.persistance.DatabaseManager import DatabaseManager


def initialize_interaction():
    from client.interaction.InteractionManager import InteractionManager
    interaction_manager = InteractionManager()
    interaction_manager.start()


def initialize_communication(database_manager: DatabaseManager):
    network_handler = NetworkHandler()
    host = Host(network_handler, database_manager)
    host.start()


def main():
    pass


if __name__ == '__main__':
    dev = True
    logging.basicConfig(level=logging.DEBUG)
    debug("Initializing...")
    if not dev:
        # initialize_interaction()
        pass
    database_manager = DatabaseManager()
    initialize_communication(database_manager)
    main()
