from logging import debug
import logging
from time import time

from client.networking.Host import Host
from client.networking.NetworkHandler import NetworkHandler
from client.persistance.Authorization import Authorization
from client.persistance.DatabaseManager import DatabaseManager


def initialize_interaction(database_manager: DatabaseManager):
    from client.interaction.InteractionManager import InteractionManager
    interaction_manager = InteractionManager(database_manager)
    interaction_manager.start()


def initialize_communication(database_manager: DatabaseManager):
    network_handler = NetworkHandler()
    host = Host(network_handler, database_manager)
    host.start()


def set_admin(database_manager: DatabaseManager):
    database_manager.create_or_update_user(770708610319, Authorization.ADMIN)


def main():
    pass


if __name__ == '__main__':
    dev = True
    logging.basicConfig(level=logging.DEBUG)
    debug("Initializing...")
    database_manager = DatabaseManager()
    set_admin(database_manager)
    database_manager.print_users()
    initialize_interaction(database_manager)
    initialize_communication(database_manager)
    main()
