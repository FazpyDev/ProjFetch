from colorama import Fore, Style

def query(color, outputText):
    color_print(color, outputText)
    userInput = input()
    return userInput.lower().startswith('y')

def querySelector(queryList):
    print("Please select an option: ")
    for i, query in enumerate(queryList):
        print(f"{i+1}. {query}")
    
    userInput = input()
    return int(userInput) -1

def color_print(color, text):
    print(color + text + Style.RESET_ALL)
