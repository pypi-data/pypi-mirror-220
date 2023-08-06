def imageexp():
  from PIL import Image
  import requests
  from io import BytesIO
  import pandas as pd
  from transformers import CLIPProcessor, CLIPModel
  from google.colab import files


  V01 = "Very Expensive"
  V02 = "Expensive"
  V03 = "Average"
  V04 = "Inexpensive"
  V05 = "Very inexpensive"

# Load CLIP model and processor (for expensive level rating)
  model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
  processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

# Helper function to process each image and get the total_index_colour and comment_colour
  def process_image_val(image_path):
     image = Image.open(image_path)

   # Process image and text
     inputs = processor(text=[V01, V02, V03, V04, V05], images=image, return_tensors="pt", padding=True)
     outputs = model(**inputs)
     logits_per_image = outputs.logits_per_image
     probs = logits_per_image.softmax(dim=1)
     labels = [V01, V02, V03, V04, V05]
     label_probs = [(label, prob.item()) for label, prob in zip(labels, probs[0])]
     label_probs_sorted = sorted(label_probs, key=lambda x: x[1], reverse=True)

   # Calculate total_index
     label_values = [5, 4, 3, 2, 1]
     total_index_val = sum(label_values[labels.index(label)] * confidence for label, confidence in label_probs_sorted)

   # Determine comment based on total_index
     comment_val = ""
     if total_index_val >= 4:
        comment_val = V01
     elif total_index_val >= 3:
        comment_val = V02
     elif total_index_val >= 2:
        comment_val = V03
     elif total_index_val >= 1:
        comment_val = V04
     else:
        comment_val = V05

     return total_index_val, comment_val

# Upload the batch of photos and process them one by one
  uploaded_files = files.upload()
  output_data = []
  for image_path in uploaded_files.keys():
    total_index_val, comment_val = process_image_val(BytesIO(uploaded_files[image_path]))
    output_data.append({"Image_Path": image_path, "Total_Index": total_index_val, "Comment": comment_val})

# Save the output data to a CSV file
  output_df = pd.DataFrame(output_data)
  output_csv_path = "output_results.csv"
  output_df.to_csv(output_csv_path, index=False)
  print(f"Output data saved to {output_csv_path}.")
