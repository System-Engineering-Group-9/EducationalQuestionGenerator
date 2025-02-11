import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from app.ai.enums.topic import Topic


def extract_after_colon(text):
    return text.split(':', 1)[1].strip()


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


class QuestionGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        model_path = "ibm-granite/granite-3.1-2b-instruct"
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        # Load Model
        self.model = AutoModelForCausalLM.from_pretrained(model_path).to(self.device)

    def generateQuestions(self, number: int, topic: Topic, ageGroup: str, item: str = None) -> list:
        if item is None:
            prompt = (f"Generate {number} multiple choice quiz questions with 4 choices based on {topic.value},"
                      f" suitable for children at {ageGroup} years old "
                      f"and ensure there is only 1 correct answer, "
                      f"include correct answer of multiple choice quiz question."
                      f"Do not include any quotation marks in the output."
                      f"Output in the format: "
                      f"Question:"
                      f"ChoiceA:"
                      f"ChoiceB:"
                      f"ChoiceC:"
                      f"ChoiceD:"
                      f"Answer:"
                      f"Here is an example of output:"
                      f"Question:What is the only planet that hosts life that we know of?\n"
                      f"ChoiceA:Earth\n"
                      f"ChoiceB:Mars\n"
                      f"ChoiceC:Jupiter\n"
                      f"ChoiceD:Venus\n"
                      f"Answer:A"
                    )
        else:
            prompt = (f"Generate {number} multiple choice quiz questions around {item} with 4 choices based on {topic.value},"
                    f" suitable for children at {ageGroup} years old "
                    f"and ensure there is only 1 correct answer, "
                    f"include correct answer of multiple choice quiz question."
                    f"Do not include any quotation marks in the output."
                    f"Output in the format: "
                      f"Question:"
                      f"ChoiceA:"
                      f"ChoiceB:"
                      f"ChoiceC:"
                      f"ChoiceD:"
                      f"Answer:"
                    f"Here is an example of output:"
                    f"Question:What is the only planet that hosts life that we know of?\n"
                    f"ChoiceA:Earth\n"
                    f"ChoiceB:Mars\n"
                    f"ChoiceC:Jupiter\n"
                    f"ChoiceD:Venus\n"
                    f"Answer:A"
            )

        chat = [
            {"role": "user", "content": prompt},
        ]
        chat = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
        input_tokens = self.tokenizer(chat, return_tensors="pt").to(self.device)
        output = self.model.generate(**input_tokens, max_new_tokens=number * 100 + 200, temperature=0.85,
                                     do_sample=True)
        output = self.tokenizer.batch_decode(output, skip_special_tokens=True)[0]
        assistantIndex = output.index("\nassistant")
        text = output[assistantIndex + 10:]
        textList = text.splitlines()
        textList = [text.strip() for text in textList if text != '']
        questions = []
        for index in range(0, len(textList), 6):
            questionText = extract_after_colon(textList[index])
            choiceA = extract_after_colon(textList[index + 1])
            choiceB = extract_after_colon(textList[index + 2])
            choiceC = extract_after_colon(textList[index + 3])
            choiceD = extract_after_colon(textList[index + 4])
            answer = extract_after_colon(textList[index + 5])
            questions.append(QuizQuestion(questionText, choiceA, choiceB, choiceC, choiceD, answer))
        return questions
