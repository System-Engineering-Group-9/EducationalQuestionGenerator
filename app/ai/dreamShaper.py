import torch
from diffusers import AutoPipelineForText2Image, DEISMultistepScheduler


class DreamShaper:
    def __init__(self):
        pipe = AutoPipelineForText2Image.from_pretrained('lykon/dreamshaper-8', torch_dtype=torch.float16,
                                                         variant="fp16")
        pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
        pipe = pipe.to("cuda")
        self.pipe = pipe
        self.generator = torch.manual_seed(20)

    def generate_image(self, prompt: str):
        return self.pipe(prompt, generator=self.generator, num_inference_steps=25).images[0]
