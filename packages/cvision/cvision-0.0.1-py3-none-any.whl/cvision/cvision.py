from PIL import Image
import requests
from io import BytesIO
import pandas as pd
from transformers import CLIPProcessor, CLIPModel
from google.colab import files

# Load CLIP model and processor (for expensive level rating)
model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

# Helper function to process each image and get the total_index and comment
def process_image(image_path):
   image = Image.open(image_path)

   # Process image and text
   inputs = processor(text=["very expensive", "expensive", "average", "inexpensive", "very inexpensive"], images=image, return_tensors="pt", padding=True)
   outputs = model(**inputs)
   logits_per_image = outputs.logits_per_image
   probs = logits_per_image.softmax(dim=1)
   labels = ["very expensive", "expensive", "average", "inexpensive", "very inexpensive"]
   label_probs = [(label, prob.item()) for label, prob in zip(labels, probs[0])]
   label_probs_sorted = sorted(label_probs, key=lambda x: x[1], reverse=True)

   # Calculate total_index
   label_values = [5, 4, 3, 2, 1]
   total_index = sum(label_values[labels.index(label)] * confidence for label, confidence in label_probs_sorted)

   # Determine comment based on total_index
   comment = ""
   if total_index >= 4:
       comment = "Very expensive"
   elif total_index >= 3:
       comment = "Expensive"
   elif total_index >= 2:
       comment = "Average"
   elif total_index >= 1:
       comment = "Inexpensive"
   else:
       comment = "Very inexpensive"

   return total_index, comment

# Upload the batch of photos and process them one by one
uploaded_files = files.upload()
output_data = []
for image_path in uploaded_files.keys():
   total_index, comment = process_image(BytesIO(uploaded_files[image_path]))
   output_data.append({"Image_Path": image_path, "Total_Index": total_index, "Comment": comment})

# Save the output data to a CSV file
output_df = pd.DataFrame(output_data)
output_csv_path = "output_results.csv"
output_df.to_csv(output_csv_path, index=False)
print(f"Output data saved to {output_csv_path}.")
