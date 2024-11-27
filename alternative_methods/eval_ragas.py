from datasets import Dataset
import pandas as pd
from ragas import evaluate
from ragas.metrics import faithfulness, answer_correctness
import ast  # To safely evaluate string representations of lists
import os
from dotenv import load_dotenv
import openai

load_dotenv()

# Set OpenAI API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Import the data from dataset.csv
csv_file = 'dataset.csv'  # Path to your dataset CSV file

# Load the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file)

# Ensure the DataFrame has the required columns
required_columns = ['question', 'generated_answer', 'context', 'ground_truth']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"The CSV file must contain the following columns: {required_columns}")

# Process the 'context' column to ensure it's a list of strings
def process_context(context):
    if isinstance(context, str):
        try:
            # If context is a string, convert it to a list of strings
            return [context]  # Wrap in a list if it's a single string
        except (ValueError, SyntaxError):
            return [context]
    return context  # Return as-is if already a list


df['context'] = df['context'].apply(process_context)

# Create the data_samples dictionary
data_samples = {
    "question": df["question"].tolist(),
    "answer": df["generated_answer"].tolist(),
    "contexts": df["context"].apply(lambda x: [x] if isinstance(x, str) else x).tolist(),
    "ground_truth": df["ground_truth"].tolist(),
}


# Convert the data_samples dictionary to a Hugging Face Dataset
dataset = Dataset.from_dict(data_samples)

# Evaluate the dataset using Ragas
try:
    score = evaluate(dataset, metrics=[faithfulness, answer_correctness])
    print("EVALUATION RESULTS:", score)
except Exception as e:
    print(f"ERROR during evaluation: {e}")
    raise

# Save the evaluation scores to a CSV file
df_score = score.to_pandas()
df_score.to_csv('ragas_score.csv', index=False)

print("Evaluation scores saved to 'ragas_score.csv'")