from colorama import Fore, Style

def query(color, outputText):
    color_print(color, outputText)
    userInput = input()
    return userInput.lower().startswith('y')

def querySelector(queryList):
    queryListlength = len(queryList)
    print(f"Please type a number to select your option (1-{queryListlength}): ")
    for i, query in enumerate(queryList):
        print(f"{i+1}. {query}")
    
  #  while not userInput.isdigit():
  #      
  #      color_print(Fore.RED, "Please enter a number! ")
  #      userInput = input(f"Please type a correct number (1-{queryListlength}): ")    
    index = -1 #int(userInput) - 1
    while index not in range(0, queryListlength):
        userInput = input(f"Please type a correct number (1-{queryListlength}): ")
        if userInput.isdigit():
            index = int(userInput) - 1
            if index not in range(0, queryListlength):
                color_print(Fore.RED, f"Make sure to enter a number between 1-{queryListlength}")
        elif not userInput.isdigit():
            color_print(Fore.RED, "Make sure to enter a number!")
        


    print(index)
    return index

def color_print(color, text):
    print(color + text + Style.RESET_ALL)
