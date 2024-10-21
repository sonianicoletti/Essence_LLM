import os
import json

# Define a function to convert JSON to Markdown
def json_to_markdown(json_folder_path, output_folder_path):
    # Ensure the output folder exists
    os.makedirs(output_folder_path, exist_ok=True)

    # Iterate over each JSON file in the specified folder
    for filename in os.listdir(json_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(json_folder_path, filename)

            # Read the JSON file
            with open(file_path, "r", encoding='utf-8') as f:
                json_data = json.load(f)
                
            # Initialize a list to hold markdown lines for this specific file
            markdown_lines = []

            # Process each object in the JSON data
            for record in json_data:
                text = record.get("text", "")
                record_type = record.get("type", "")

                # Append formatted text based on its type
                if record_type == "Title":
                    markdown_lines.append(f"# {text}\n")  # Title formatted as H1
                elif record_type == "Header":
                    markdown_lines.append(f"## {text}\n")  # Header formatted as H2
                elif record_type not in ["PageBreak", "PageNumber", "Image"]:  # Ignore these types
                    markdown_lines.append(f"{text}\n")  # Normal text

            # Join all lines into a single markdown string
            markdown_content = "".join(markdown_lines)

            # Define the output Markdown file path
            output_markdown_path = os.path.join(output_folder_path, f"{os.path.splitext(filename)[0]}.md")

            # Write the markdown content to the output file with utf-8 encoding
            with open(output_markdown_path, "w", encoding='utf-8') as md_file:
                md_file.write(markdown_content)

            print(f"Markdown file created at: {output_markdown_path}")

# Specify the path to the JSON folder and the output Markdown folder
json_folder_path = "../data/json/"
output_folder_path = "../output/"

# Call the function to convert JSON to Markdown
json_to_markdown(json_folder_path, output_folder_path)
