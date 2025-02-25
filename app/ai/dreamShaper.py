import torch
from diffusers import AutoPipelineForText2Image, DEISMultistepScheduler

from app.ai.enums.subject import Subject


def get_background_prompt(subject: Subject, ageGroup: str) -> str:
    subject_prompts = {
        Subject.History: f"A colorful and engaging historical scene illustrating {ageGroup}-year-old friendly events, such as ancient civilizations or medieval castles.",
        Subject.English: f"A vibrant storybook-themed background with playful letters and literary elements, appealing to {ageGroup}-year-old children.",
        Subject.French: f"A picturesque scene of France with iconic elements like the Eiffel Tower, baguettes, and a lively French café, suitable for {ageGroup}-year-old learners.",
        Subject.Spanish: f"A bright and cheerful Spanish-themed setting featuring elements like flamenco dancers, Spanish landmarks, and fun vocabulary words for {ageGroup}-year-old children.",
        Subject.Business: f"A fun and simplified illustration of a marketplace, money flow, or teamwork, making business concepts accessible to {ageGroup}-year-olds.",
        Subject.Economics: f"A visually engaging economy-themed background with concepts like trade, supply and demand, and basic financial ideas, designed for {ageGroup}-year-olds."
    }

    return subject_prompts.get(subject,
                               f"A general educational background image themed around {subject.value}, suitable for {ageGroup}-year-old children.")


def get_quiz_panel_background_prompt(subject: Subject, ageGroup: str) -> str:
    quiz_panel_prompts = {
        Subject.History: f"A clean and structured historical-themed quiz background with subtle ancient civilization or medieval motifs, optimized for {ageGroup}-year-old learners.",
        Subject.English: f"A minimalist storybook-themed quiz panel background with light literary elements and playful typography, suitable for {ageGroup}-year-old children.",
        Subject.French: f"A quiz-friendly, French-themed background featuring soft, unobtrusive depictions of iconic elements like the Eiffel Tower and French culture, perfect for {ageGroup}-year-old learners.",
        Subject.Spanish: f"A visually engaging but uncluttered Spanish-themed quiz panel background, incorporating subtle references to Spanish culture and language for {ageGroup}-year-old children.",
        Subject.Business: f"A simple yet effective business-themed quiz background with faint imagery of teamwork, markets, or financial symbols, catering to {ageGroup}-year-olds.",
        Subject.Economics: f"A structured, economy-themed quiz background featuring minimal yet recognizable trade and financial motifs, ensuring focus for {ageGroup}-year-olds."
    }

    return quiz_panel_prompts.get(subject,
                                  f"A quiz-friendly educational background themed around {subject.value}, designed for {ageGroup}-year-old children.")



class DreamShaper:
    def __init__(self):
        pipe = AutoPipelineForText2Image.from_pretrained('lykon/dreamshaper-8', torch_dtype=torch.float16,
                                                         variant="fp16")
        pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(self.device)
        self.pipe = pipe
        self.generator = torch.manual_seed(20)

    def generate_background_image(self, subject: Subject, ageGroup: str):
        return self.pipe(get_background_prompt(subject, ageGroup), generator=self.generator,
                         num_inference_steps=20).images[0]

    def generate_quiz_panel_background_image(self, subject: Subject, ageGroup: str):
        return self.pipe(get_quiz_panel_background_prompt(subject, ageGroup), generator=self.generator,
                         num_inference_steps=25).images[0]
