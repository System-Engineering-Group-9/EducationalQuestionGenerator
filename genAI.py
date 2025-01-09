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
        model_path = "ibm-granite/granite-3.1-2b-instruct"
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        # Load Model
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)

    def generateQuestions(self, number: int, topic: Topics, ageGroup: str, item: str = None) -> list:
        # change input text as desired
        if item is None:
            prompt = (f"Generate {number} multiple choice quiz question with 4 choices based on {topic.value},"
                      f" suitable for children at {ageGroup} years old "
                      f"and ensure there is only 1 correct answer, "
                      f"include correct answer of multiple choice quiz question."
                      f"Only include the question, choices and answer and output and output in the format of question in the first line"
                      f"choice A in the second line, choice B in the third line, choice C in the fourth line, choice D in the fifth line"
                      f"Answer in the sixth line.")
        else:
            prompt = (
                f"Generate {number} multiple choice quiz question around {item} with 4 choices based on {topic.value},"
                f" suitable for children at {ageGroup} years old "
                f"and ensure there is only 1 correct answer, "
                f"include correct answer of multiple choice quiz question."
                f"Only include the question, choices and answer and output and output in the format of question in the first line"
                f"choice A in the second line, choice B in the third line, choice C in the fourth line, choice D in the fifth line"
                f"Answer in the sixth line."
                )
        chat = [
            {"role": "user", "content": prompt},
        ]
        chat = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        # tokenize the text

        input_tokens = self.tokenizer(chat, return_tensors="pt").to(self.device)

        # generate output tokens
        output = self.model.generate(**input_tokens,
                                     max_new_tokens=number * 100 + 200, temperature=0.85, do_sample=True)

        # decode output tokens into text
        output = self.tokenizer.batch_decode(output, skip_special_tokens=True)[0]
        assistantIndex = output.index("\nassistant")
        text = output[assistantIndex + 10:]
        textList = text.splitlines()
        textList = [text.strip() for text in textList if text != '']
        questions = []
        for index in range(0, len(textList), 6):
            questionText = textList[index]
            choiceA = textList[index + 1]
            choiceB = textList[index + 2]
            choiceC = textList[index + 3]
            choiceD = textList[index + 4]
            answer = textList[index + 5]
            questions.append(QuizQuestion(questionText, choiceA, choiceB, choiceC, choiceD, answer))
        return questions
