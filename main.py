from logging import debug
import logging

from client.interaction.InteractionManager import InteractionManager


def test_init():
    interaction_manager = InteractionManager()
    interaction_manager.start()


def main():
    import client.read_write_test.Read


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    debug("Initializing...")
    test_init()
    # main()