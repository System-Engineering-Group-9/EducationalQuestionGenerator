# main.py
from app.ai.enums.topic import Topic
from app.ai.questionGenerator import QuestionGenerator


def main():
    # Initialize the question generator
    print("Loading models")
    genAi = QuestionGenerator()
    print("Models loaded")

    # Input the number of questions to generate, the topic, the age group
    while True:
        try:
            number = int(input("Enter the number of questions to generate: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        try:
            topic = Topic(
                input("Enter the topic (Available Topics: History, English, French, Spanish, Business, Economics): "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid topic.")

    ageGroup = input("Enter the age group: ")

    # Generate questions
    print("Generating questions......")
    questions = genAi.generateQuestions(number, topic, ageGroup, None)
    print("Finished generating questions!")

    # Write questions to a CSV file
    csvHeader = ['question', 'choiceA', 'choiceB', 'choiceC', 'choiceD', 'answer']
    file = open("output.csv", "w")
    file.write(",".join(csvHeader) + '\n')
    for question in questions:
        file.write(",".join(question.__dict__.values()) + '\n')
    file.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:", e)
    # Press any key to exit
    input("Press any key to exit")
