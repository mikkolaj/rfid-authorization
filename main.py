from logging import debug
import logging

from client.persistance.DatabaseManager import DatabaseManager


def initialize_interaction():
    from client.interaction.InteractionManager import InteractionManager
    interaction_manager = InteractionManager()
    interaction_manager.start()


def main():
    pass


if __name__ == '__main__':
    dev = True
    logging.basicConfig(level=logging.DEBUG)
    debug("Initializing...")
    if not dev:
        # initialize_interaction()
        pass
    managerBazy = DatabaseManager()
    managerBazy.print_users()
    managerBazy.create_or_update_user(10, 1)
    managerBazy.print_users()
    managerBazy.create_or_update_user(10, 0)
    managerBazy.print_users()
    managerBazy.create_or_update_user(11, 1)
    managerBazy.print_users()
    debug(managerBazy.is_tag_authorized(10))
    debug(managerBazy.is_tag_authorized(11))
    main()
