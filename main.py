from os import getenv

from dotenv import load_dotenv

from messageremover import bot


def main():
    load_dotenv()
    bot.run(getenv('TOKEN'))


if __name__ == '__main__':
    main()
