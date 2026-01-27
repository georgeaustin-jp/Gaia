from app import App
import colorama as cr

def main() -> None:
  print(f"{cr.Fore.YELLOW}Loading...{cr.Fore.RESET}")
  app = App()
  print(f"{cr.Fore.GREEN}Loaded{cr.Fore.RESET}")
  app.run()
  
if __name__ == "__main__": main()