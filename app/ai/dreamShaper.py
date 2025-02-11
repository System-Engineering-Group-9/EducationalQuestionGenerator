import torch
from diffusers import AutoPipelineForText2Image, DEISMultistepScheduler

from app.ai.enums.topic import Topic


class DreamShaper:
    def __init__(self):
        pipe = AutoPipelineForText2Image.from_pretrained('lykon/dreamshaper-8', torch_dtype=torch.float16,
                                                         variant="fp16")
        pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to("cuda")
        self.pipe = pipe
        self.generator = torch.manual_seed(20)

    def generate_image(self, topic: Topic, ageGroup: str):
        prompt = (f"Generate an background image with a topic of {topic.value},"
                  f" suitable for children at {ageGroup} years old, highlight the main theme of the topic.")
        return self.pipe(prompt, generator=self.generator, num_inference_steps=25).images[0]