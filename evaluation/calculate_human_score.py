import pandas as pd

# Load the Excel file into a pandas DataFrame
csv_file = 'scores_human.csv'
df = pd.read_csv(csv_file)

# Ensure the DataFrame has the required columns
required_columns = [
    'question', 'question_type', 'ground_truth',
    'answer_llama', 'rel_llama', 'acc_llama', 'com_llama',
    'answer_llama_rag', 'rel_llama_rag', 'acc_llama_rag', 'com_llama_rag',
    'answer_gpt', 'rel_gpt', 'acc_gpt', 'com_gpt',
    'answer_gpt_rag', 'rel_gpt_rag', 'acc_gpt_rag', 'com_gpt_rag',
    'answer_deepseek', 'rel_deep', 'acc_deep', 'com_deep',
    'answer_deepseek_rag', 'rel_deep_rag', 'acc_deep_rag', 'com_deep_rag',
    'answer_claude', 'rel_claude', 'acc_claude', 'com_claude',
    'answer_claude_rag', 'rel_claude_rag', 'acc_claude_rag', 'com_claude_rag'
]

if not all(col in df.columns for col in required_columns):
    raise ValueError(f"The dataset file must contain the following columns: {required_columns}")

# Compute the overall averages
overall_avg = df[[
    'rel_llama', 'acc_llama', 'com_llama',
    'rel_llama_rag', 'acc_llama_rag', 'com_llama_rag',
    'rel_gpt', 'acc_gpt', 'com_gpt',
    'rel_gpt_rag', 'acc_gpt_rag', 'com_gpt_rag',
    'rel_deep', 'acc_deep', 'com_deep',
    'rel_deep_rag', 'acc_deep_rag', 'com_deep_rag',
    'rel_claude', 'acc_claude', 'com_claude',
    'rel_claude_rag', 'acc_claude_rag', 'com_claude_rag'
]].mean()


# Compute averages for each question_type
grouped_avg = df.groupby('question_type')[[
    'rel_llama', 'acc_llama', 'com_llama',
    'rel_llama_rag', 'acc_llama_rag', 'com_llama_rag',
    'rel_gpt', 'acc_gpt', 'com_gpt',
    'rel_gpt_rag', 'acc_gpt_rag', 'com_gpt_rag',
    'rel_deep', 'acc_deep', 'com_deep',
    'rel_deep_rag', 'acc_deep_rag', 'com_deep_rag',
    'rel_claude', 'acc_claude', 'com_claude',
    'rel_claude_rag', 'acc_claude_rag', 'com_claude_rag'
]].mean()

# Combine overall and grouped averages into a single DataFrame
overall_avg_df = pd.DataFrame(overall_avg, columns=['Overall']).T  # Convert to row
grouped_avg_df = grouped_avg.reset_index()  # Reset index for grouped averages

# Concatenate overall and grouped averages
combined_df = pd.concat([overall_avg_df, grouped_avg_df], ignore_index=False)

# Save the combined averages to a CSV file
combined_df.to_csv('scores_human_avg.csv', index=False)

print("Averages saved to 'scores_human_avg.csv'")