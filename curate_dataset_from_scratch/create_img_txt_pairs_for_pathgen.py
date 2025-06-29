import os
import json
from PIL import Image
import openslide
import shutil

with open("file_name_to_uuid.json") as f:
		wsi_to_uuid = json.load(f)

# Define paths and configuration
WSI_DIR = "pathgen_output"  # Update this to the directory containing your WSI files

OUTPUT_DIR = "pathgen"  # Directory where patches and captions will be saved


PATCH_SIZE = (672, 672)  # Size of the patch to extract
ALREADY_DONE = os.listdir(OUTPUT_DIR)
# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

pathgen_data_path = '/data/hmaurya/PathGen-1.6M.json'
with open(pathgen_data_path, 'r') as f:
		data = json.load(f)

def extract_patch_from_wsi(wsi_path, position, patch_size):
		"""
		Extracts a patch from the WSI at the specified position.

		:param wsi_path: Path to the WSI file.
		:param position: Tuple of (x, y) coordinates.
		:param patch_size: Size of the patch to extract.
		:return: Extracted patch as a PIL Image.
		"""
		try:
				# Load WSI using OpenSlide
				wsi = openslide.OpenSlide(wsi_path)
				x, y = map(int, position)  # Convert position coordinates to integers
				patch = wsi.read_region((x, y), 0, patch_size)  # Extract patch
				return patch
		except Exception as e:
				print(f"Error extracting patch from {wsi_path} at {position}: {e}")
				return None

data.reverse()
for item in data:
	wsi_id = item['wsi_id']
	position = item['position']
	caption = item['caption']
	
	patch_filename = f"{wsi_id}_{position[0]}_{position[1]}.png"
	if patch_filename in ALREADY_DONE:
		print(f"Already done {wsi_id} at position {position}")
		continue
	# Construct the full path to the WSI file
	wsi_path = os.path.join(WSI_DIR,f"{wsi_to_uuid[wsi_id]}" ,f"{wsi_id}.svs")  # Update extension if different
	if not os.path.exists(wsi_path):
			print(f"WSI file not found: {wsi_path}")
			continue

	# Extract the patch
	patch = extract_patch_from_wsi(wsi_path, position, PATCH_SIZE)

	if patch:
   # Save the patch as an image file
		patch_filename = f"{wsi_id}_{position[0]}_{position[1]}.png"
		patch_path = os.path.join(OUTPUT_DIR, patch_filename)
  # Save the caption in a text file
		caption_filename = f"{wsi_id}_{position[0]}_{position[1]}.txt"
		caption_path = os.path.join(OUTPUT_DIR, caption_filename)
		if patch_filename in ALREADY_DONE:
			print(f"Already done {wsi_id} at position {position}")
			continue
		
		patch.save(patch_path)

		
		with open(caption_path, 'w') as caption_file:
			caption_file.write(caption)
	
		# wsi_name_done[wsi_id] += 1
		
		print(f"Extracted and saved patch and caption for {wsi_id} at position {position}")
	else:
		print(f"Failed to extract patch for {wsi_id} at position {position}")
