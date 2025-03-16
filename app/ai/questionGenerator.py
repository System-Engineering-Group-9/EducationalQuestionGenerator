import torch
from llama_cpp import Llama

from app.ai.enums.subject import Subject


def extract_after_colon(text):
    return text.split(':', 1)[1].strip()


class QuizQuestion:

    def __init__(self, question, choiceA, choiceB, choiceC, choiceD, answer):
        self.question = question
        self.choiceA = choiceA
        self.choiceB = choiceB
        self.choiceC = choiceC
        self.choiceD = choiceD
        self.answer = answer

    def __str__(self):
        return (f"Question:{self.question}"
                f"ChoiceA: {self.choiceA}"
                f"ChoiceB: {self.choiceB}"
                f"ChoiceC: {self.choiceC}"
                f"ChoiceD: {self.choiceD}"
                f"Answer: {self.answer}")


def get_prompt(number: int, subject: Subject, ageGroup: str, item: str = None) -> str:
    base_prompt = (
        f"Generate {number} multiple choice quiz questions "
        f"with 4 choices based on {subject.value}, suitable for children at {ageGroup} years old. "
        f"Ensure there is only 1 correct answer and include the correct answer. "
        f"Do not include any quotation marks in the output. "
        f"Output each question in the following format:\n"
        f"Question:\n"
        f"ChoiceA:\n"
        f"ChoiceB:\n"
        f"ChoiceC:\n"
        f"ChoiceD:\n"
        f"Answer:\n"
        f"Here is an example of output:\n"
        f"Question:What is the only planet that hosts life that we know of?\n"
        f"ChoiceA:Earth\n"
        f"ChoiceB:Mars\n"
        f"ChoiceC:Jupiter\n"
        f"ChoiceD:Venus\n"
        f"Answer:A"
    )

    if item:
        base_prompt = base_prompt.replace(
            f"Generate {number} multiple choice quiz questions",
            f"Generate {number} multiple choice quiz questions around {item}"
        )

    return base_prompt


class QuestionGenerator:
    def __init__(self):
        if torch.cuda.is_available():
            # Use GPU
            self.llm = Llama.from_pretrained(
                repo_id="QuantFactory/granite-3.0-8b-instruct-GGUF",
                filename="granite-3.0-8b-instruct.Q4_K_S.gguf",
                n_gpu_layers=-1,  # Use all layers on GPU
            )
        else:
            # Use CPU
            self.llm = Llama.from_pretrained(
                repo_id="QuantFactory/granite-3.0-8b-instruct-GGUF",
                filename="granite-3.0-8b-instruct.Q4_K_S.gguf"
            )

    def generateQuestions(self, number: int, subject: Subject, ageGroup: str, item: str = None) -> list:
        prompt = get_prompt(number, subject, ageGroup, item)
        chat = [
            {"role": "user", "content": prompt},
        ]
        response = self.llm.create_chat_completion(
            messages=chat,
            max_tokens=number * 200 + 200,
            temperature=0.85,
        )
        output = response['choices'][0]['message']['content']
        textList = output.splitlines()
        textList = [text.strip() for text in textList if text != '']
        questions = []
        for index in range(0, len(textList), 6):
            question = extract_after_colon(textList[index])
            choiceA = extract_after_colon(textList[index + 1])
            choiceB = extract_after_colon(textList[index + 2])
            choiceC = extract_after_colon(textList[index + 3])
            choiceD = extract_after_colon(textList[index + 4])
            answer = extract_after_colon(textList[index + 5])
            questions.append(QuizQuestion(question, choiceA, choiceB, choiceC, choiceD, answer))
        return questions
