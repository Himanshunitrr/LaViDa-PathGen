#!/usr/bin/env python3
import numpy as np
import imageio
from PIL import Image, ImageDraw, ImageFont

def wrap_text_any(draw, text, font, max_width):
    """
    Break text into lines so that each line’s pixel width ≤ max_width,
    wrapping at any character (not just spaces).
    """
    lines = []
    curr = ""
    for ch in text:
        test = curr + ch
        bb = draw.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] <= max_width - 15:
            curr = test
        else:
            lines.append(curr)
            curr = ch
    if curr:
        lines.append(curr)
    return lines

# ==== User settings ====
image_path     = '/home/himanshu/Downloads/temp_image.png'
# The series of text you want to show
text_frames = [
    '0: ***************************************************************<|eot_id|>',
'1: **************************************************************.<|eot_id|>',
'2: The*************************************************************.<|eot_id|>',
'3: The tissue************************************************************.<|eot_id|>',
'4: The tissue*********************************************************** carcinoma.<|eot_id|>',
'5: The tissue********************************************************** breast carcinoma.<|eot_id|>',
'6: The tissue********************************************************* of breast carcinoma.<|eot_id|>',
'7: The tissue******************************************************** diagnosis of breast carcinoma.<|eot_id|>',
'8: The tissue******************************************************* a diagnosis of breast carcinoma.<|eot_id|>',
'9: The tissue shows****************************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'10: The tissue shows ple***************************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'11: The tissue shows pleomorphic**************************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'12: The tissue shows pleomorphic cells*************************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'13: The tissue shows pleomorphic cells with************************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'14: The tissue shows pleomorphic cells with hyper************************************************* a diagnosis of breast carcinoma.<|eot_id|>',
'15: The tissue shows pleomorphic cells with hyperchrom************************************************ a diagnosis of breast carcinoma.<|eot_id|>',
'16: The tissue shows pleomorphic cells with hyperchromatic*********************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'17: The tissue shows pleomorphic cells with hyperchromatic nuclei********************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'18: The tissue shows pleomorphic cells with hyperchromatic nuclei,********************************************* a diagnosis of breast carcinoma.<|eot_id|>',
'19: The tissue shows pleomorphic cells with hyperchromatic nuclei,* nucle******************************************* a diagnosis of breast carcinoma.<|eot_id|>',
'20: The tissue shows pleomorphic cells with hyperchromatic nuclei,* nucleoli****************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'21: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli****************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'22: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli,***************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'23: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and**************************************** a diagnosis of breast carcinoma.<|eot_id|>',
'24: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and*************************************** with a diagnosis of breast carcinoma.<|eot_id|>',
'25: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and************************************** consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'26: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and*************************************, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'27: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and************************************ process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'28: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and*********************************** malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'29: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and********************************** a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'30: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and********************************* suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'31: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and******************************* These* suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'32: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and******************************. These* suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'33: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and******************************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'34: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high*****************************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'35: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear****************************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'36: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to***************************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'37: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cy**************************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'38: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cy*ic************************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'39: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cy*ic ratios***********************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'40: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios***********************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'41: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios.**********************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'42: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The*********************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'43: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells********************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'44: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are*******************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'45: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged******************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'46: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in*****************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'47: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a****************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'48: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a dis***************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'49: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized**************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'50: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized,*************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'51: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking************. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'52: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal***********. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'53: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal duct**********. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'54: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal*********. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'55: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal*,*******. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'56: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures,*******. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'57: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures, and******. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'58: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures, and there*****. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'59: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures, and there is****. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'60: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures, and there is a***. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'61: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures, and there is a* of*. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'62: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures, and there is a lack of*. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>',
'63: The tissue shows pleomorphic cells with hyperchromatic nuclei, prominent nucleoli, and high nuclear-to-cyasmic ratios. The cells are arranged in a disorganized, lacking normal ductal structures, and there is a lack of polarity. These findings suggest a malignant process, consistent with a diagnosis of breast carcinoma.<|eot_id|>']
frame_size     = (800, 400)     # total canvas size
font_size      = 24
caption_text   = "Describe the image in detail"
total_duration = 2.81           # seconds
output_path    = 'image_text_animation.gif'

# ==== Derived parameters ====
num_frames   = len(text_frames)
duration_per = total_duration / num_frames

# ==== Split canvas ====
left_w, left_h = frame_size[0] // 2, frame_size[1] - 50  # reserve 50px for caption

# ==== Load & resize left image once ====
left_img = Image.open(image_path).convert('RGB')
left_img = left_img.resize((left_w, left_h))

# ==== Load font once ====
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except IOError:
    font = ImageFont.load_default()

# ==== Precompute caption position ====
dummy     = Image.new('RGB', (1,1))
measure   = ImageDraw.Draw(dummy)
bbox_cap  = measure.textbbox((0,0), caption_text, font=font)
cap_w     = bbox_cap[2] - bbox_cap[0]
cap_x     = (left_w - cap_w) // 2
cap_y     = frame_size[1] - 40

# ==== Text region settings ====
gutter      = 15
text_x      = left_w + gutter
text_max_w  = frame_size[0] - text_x     # full right half
line_spacing = 6

# ==== Build static “base” frame ====
base      = Image.new('RGB', frame_size, 'white')
draw_base = ImageDraw.Draw(base)
base.paste(left_img, (0,0))
draw_base.text((cap_x, cap_y), caption_text, fill='black', font=font)

# ==== Write GIF via imageio ====
with imageio.get_writer(output_path, mode='I', duration=duration_per) as writer:
    for txt in text_frames:
        frame = base.copy()
        draw  = ImageDraw.Draw(frame)

        # wrap anywhere by pixel width
        lines = wrap_text_any(draw, txt, font, text_max_w)

        y = 50
        for line in lines:
            draw.text((text_x, y), line, fill='black', font=font)
            y += font_size + line_spacing

        writer.append_data(np.array(frame))

print(f"Saved → {output_path}")