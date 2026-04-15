import csv, random

def main():
    playing = 'y'

    ## MERGE CONFLICT DEMO

    Score = 0
    NUMBER_OF_QUESTIONS = 10

    while playing != 'n':
        ## GET USER INFO
        userFirst, userLast, userID = getUserInfo()
        print(userFirst, userLast, userID)

        ## ASK THE USER 10 QUESTIONS (can be changed)
        questionList = []

        for i in range(1,NUMBER_OF_QUESTIONS + 1):
            currentQuestionNumber = i
            ## Get questions one at a time
            currentQuestion, questionList = getQuestion(currentQuestionNumber, questionList)

            # Display question and answer options
            print("Question ", currentQuestionNumber, ": ",  currentQuestion[0], sep="")

            print("A.", currentQuestion[1])
            print("B.", currentQuestion[2])
            ## Only display option C if the question is not true/false
            if currentQuestion[3] != "":
                print("C.", currentQuestion[3])

            # Get user answer
            userAnswer = input("Answer (A, B, or, C): ").lower()

            ## CHECK IF ANSWER IS CORRECT
            validateAnswer()
            # increment score if correct
            score =+ 1

            # increment current question number
            currentQuestionNumber += 1

        ## STORE RESULTS
        storeResults()


        status = input("Type 'Q' to quit and 'S' to restart the quiz:")
        if status.lower() == 'q':
            playing = 'n'
            print("Thanks for playing!")
        elif status.lower() == 's':
            #restart quiz
            print("NEW QUIZ!")


def getUserInfo():
    validateInfo()
    userFirst = "temp"
    userLast = "temp"
    userID = "temp"
    return userFirst, userLast, userID

def validateInfo():
    print("placeholder")

def getQuestion(currentQuestionNumber, questionList):
    questions = questionList
    questionNum = currentQuestionNumber - 1
    #only get new questions for a new quiz, otherwise keep the same questions
    if questionNum == 0:
        questions = genQuestions(10)

    return questions[questionNum], questions



def genQuestions(requestedQuestionCount):
    questions = []
    randomQuestions = []
    # open the csv file and read the questions
    with open('testbank.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the first line
        # add all the questions to a list
        for question in reader:
            questions.append(question)

    questionCount = requestedQuestionCount
    questionCounter = 0
    #randomly select 10 questions
    while questionCounter < questionCount:
        newQuestion = random.choice(questions)
        if newQuestion not in randomQuestions:
            randomQuestions.append(newQuestion)
            questionCounter += 1

    return randomQuestions


def validateAnswer():
    print("placeholder")


def storeResults():
    print("placeholder")

if __name__ == "__main__":
    main()