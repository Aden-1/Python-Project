import csv, random, time, sys

def main():
    """
    Main function of the program.
    Makes calls to other functions to execute tasks.
    Will create a 10 or 20 question quiz and score the user's answers.
    Quiz stops asking new questions after 10 minutes (600 seconds).
    """
    playing = 'y'
    DEFAULT_NUM_OF_QUESTIONS = 10


    while playing != 'n':

        # init time vars
        startTime = time.time()
        timeLimit = 600
        elapsedTime = 0
        # init score and temp quiz length
        score=0
        quizLength = 10

        ## HAVE THE USER SELECT A 10 or 20 QUESTION QUIZ
        quizLength = input("How many questions would you like answer? Type '10' or '20': ")

        # check for an invalid answer and fix it.
        while quizLength != "10" and quizLength != "20":
            print("Invalid number of questions selected!")
            quizLength = input("How many questions would you like answer? Type '10' or '20': ")

        # cast user input to an int
        try:
            quizLength = int(quizLength)
        except ValueError:
            print("Integer not input")
            quizLength = input("How many questions would you like answer? Type '10' or '20': ")

        ## GET USER INFO
        userFirst, userLast, userID = getUserInfo()
        print(userFirst, userLast, userID)

        ## ASK THE USER 10 QUESTIONS (can be changed)
        questionList = []
        #Store valid answers given by the user
        answerHistory = []

        ## RUN THE QUIZ
        # pass any needed info and return it
        elapsedTime, score, questionList, answerHistory = askQuestions(startTime, timeLimit, elapsedTime, quizLength, DEFAULT_NUM_OF_QUESTIONS, score, questionList, answerHistory)

        ## STORE RESULTS
        storeResults(userFirst, userLast, userID, score, quizLength, questionList, answerHistory, elapsedTime, DEFAULT_NUM_OF_QUESTIONS)#vars for implementing store results: userFirst, userLast, userID, score, quizLength, questionList, answerHistory, elapsedTime, DEFAULT_NUM_OF_QUESTIONS

        ## PRINT TEST RESULTS
        print("Quiz complete! Your score is ", score, "/", DEFAULT_NUM_OF_QUESTIONS, ".", sep="")

        ## ALLOW THE USER TO QUIT OR RESTART THE QUIZ WITH NEW QUESTIONS
        status = input("Type 'Q' to quit and 'S' to clear the quiz:")

        while status.lower() != 'q' and status.lower() != 's':
            print("Invalid choice.")
            status = input("Type 'Q' to quit and 'S' to clear the quiz:")

        if status.lower() == 'q':
            playing = 'n'
            print("Thanks for playing!")
        elif status.lower() == 's':
            #restart quiz
            print("NEW QUIZ!")



def askQuestions(startTime, timeLimit, elapsedTime, quizLength, DEFAULT_NUM_OF_QUESTIONS, score, questionList, answerHistory):
    """
    Takes basic quiz information, asks the user the quis questions, and returns the results of the quiz to be processed.
    """
    ## For every item in the quiz
    for i in range(1, quizLength + 1):
        # Time limit
        elapsedTime = time.time() - startTime
        if elapsedTime >= timeLimit:
            print("Time limit exceeded.\n")
            break
        currentQuestionNumber = i
        ## Get questions one at a time
        currentQuestion, questionList = getQuestion(currentQuestionNumber, questionList, quizLength)

        # Display question and answer options
        print("Question ", currentQuestionNumber, ": ", currentQuestion[0], sep="")

        print("A.", currentQuestion[1])
        print("B.", currentQuestion[2])
        ## Only display option C if the question is not true/false
        if currentQuestion[3] != "":
            print("C.", currentQuestion[3])

        # Get user answer
        if currentQuestion[3] == "":
            userAnswer = input("Answer (A or B): ").lower()
        else:
            userAnswer = input("Answer (A, B, or, C): ").lower()

        ## Validate user answer
        if currentQuestion[3] != "":
            while userAnswer not in ('a', 'b', 'c') and currentQuestion[3] != "":
                userAnswer = input("Invalid answer. Please enter A, B, or C: ").lower()
        if currentQuestion[3] == "":
            while userAnswer not in ('a', 'b'):
                    userAnswer = input("Invalid answer. Please enter A or B: ").lower()


        # store valid answer in answer history
        answerHistory.append(userAnswer)

        ## CHECK IF ANSWER IS CORRECT
        if validateAnswer(currentQuestion, userAnswer):
            # increment score based off quiz length
            if quizLength == 10:
                score += 1
            elif quizLength == 20:
                score += 0.5
            print("Correct!")
        else:
            print("Incorrect. The correct answer is ", currentQuestion[4], ".", sep="")

        # separate questions
        print("")
    return elapsedTime, score, questionList, answerHistory

def getUserInfo():
    # LH Collects the user's first name, last name, and validated school ID.
    while True:
        try:
            # LH Get first name and validate it's alphabetic
            userFirst = input("Hello and welcome, please enter your first name below: \n")
            if not userFirst.isalpha():
                raise ValueError("Invalid first name. Please enter only letters (no numbers or special characters).")
            break
        except ValueError as e:
            print(e)
    while True:
        try:
            # LH Get last name and validate it's alphabetic
            userLast = input("Please enter your last name: \n")
            if not userLast.isalpha():
                raise ValueError("Invalid last name. Please enter only letters (no numbers or special characters).")
            break
        except ValueError as e:
            print(e)
    # LH Get and validate school ID
    userID = input("And finally, what is your School ID? (A00000): \n").upper()
    print(userID)
    userID = validateInfo(userID)
    if userID is None:
        # LH Exit if too many invalid ID attempts
        print("Too many invalid attempts for school ID. Exiting program.")
        sys.exit()
    print('Hello ' + userFirst + ' ' + userLast + ' Welcome to the quiz, Good Luck!')
    print('=' * 80)
    pass
    return userFirst, userLast, userID

def validateInfo(userID):
    # LH Validates the school ID format (A + 5 digits, first digit 1–9).
    attempts = 0
    while not (
        len(userID) == 6 and
        userID[0].upper() == 'A' and
        userID[1] in '123456789' and
        userID[2:].isdigit()
    ):
        attempts += 1
        if attempts >= 3:
            # LH Return None after 3 failed attempts
            return None
        userID = input('Invalid User ID, Please Try again: ').upper()
        print(userID)
    return userID

def getQuestion(currentQuestionNumber, questionList, quizLength):
    """
    Returns one question at a time from a generated list of defined questions.
    May request a new list of questions if a new quiz has started.
    """
    # set the current questions to the question list passed
    questions = questionList
    questionNum = currentQuestionNumber - 1
    #only get new questions for a new quiz, otherwise keep the same questions
    if questionNum == 0:
        questions = genQuestions(quizLength)

    # retun the current question in the list along with the question list (will request one for a new quiz)
    return questions[questionNum], questions



def genQuestions(requestedQuestionCount):
    """
    Generates a list of unique questions based off of the number of questions requested.
    """
    questions = []
    randomQuestions = []
    # open the csv file and read the questions
    try:
        with open('testbank.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first line
            # add all the questions to a list
            for question in reader:
                questions.append(question)
    except FileNotFoundError:
        sys.exit("quizbank file is missing")


    questionCount = requestedQuestionCount
    questionCounter = 0
    #randomly select unique questions
    while questionCounter < questionCount:
        newQuestion = random.choice(questions)
        if newQuestion not in randomQuestions:
            randomQuestions.append(newQuestion)
            questionCounter += 1

    # return the random questions
    return randomQuestions


def validateAnswer(currentQuestion, userAnswer):
    """
    check if the answer selected is equal to the user's answer return a bool value
    """
    # check if the answer selected is equal to the correct answer
    return currentQuestion[4].lower() == userAnswer



def storeResults(userFirst, userLast, userID, score, quizLength, questionList, answerHistory, elapsedTime, DEFAULT_NUM_OF_QUESTIONS):#vars for implementing store results: userFirst, userLast, userID, score, quizLength, questionList, answerHistory, elapsedTime, DEFAULT_NUM_OF_QUESTIONS
    """Saves the quiz results into a text file"""

    # Create the file name string
    results = str((userID + "_" + userFirst + "_" + userLast + ".txt"))

    # open the file to save the results
    with open(results, "w") as save:
        save.write(f"Student ID: {userID}\n")
        save.write(f"Name: {userFirst} {userLast}\n")
        save.write(f"Score: {score}/{DEFAULT_NUM_OF_QUESTIONS}\n")
        save.write(f"Elapsed Time: {round(elapsedTime,2)} seconds\n")
        save.write("\n")

        #for every question asked save it to the file
        for i in range(quizLength):
            save.write("\n")
            question = questionList[i] #loops through the answers the student entered and outputs it.
            save.write(f"Question{i+1}: {question[0]}\n")
            save.write(f"Correct Answer: {question[4].title()}\n")
            if question[4].lower() == "a":
                save.write(f"Correct Answer Text: {question[1]}\n")
            elif question[4].lower() == "b":
                save.write(f"Correct Answer Text: {question[2]}\n")
            else:
                save.write(f"Correct Answer Text: {question[3]}\n")
            save.write(f"Your Answer: {answerHistory[i].title()}\n")
            if answerHistory[i].lower() == "a":
                save.write(f"Your answer text: {question[1]}\n")
            elif answerHistory[i].lower() == "b":
                save.write(f"Your answer text: {question[2]}\n")
            else:
                save.write(f"Your answer text: {question[3]}\n")

    print("Results saved.\n")

# Run the main function if not imported
if __name__ == "__main__":
    main()