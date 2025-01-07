import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from enum import Enum

class Topics(Enum):
    History = 'History'
    English = 'English'
    French = 'French'
    Spanish = 'Spanish'
    Business = 'Business'
    Economics = 'Economics'

class QuizQuestion:

    def __init__(self, question_text, choiceA, choiceB, choiceC, choiceD, answer):
        self.question_text = question_text
        self.choiceA = choiceA
        self.choiceB = choiceB
        self.choiceC = choiceC
        self.choiceD = choiceD
        self.answer = answer

    def __str__(self):
        return (f"Question:{self.question_text}"
                f"ChoiceA: {self.choiceA}"
                f"ChoiceB: {self.choiceB}"
                f"ChoiceC: {self.choiceC}"
                f"ChoiceD: {self.choiceD}"
                f"Answer: {self.answer}")




class GenAI:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_path = "ibm-granite/granite-3.0-2b-instruct"
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        # Load Model
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)
        # Set the model to evaluation model
        self.model.eval()

    def generateQuestions(self, number: int, topic: Topics, ageGroup: str):
        # change input text as desired
        chat = [
            {"role": "user", "content": f"Generate {number} multiple choice quiz question with 4 choices based on {topic.value},"
                                        f" suitable for children at {ageGroup} years old "
                                        f"and ensure there is only 1 correct answer, "
                                        f"include correct answer of multiple choice quiz question."},
        ]
        chat = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        # tokenize the text

        input_tokens = self.tokenizer(chat, return_tensors="pt").to(self.device)

        # generate output tokens
        output = self.model.generate(**input_tokens,
                                     max_new_tokens=number * 100 + 200, temperature=0.85, do_sample=True)

        # decode output tokens into text
        output = self.tokenizer.batch_decode(output, skip_special_tokens=True)[0]
        assistantIndex = output.index("assistant")
        return output[assistantIndex + 9:]

if __name__ == "__main__":
    # print output
    genAi = GenAI()

    text = genAi.generateQuestions(3, Topics.Business, "12-15")
    # store in objects
    textList = text.splitlines()
    textList = [text.strip() for text in textList if text!='']
    questions = []
    for index in range(0,len(textList),6):
        questionText = textList[index]
        choiceA = textList[index+1]
        choiceB = textList[index+2]
        choiceC = textList[index+3]
        choiceD = textList[index+4]
        answer = textList[index+5]
        questions.append(QuizQuestion(questionText, choiceA, choiceB, choiceC, choiceD, answer))
    # write csv file
    csvHeader = ['question', 'choice A', 'choice B', 'choice C', 'choice D', 'answer']
    file = open("statics/output.csv", "w")
    file.write(",".join(csvHeader)+'\n')
    for question in questions:
        file.write(",".join(question.__dict__.values())+'\n')
    file.close()





























