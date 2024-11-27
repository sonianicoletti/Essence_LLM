import json
import pandas as pd

def create_dataset_from_json(json_file_path, output_csv_path):
    # Initialize a list to hold the dataset rows
    dataset = []

    # Read the JSON lines file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            record = json.loads(line.strip())  # Parse each line as a JSON object
            question = record.get("user_question", "")
            context = "\n".join(record.get("context", []))  # Combine list of contexts into a single string
            generated_answer = record.get("answer", "")
            ground_truth = ""  # Leave ground_truth empty

            # Append the row to the dataset
            dataset.append({
                "question": question,
                "context": context,
                "generated_answer": generated_answer,
                "ground_truth": ground_truth
            })

    # Convert the dataset list to a DataFrame
    df = pd.DataFrame(dataset)

    # Save the dataset as a CSV file with UTF-8 encoding
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"Dataset saved to {output_csv_path}")

# Example usage
json_file_path = 'data.jsonl'  # Path to the input JSON lines file
output_csv_path = 'dataset.csv'  # Path to save the output CSV file
create_dataset_from_json(json_file_path, output_csv_path)


