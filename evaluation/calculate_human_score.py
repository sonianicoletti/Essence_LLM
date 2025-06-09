# pip install pandas, openpyxl
import pandas as pd
import glob
import os

input_folder = "input/human_eval"
output_file = "output/scores_human_avg.xlsx"
file_paths = sorted(glob.glob(os.path.join(input_folder, "scores_human_*.xlsx")))

# Read all dataframes into a list
dataframes = [pd.read_excel(fp) for fp in file_paths]

# Concatenate and group by index to average all numeric columns
# Assumes files are row-aligned (i.e., same order of questions)
df_concat = pd.concat(dataframes, axis=0).groupby(level=0).mean(numeric_only=True)

# Use the first file as reference for non-numeric columns
df_base = pd.read_excel(file_paths[0])
for col in df_base.columns:
    if col not in df_concat.columns:
        df_concat[col] = df_base[col]

# Reorder columns to match original
df_concat = df_concat[df_base.columns]

# Save to output
os.makedirs("output", exist_ok=True)
df_concat.to_excel(output_file, index=False)
print(f"Averaged file saved to: {output_file}")

# --------------------------
# ANALYSIS ON AVERAGED FILE
# --------------------------

# Reload the averaged file
df = pd.read_excel(output_file)

# Ensure numeric evaluation columns
eval_columns = [col for col in df.columns if col.startswith(('rel_', 'acc_', 'com_'))]
df[eval_columns] = df[eval_columns].apply(pd.to_numeric, errors='coerce')

# Define models and their corresponding columns
models = {
    'llama': ['rel_llama', 'acc_llama', 'com_llama'],
    'llama_rag': ['rel_llama_rag', 'acc_llama_rag', 'com_llama_rag'],
    'gpt': ['rel_gpt', 'acc_gpt', 'com_gpt'],
    'gpt_rag': ['rel_gpt_rag', 'acc_gpt_rag', 'com_gpt_rag'],
    'deepseek': ['rel_deep', 'acc_deep', 'com_deep'],
    'deepseek_rag': ['rel_deep_rag', 'acc_deep_rag', 'com_deep_rag'],
    'claude': ['rel_claude', 'acc_claude', 'com_claude'],
    'claude_rag': ['rel_claude_rag', 'acc_claude_rag', 'com_claude_rag'],
}

question_types = ['information', 'decision-making', 'translation']
metrics = ['Relevance', 'Accuracy', 'Completeness', 'Average']
columns = ['Information', 'Decision-Making', 'Translation', 'Overall']

# Create result table
result_data = []

for model, cols in models.items():
    model_rows = []

    for i, metric in enumerate(['Relevance', 'Accuracy', 'Completeness']):
        row = []
        for qtype in question_types:
            avg = df[df['question_type'].str.lower() == qtype][cols[i]].mean()
            row.append(round(avg, 3) if pd.notna(avg) else 0.000)
        overall_avg = df[cols[i]].mean()
        row.append(round(overall_avg, 3) if pd.notna(overall_avg) else 0.000)
        model_rows.append(row)

    # Compute Average row (mean of Relevance, Accuracy, Completeness per question type and overall)
    avg_row = [round(sum(col) / 3, 3) for col in zip(*model_rows)]
    model_rows.append(avg_row)

    # Append to result with labels
    for metric_name, values in zip(metrics, model_rows):
        result_data.append([model.upper(), metric_name] + values)

# Create and print result DataFrame
result_df = pd.DataFrame(result_data, columns=["Model", "Metric"] + columns)
print("\nFinal Evaluation Table from Averaged Scores:\n")
print(result_df.to_string(index=False))
