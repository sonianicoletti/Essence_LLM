import pandas as pd

# Load the file
excel_file = 'input/scores_retrieval.xlsx'
df = pd.read_excel(excel_file)

# Ensure required columns exist
required_columns = ['k', 'relevant_results', 'total_relevant_results',
                    'pos_rel_doc_1', 'pos_rel_doc_2', 'pos_rel_doc_3', 'pos_rel_doc_4']
if not all(col in df.columns for col in required_columns):
    raise ValueError(f"The CSV file must contain the following columns: {required_columns}")

# Initialize metrics
precision_at_k = []
recall_at_k = []
reciprocal_ranks = []
average_precisions = []

# Process each question
for _, row in df.iterrows():
    k = row['k']
    relevant_results = row['relevant_results']
    total_relevant = row['total_relevant_results']
    positions = [row[f'pos_rel_doc_{i+1}'] for i in range(4) if not pd.isna(row[f'pos_rel_doc_{i+1}'])]

    print("POSTIONS")
    print(positions)

    # Precision@K
    precision = relevant_results / k if k > 0 else 0
    precision_at_k.append(precision)

    # Recall@K
    recall = relevant_results / total_relevant if total_relevant > 0 else 0
    recall_at_k.append(recall)

    # Mean Reciprocal Rank (MRR)
    reciprocal_rank = 0
    if positions:
        reciprocal_rank = 1 / positions[0]
    reciprocal_ranks.append(reciprocal_rank)

    # Mean Average Precision (MAP)
    if positions:
        positions_sorted = sorted(positions)
        precision_scores = []
        for i, pos in enumerate(positions_sorted, start=1):
            if pos <= k:
                precision_scores.append(i / pos)
        average_precision = sum(precision_scores) / len(positions_sorted) if positions_sorted else 0
    else:
        average_precision = 0
    average_precisions.append(average_precision)

# Compute averages for the metrics
mean_precision_at_k = sum(precision_at_k) / len(precision_at_k) if precision_at_k else 0
mean_recall_at_k = sum(recall_at_k) / len(recall_at_k) if recall_at_k else 0
mean_reciprocal_rank = sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0
mean_average_precision = sum(average_precisions) / len(average_precisions) if average_precisions else 0

# Print the results
print(f"Precision@K: {mean_precision_at_k:.3f}")
print(f"Recall@K: {mean_recall_at_k:.3f}")
print(f"Mean Reciprocal Rank (MRR): {mean_reciprocal_rank:.3f}")
print(f"Mean Average Precision (MAP): {mean_average_precision:.3f}")