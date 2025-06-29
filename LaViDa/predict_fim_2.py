

from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path, process_images, tokenizer_image_token
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN, IGNORE_INDEX
from llava.conversation import conv_templates, SeparatorStyle

from PIL import Image
import requests
import copy
import torch
import json

 
# pretrained = "lavida-ckpts/lavida-llada-hd-fim" # this may also work
pretrained = "lavida-ckpts/lavida-llada-hd-fim"
model_name = "llava_llada"
device = "cuda"
device_map = "cuda:0"
conv_template = "llada" # Make sure you use correct chat template for different models
question = DEFAULT_IMAGE_TOKEN + "\nWrite a story based on the image."

FIM = '<|reserved_token_1|>'
# FIM = ''
draft_answer = f'''
Sure, here is a segment.
The boy climbed the hill with his dog.{"<|mdm_mask|>"*40}{FIM} They stood in silence as the star streaked across the sky.
<|eot_id|>'''

conv = copy.deepcopy(conv_templates[conv_template])
conv.append_message(conv.roles[0], question)
conv.append_message(conv.roles[1], None)
prompt_question = conv.get_prompt()
# breakpoint()
# exit()
vision_kwargs = None
vision_kwargs = dict(
       mm_vision_tower="google/siglip-so400m-patch14-384",
    mm_resampler_type=None,
    mm_projector_type='mlp2x_gelu',
    mm_hidden_size=1152,
    use_mm_proj=True
)
tokenizer, model, image_processor, max_length = load_pretrained_model(pretrained, None, model_name, device_map=device_map,vision_kwargs=vision_kwargs,torch_dtype='bfloat16') # Add any other thing you want to pass in llava_model_args

model.eval()
model.tie_weights()
model.to(torch.bfloat16)

img = 'images/port.png'
image = Image.open(img).convert('RGB')
image_tensor = process_images([image], image_processor, model.config)
image_tensor = [_image.to(dtype=torch.bfloat16, device=device) for _image in image_tensor]

input_ids = tokenizer_image_token(prompt_question, tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt").unsqueeze(0).to(device)
image_sizes = [image.size]


if True:
    draft_tokens = tokenizer(draft_answer,return_tensors='pt').to(input_ids.device).input_ids
    
    cont,_ = model.generate(
        input_ids,
        images=image_tensor,
        image_sizes=image_sizes,
        do_sample=False,
        temperature=0.0,
        max_new_tokens=256,
        step_ratio=1.0,
        # steps=128
        tokenizer=tokenizer,
        prefix_lm=True,
        verbose=True,
        draft_tokens=draft_tokens,
        schedule='shift',
        schedule_kwargs=dict(shift=1/3),
    )

    text_outputs = tokenizer.batch_decode(cont, skip_special_tokens=False)

    text_outputs = [text_output.lstrip('!').replace('<|endoftext|>','') for text_output in text_outputs]
    print(text_outputs[0])
    # print(tokenizer.batch_decode(cont[0], skip_special_tokens=True))
