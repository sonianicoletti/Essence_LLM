from evaluate import load
import pandas as pd
import numpy as np

# Load BERTScore
bertscore = load("bertscore")

# Load the Excel file into a pandas DataFrame
dataset_file = 'input/dataset.csv'
df = pd.read_csv(dataset_file)

# Ensure the DataFrame has the required columns
required_columns = ['question', 'question_context', 'question_type', 'context_1', 'context_2', 'context_3', 'context_4', 'ground_truth', 'answer_llama', 'answer_llama_rag', 'answer_gpt', 'answer_gpt_rag', 'answer_deepseek', 'answer_deepseek_rag', 'answer_claude', 'answer_claude_rag']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"The dataset file must contain the following columns: {required_columns}")

# Extract data for processing
questions = df['question'].tolist()
questions_context = df['question_context'].tolist()
question_types = df['question_type'].tolist()
contexts = df[['context_1', 'context_2', 'context_3', 'context_4']].values.tolist()
ground_truths = df['ground_truth'].tolist()

# Extract model-generated answers
answers_llama = df['answer_llama'].tolist()
answers_llama_rag = df['answer_llama_rag'].tolist()
answers_gpt = df['answer_gpt'].tolist()
answers_gpt_rag = df['answer_gpt_rag'].tolist()
answers_deepseek = df['answer_deepseek'].tolist()
answers_deepseek_rag = df['answer_deepseek_rag'].tolist()
answers_claude = df['answer_claude'].tolist()
answers_claude_rag = df['answer_claude_rag'].tolist()

answers_claude = ["" if isinstance(ans, float) and np.isnan(ans) else ans for ans in answers_claude]
answers_claude_rag = ["" if isinstance(ans, float) and np.isnan(ans) else ans for ans in answers_claude_rag]

# Compute BERTScore for LLMs with RAG
results_llama_rag = bertscore.compute(predictions=answers_llama_rag, references=ground_truths, lang="en")
results_gpt_rag = bertscore.compute(predictions=answers_gpt_rag, references=ground_truths, lang="en")
results_deepseek_rag = bertscore.compute(predictions=answers_deepseek_rag, references=ground_truths, lang="en")
results_claude_rag = bertscore.compute(predictions=answers_claude_rag, references=ground_truths, lang="en")

# Compute BERTScore for LLMs without RAG
results_llama = bertscore.compute(predictions=answers_llama, references=ground_truths, lang="en")
results_gpt = bertscore.compute(predictions=answers_gpt, references=ground_truths, lang="en")
results_deepseek = bertscore.compute(predictions=answers_deepseek, references=ground_truths, lang="en")
results_claude = bertscore.compute(predictions=answers_claude, references=ground_truths, lang="en")

# Combine results with questions into a single DataFrame
df_score = pd.DataFrame({
    'question': questions,
    'question_type': question_types,
    
    # Llama scores
    'precision_llama_rag': results_llama_rag['precision'],
    'recall_llama_rag': results_llama_rag['recall'],
    'f1_llama_rag': results_llama_rag['f1'],
    'precision_llama': results_llama['precision'],
    'recall_llama': results_llama['recall'],
    'f1_llama': results_llama['f1'],
    
    # GPT scores
    'precision_gpt_rag': results_gpt_rag['precision'],
    'recall_gpt_rag': results_gpt_rag['recall'],
    'f1_gpt_rag': results_gpt_rag['f1'],
    'precision_gpt': results_gpt['precision'],
    'recall_gpt': results_gpt['recall'],
    'f1_gpt': results_gpt['f1'],
    
    # DeepSeek scores
    'precision_deepseek_rag': results_deepseek_rag['precision'],
    'recall_deepseek_rag': results_deepseek_rag['recall'],
    'f1_deepseek_rag': results_deepseek_rag['f1'],
    'precision_deepseek': results_deepseek['precision'],
    'recall_deepseek': results_deepseek['recall'],
    'f1_deepseek': results_deepseek['f1'],
    
    # Claude scores
    'precision_claude_rag': results_claude_rag['precision'],
    'recall_claude_rag': results_claude_rag['recall'],
    'f1_claude_rag': results_claude_rag['f1'],
    'precision_claude': results_claude['precision'],
    'recall_claude': results_claude['recall'],
    'f1_claude': results_claude['f1'],
})

# Save the evaluation scores to a CSV file
df_score.to_csv('scores_comparison.csv', index=False)

print("Evaluation scores saved to 'scores_comparison.csv'")

# Define all the relevant metric columns
metric_columns = [
    'precision_llama_rag', 'recall_llama_rag', 'f1_llama_rag',
    'precision_llama', 'recall_llama', 'f1_llama',
    'precision_gpt_rag', 'recall_gpt_rag', 'f1_gpt_rag',
    'precision_gpt', 'recall_gpt', 'f1_gpt',
    'precision_deepseek_rag', 'recall_deepseek_rag', 'f1_deepseek_rag',
    'precision_deepseek', 'recall_deepseek', 'f1_deepseek',
    'precision_claude_rag', 'recall_claude_rag', 'f1_claude_rag',
    'precision_claude', 'recall_claude', 'f1_claude'
]

# Calculate averages for all rows
overall_avg = df_score[metric_columns].mean()

# Filter and calculate averages for specific question types
info_avg = df_score[df_score['question_type'] == 'information'][metric_columns].mean()
decision_avg = df_score[df_score['question_type'] == 'decision-making'][metric_columns].mean()
translation_avg = df_score[df_score['question_type'] == 'translation'][metric_columns].mean()

# Combine all averages into a single DataFrame
avg_data = pd.DataFrame({
    'Metric': metric_columns,
    'Overall': overall_avg.values,
    'Information': info_avg.values,
    'Decision-Making': decision_avg.values,
    'Translation': translation_avg.values,
})

# Save the averages to a CSV file
avg_data.to_csv('output/results_avg.csv', index=False)

print("Average scores saved to 'output/results_avg.csv'")