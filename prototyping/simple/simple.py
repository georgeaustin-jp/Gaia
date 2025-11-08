if __name__ == "__main__":
  word: str = ""
  print("Hello")
  print("To end the program, enter the word \":q\"")
  while word != ":q":
    word = input("Enter a word: ")
    print(f"Your word is: {word}")
  print("Goodbye")