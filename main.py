from genAI import GenAI, Topics

if __name__ == "__main__":
    # initialize generator
    genAi = GenAI()
    # generate questions
    questions = genAi.generateQuestions(1, Topics.Business, "12-15","water bottle")
    # write csv file
    csvHeader = ['question', 'choice A', 'choice B', 'choice C', 'choice D', 'answer']
    file = open("statics/output.csv", "w")
    file.write(",".join(csvHeader)+'\n')
    for question in questions:
        file.write(",".join(question.__dict__.values())+'\n')
    file.close()





























