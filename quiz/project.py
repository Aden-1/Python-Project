import csv, random

def main():
    playing = 'y'

    score = 0
    NUMBER_OF_QUESTIONS = 10

    elapsedTime = 0

    while playing != 'n':
        ## GET USER INFO
        userFirst, userLast, userID = getUserInfo()
        print(userFirst, userLast, userID)

        ## ASK THE USER 10 QUESTIONS (can be changed)
        questionList = []
        #Store valid answers given by the user
        answerHistory = []

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

            # increment current question number
            currentQuestionNumber += 1
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


def validateAnswer(currentQuestion, userAnswer):
    return currentQuestion[4].lower() == userAnswer



def storeResults():#vars for implementing store results: userFirst, userLast, userID, score, NUMBER_OF_QUESTIONS, questionList, answerHistory, elapsedTime
    """Saves the quiz results into a text file"""                  #i just put whatever as a placeholder

    results = (student_id,"_",fName,"_",lName,".txt")

    with open("results.txt", "w") as save:
        save.write("Student ID: ",student_id,"\n")
        save.write("Name: ",fName," ",lName,"\n")
        save.write("Score: ",score,"\n")
        save.write("Elapsed Time: ",elapsedTime,"\n")

        for i in answer: #loops through the answers the student entered (answer) being the directory we're saving the answers in. (change if want)
            save.write("Question: ",i[question],"\n")
            save.write("Correct answer: ", i[answer],"\n")
            save.write("Selected: ",i[studentAnswer]) #placeholder variable for whatever the student's entered answer is.

    print("Results saved.\n")

if __name__ == "__main__":
    main()