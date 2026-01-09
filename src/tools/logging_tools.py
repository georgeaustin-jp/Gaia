import logging
import colorama as cr

cr.init(autoreset=True)

logging.basicConfig(format=f"{cr.Fore.CYAN}%(levelname)s[%(name)s]{cr.Fore.WHITE} AT {cr.Fore.LIGHTMAGENTA_EX}\'%(filename)s\'{cr.Fore.WHITE} IN {cr.Fore.BLUE}\'%(funcName)s\'{cr.Fore.WHITE} {cr.Fore.LIGHTBLACK_EX}(line %(lineno)s):{cr.Style.RESET_ALL}\n >>> %(message)s", level=logging.DEBUG)