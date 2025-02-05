from app.ai.genAI import GenAI, Topics

if __name__ == "__main__":
    # initialize generator
    print("Loading models")
    genAi = GenAI()
    # generate questions
    print("Generating questions......")
    questions = genAi.generateQuestions(1, Topics.Business, "12-15",None)
    print("Finished generating questions!")
    # write csv file
    csvHeader = ['question', 'choice A', 'choice B', 'choice C', 'choice D', 'answer']
    file = open("static/output.csv", "w")
    file.write(",".join(csvHeader)+'\n')
    for question in questions:
        file.write(",".join(question.__dict__.values())+'\n')
    file.close()





























