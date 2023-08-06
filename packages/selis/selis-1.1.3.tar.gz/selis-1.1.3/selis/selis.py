import sys

from optparse import OptionParser
from selis.client import ChatClient


def print_usge():
    usage = "Usage: selis [port] [options]\n"
    option_info = "\nOptions:\n"\
                  "-h, --help            show this help message and exit\n"\
                  "-n NICKNAME, --nickname=NICKNAME\n"\
                  "                      choose a nickname\n"\
                  "-p PASSWORD, --password=PASSWORD\n"\
                  "                      password of the room (if required)"

    print(usage + option_info)


def return_arguments(): 
    parser = OptionParser(add_help_option=False)
    parser.add_option("-h", "--help", dest="help", action="store_true", help="show this help message and exit")
    parser.add_option("-n", "--nickname", dest="nickname", help="choose a nickname")
    parser.add_option("-p", "--password", dest="password", help="password of the room")
    (options, arguments) = parser.parse_args()

    if options.help:
        print_usge()
        sys.exit()

    if not options.nickname:
        print_usge()
        sys.exit()

    return options


def get_port():
    try:
        return int(sys.argv[1])
    except:
        print_usge()
        sys.exit(0)


def main():
    options = return_arguments()

    ip = "0.tcp.ap.ngrok.io"
    port = get_port()
    nickname = options.nickname

    password = options.password


    try:
        client = ChatClient(ip, port, nickname, password)
        client.start()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
