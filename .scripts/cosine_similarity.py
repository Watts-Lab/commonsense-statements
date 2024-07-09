from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# embedded files
embedding_files = [
    'embeddings/observable_gpt4o_embedding.csv',
    'embeddings/news_statements_amir_embedding.csv', 
    'embeddings/email_statements_embedding.csv'
]

# load the embedded files and combine embeddings
all_embeddings = []
all_statements = []
all_files = []
for file in embedding_files:
    df = pd.read_csv(file)
    all_embeddings.extend(df['embedding'].apply(eval).tolist())
    all_statements.extend(df['statement'].tolist())
    all_files.extend([file] * len(df))

# compute cosine similarity matrix for all embeddings
embeddings_array = np.array(all_embeddings)
similarity_matrix = cosine_similarity(embeddings_array)

# helper function to find pairs exceeding similarity threhold
def get_high_similarity_pairs(similarity_matrix, threshold=0.97):
    high_sim_indices = np.argwhere(similarity_matrix > threshold) # get the indices of the pairs with similarity above the threshold
    mask = high_sim_indices[:, 0] != high_sim_indices[:, 1] # filter out self pairs
    high_sim_indices = high_sim_indices[mask]
    
    # ensure each pair is unique by sorting indices and using a set
    unique_pairs = set()
    for idx1, idx2 in high_sim_indices:
        sorted_pair = tuple(sorted((idx1, idx2)))
        unique_pairs.add(sorted_pair)
    
    return list(unique_pairs)

# find pairs with more than 97% similarity
high_sim_pairs = get_high_similarity_pairs(similarity_matrix, threshold=0.97)

similar_pairs_df = pd.DataFrame(columns=['Pair ID', 'File 1', 'Statement 1', 'File 2', 'Statement 2', 'Cosine Similarity'])

# add pairs to df
for pair_id, (idx1, idx2) in enumerate(high_sim_pairs, start=1):
    similar_pairs_df = pd.concat([similar_pairs_df, pd.DataFrame({
        'Pair ID': [pair_id],
        'File 1': [all_files[idx1]],
        'Statement 1': [all_statements[idx1]],
        'File 2': [all_files[idx2]],
        'Statement 2': [all_statements[idx2]],
        'Cosine Similarity': [similarity_matrix[idx1, idx2]]
    })], ignore_index=True)

# sort in descending order of similarity
similar_pairs_df = similar_pairs_df.sort_values(by='Cosine Similarity', ascending=False)

# output the df as a csv for analysis
similar_pairs_df.to_csv('high_similarity_statements.csv', index=False)

print(f"Found {len(similar_pairs_df)} unique pairs exceeding 97% similarity.")
