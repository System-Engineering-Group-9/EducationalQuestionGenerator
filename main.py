from genAI import GenAI, Topics
from detection import Detection

if __name__ == "__main__":
    # initialize generator
    genAi = GenAI()
    detection = Detection()
    item = detection.cameraDetection()
    # generate questions
    questions = genAi.generateQuestions(3, Topics.Business, "12-15",item)
    # write csv file
    csvHeader = ['question', 'choice A', 'choice B', 'choice C', 'choice D', 'answer']
    file = open("statics/output.csv", "w")
    file.write(",".join(csvHeader)+'\n')
    for question in questions:
        file.write(",".join(question.__dict__.values())+'\n')
    file.close()





























