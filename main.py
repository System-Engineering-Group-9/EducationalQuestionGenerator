# main.py
import json

from app.ai.enums.subject import Subject
from app.ai.questionGenerator import QuestionGenerator


def main():
    # Initialize the question generator
    print("Loading models")
    genAi = QuestionGenerator()
    print("Models loaded")

    # Input the number of questions to generate, the subject, the age group
    while True:
        try:
            number = int(input("Enter the number of questions to generate(between 1 and 5): "))
            if 1 <= number <= 5:
                break
            else:
                print("Invalid input. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 5.")

    while True:
        try:
            subject = Subject(
                input(
                    "Enter the subject (Available Subjects: History, English, French, Spanish, Business, Economics): "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid subject.")

    item = input("Enter the item: ")

    ageGroup = input("Enter the age group: ")

    # Generate questions
    print("Generating questions......")
    questions = genAi.generateQuestions(number, subject, ageGroup, item)
    print("Finished generating questions!")

    # Write questions to a Json file
    file = open("output.json", "w")
    file.write(json.dumps([question.__dict__ for question in questions], indent=4))
    file.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:", e)
    # Press any key to exit
    input("Press any key to exit")
