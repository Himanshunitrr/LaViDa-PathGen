import requests
import json
import re
# Load your file names from a JSON file
with open('all_image_names.json', 'r') as file:
		file_names = json.load(file)  # Assuming it's a list of file names

# API endpoint
API_URL = "https://api.gdc.cancer.gov/files"

# Pagination and filtering parameters
PAGE_SIZE = 100  # Adjust based on API limits
file_name_to_uuid = {}

def fetch_data(page):
		params = {
				"size": PAGE_SIZE,
				"from": page * PAGE_SIZE,
				"pretty": "true"
		}
		response = requests.get(API_URL, params=params)
		response.raise_for_status()  # Raise error for HTTP issues
		return response.json()

# Iterate over all pages
page = 0
while True:
		print(f"Fetching page {page + 1}...")
		data = fetch_data(page)
		
		# Iterate through the 'hits' and match file names
		for record in data["data"]["hits"]:
				file_name = record.get("file_name")
				if ".svs" in file_name:
						file_name = re.sub(r'\.svs', '', file_name)
				elif ".tiff" in file_name:
						file_name = re.sub(r'\.tiff', '', file_name)
				elif ".tif" in file_name:	
						file_name = re.sub(r'\.tif', '', file_name)
				elif ".jpeg" in file_name:
						file_name = re.sub(r'\.jpeg', '', file_name)
				elif ".ndpi" in file_name:
						file_name = re.sub(r'\.ndpi', '', file_name)
				elif "mrxs" in file_name:
						file_name = re.sub(r'\.mrxs', '', file_name)
				elif ".afi" in file_name:
						file_name = re.sub(r'\.afi', '', file_name)
				elif ".czi" in file_name:
						file_name = re.sub(r'\.czi', '', file_name)
				elif ".bif" in file_name:
						file_name = re.sub(r'\.bif', '', file_name)
				# print(f"file_name: {file_name}")
				# print("#"*50)
				if file_name in file_names:
						print(f"Found matching file: {file_name}")
						file_name_to_uuid[file_name] = record["file_id"]
						# Save results to a JSON file
						with open('file_name_to_uuid.json', 'w') as output_file:
								json.dump(file_name_to_uuid, output_file, indent=4)
		# Check if we've reached the last page
		if page >= data["data"]["pagination"]["pages"] - 1:
				break
		page += 1
# Save results to a JSON file
with open('file_name_to_uuid.json', 'w') as output_file:
		json.dump(file_name_to_uuid, output_file, indent=4)


print(f"Completed! Found {len(file_name_to_uuid)} matching UUIDs.")
