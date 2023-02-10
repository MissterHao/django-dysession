from enum import Enum


class ANSIColor(Enum):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    SUCCESSFUL = "\033[38;5;107m"  # 7b9246
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    DEBUG = "\033[37m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def colorful_it(color: ANSIColor, content: str) -> str:
    return f"{color.value}{content}{ANSIColor.ENDC.value}"
