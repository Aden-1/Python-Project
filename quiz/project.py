def main():
    playing = 'y'
    while playing != 'n':
        userFirst, userLast, userID = getUserInfo()
        getQuestion()
        validateAnswer()
        storeResults()
        status = input("type 'Q' to quit and 'S' to restart the quiz.")
        if status.lower() == 'q':
            playing = 'n'
        elif status.lower() == 's':
            #restart quiz


def getUserInfo():
    validateInfo()

def validateInfo():

def getQuestion():

def validateAnswer():

def storeResults():

if __name__ == "__main__":
    main()