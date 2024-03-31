import logging

import colorama
from colorama import Fore, Style

colorama.init()


class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.BLUE + Style.BRIGHT,
        'INFO': Fore.GREEN + Style.BRIGHT,
        'WARNING': Fore.YELLOW + Style.BRIGHT,
        'ERROR': Fore.MAGENTA + Style.BRIGHT,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        msg = super().format(record)
        color = self.get_color(record.levelname)
        return f"{color}{msg.upper()}{Style.RESET_ALL}"

    def get_color(self, levelname):
        return self.COLORS.get(levelname, Fore.WHITE + Style.BRIGHT)


logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = ColoredFormatter('%(asctime)s | %(levelname)s | %(message)s',
                             '%m-%d-%Y %H:%M:%S')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
