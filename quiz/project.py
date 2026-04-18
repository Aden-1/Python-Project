import csv, random, time

def main():
    playing = 'y'

    NUMBER_OF_QUESTIONS = 10


    while playing != 'n':

        startTime = time.time()
        timeLimit = 600
        elapsedTime = 0
        score=0

        ## GET USER INFO
        userFirst, userLast, userID = getUserInfo()
        print(userFirst, userLast, userID)

        ## ASK THE USER 10 QUESTIONS (can be changed)
        questionList = []
        #Store valid answers given by the user
        answerHistory = []

        for i in range(1,NUMBER_OF_QUESTIONS + 1):
            #Time limit
            elapsedTime = time.time() - startTime
            if elapsedTime >= timeLimit:
                print("Time limit exceeded.\n")
                break
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

            ## Validate user answer
            while userAnswer not in ('a', 'b', 'c'):
                userAnswer = input("Invalid answer. Please enter A, B, or C: ").lower()

            #store valid answer in answer history
            answerHistory.append(userAnswer)

            ## CHECK IF ANSWER IS CORRECT
            if validateAnswer(currentQuestion, userAnswer):
                # increment score
                score += 1
                print("Correct!")
            else:
                print("Incorrect. The correct answer is ", currentQuestion[4], ".", sep="")

            # separate questions
            print("")

        ## STORE RESULTS
        storeResults()#vars for implementing store results: userFirst, userLast, userID, score, NUMBER_OF_QUESTIONS, questionList, answerHistory, elapsedTime

        ## PRINT TEST RESULTS
        print("Quiz complete! Your score is ", score, "/", NUMBER_OF_QUESTIONS, ".", sep="")

        ## ALLOW THE USER TO QUIT OR RESTART THE QUIZ WITH NEW QUESTIONS
        status = input("Type 'Q' to quit and 'R' to restart the quiz:")

        if status.lower() == 'q':
            playing = 'n'
            print("Thanks for playing!")
        elif status.lower() == 'r':
            #restart quiz
            print("NEW QUIZ!")


def getUserInfo():
    validateInfo()
    userFirst = input("Hello please enter your first name: \n")
    userLast = input("Hello please enter your last name: \n")
    userID = input("And finally, what is your School ID?: \n")

    print('Hello ' + userFirst + ' ' + userLast + ' Welcome to the quiz, Good Luck!')
    print('='*40)
    pass

    #return userFirst, userLast, userID

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


def validateAnswer(currentQuestion, userAnswer):
    return currentQuestion[4].lower() == userAnswer



def storeResults(userFirst, userLast, userID, score, NUMBER_OF_QUESTIONS, questionList, answerHistory, elapsedTime):#vars for implementing store results: userFirst, userLast, userID, score, NUMBER_OF_QUESTIONS, questionList, answerHistory, elapsedTime
    """Saves the quiz results into a text file"""                  #i just put whatever as a placeholder

    results = (userID,"_",userFirst,"_",userLast,".txt")

    with open("results.txt", "w") as save:
        save.write("Student ID: ",userID,"\n")
        save.write("Name: ",userFirst," ",userLast,"\n")
        save.write("Score: ",score,"/",NUMBER_OF_QUESTIONS,"\n")
        save.write("Elapsed Time: ",elapsedTime,"\n")

        for i in range(len(answerHistory)):
            question = questionList[i] #loops through the answers the student entered and outputs it.
            save.write("Question: ",question[0],"\n")
            save.write("Correct answer: ",question[4],"\n")
            save.write("Selected: ",answerHistory[i])

    print("Results saved.\n")

if __name__ == "__main__":
    main()