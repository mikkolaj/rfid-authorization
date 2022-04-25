from logging import debug
import logging


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
        initialize_interaction()
    main()
