from logging import debug
import logging

from client.networking.Host import Host
from client.networking.NetworkHandler import NetworkHandler
from client.persistance.Authorization import Authorization
from client.persistance.DatabaseManager import DatabaseManager
from client.interaction.InteractionManager import InteractionManager


def initialize_interaction(host: Host, database_manager: DatabaseManager):
    interaction_manager = InteractionManager(host, database_manager)
    interaction_manager.start()


def set_admin(database_manager: DatabaseManager):
    database_manager.create_or_update_user(770708610319, Authorization.ADMIN)


def initialize_communication():
    database_manager = DatabaseManager()
    network_handler = NetworkHandler()
    host = Host(network_handler, database_manager)
    host.start()
    return host, database_manager


if __name__ == '__main__':
    dev = True
    logging.basicConfig(level=logging.DEBUG)
    debug("Initializing...")
    host, database_manager = initialize_communication()
    set_admin(database_manager)
    database_manager.print_users()

    if not dev:
        initialize_interaction(host, database_manager)
