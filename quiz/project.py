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

def storeResults(student_id,fName,lName,score,elapsedTime,answer): #feel free to rename the variables,
    """Saves the quiz results into a text file"""                  #i just put whatever as a placeholder

    results = f"{student_id}_{fName}_{lName}.txt"
    with open(results, "w") as save:
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