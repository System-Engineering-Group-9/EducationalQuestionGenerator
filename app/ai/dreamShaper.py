import torch
from diffusers import AutoPipelineForText2Image, DEISMultistepScheduler

from app.ai.enums.subject import Subject


def get_prompt(subject: Subject, ageGroup: str):
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


class DreamShaper:
    def __init__(self):
        pipe = AutoPipelineForText2Image.from_pretrained('lykon/dreamshaper-8', torch_dtype=torch.float16,
                                                         variant="fp16")
        pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to("cuda")
        self.pipe = pipe
        self.generator = torch.manual_seed(20)

    def generate_image(self, subject: Subject, ageGroup: str):
        return self.pipe(get_prompt(subject, ageGroup), generator=self.generator, num_inference_steps=25).images[0]
