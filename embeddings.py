import os
import numpy as np
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_embedding(text, model="text-embedding-3-large"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def compute_embeddings_similarity(candidates_file, output_file):
    
    # Define file paths
    references_file = os.path.join("/Users/vijaykumaravelrajan/Downloads/floresp-v2.0-rc.3/devtest", "devtest.eng_Latn")
    
    # Read the files
    with open(candidates_file, 'r', encoding='utf-8') as f_cand:
        candidates = f_cand.readlines()
    
    with open(references_file, 'r', encoding='utf-8') as f_ref:
        references = f_ref.readlines()
        references = references[:50]

    n = 100  # Number of times each reference is repeated
    references = [ref for ref in references for _ in range(n)]

    print(len(candidates))
    print(len(references))
    
    if len(candidates) != len(references):
        print(f"Warning: Files have different number of lines (candidates: {len(candidates)}, references: {len(references)}). Skipping this file...")
        return
    
    # Generate embeddings and compute similarities
    similarity_scores = []
    batch_size = 100
    
    for i in range(0, len(candidates), batch_size):
        batch_candidates = candidates[i:i + batch_size]
        batch_references = references[i:i + batch_size]
        
        # Get embeddings for entire batch
        cand_embeddings = client.embeddings.create(
            input=[cand.strip() for cand in batch_candidates], 
            model="text-embedding-004"
        ).data
        ref_embeddings = client.embeddings.create(
            input=[ref.strip() for ref in batch_references], 
            model="text-embedding-004"
        ).data
        
        # Extract embedding vectors from response
        cand_vectors = [emb.embedding for emb in cand_embeddings]
        ref_vectors = [emb.embedding for emb in ref_embeddings]
        
        # Compute similarities for batch
        batch_similarities = [
            cosine_similarity(cand_vec, ref_vec) 
            for cand_vec, ref_vec in zip(cand_vectors, ref_vectors)
        ]
        similarity_scores.extend(batch_similarities)
        
        print(f"Processed batch {i//batch_size + 1}, total items: {len(similarity_scores)}")
    
    # Write similarity scores to the output file
    with open(output_file, 'w', encoding='utf-8') as f_out:
        for score in similarity_scores:
            f_out.write(f"{score}\n")

def process_directory(directory_path):
    # Get all .candidates files in directory
    candidate_files = [f for f in os.listdir(directory_path) if f.endswith('.candidates')]
    
    for candidate_file in candidate_files:
        # Construct paths
        candidate_path = os.path.join(directory_path, candidate_file)
        reference_path = candidate_path.replace('.candidates', '.references')
        reward_path = os.path.join("GEMINI_REWARD", candidate_file.replace('.candidates', '.reward'))
        
        # Skip if reference file doesn't exist
        if not os.path.exists(reference_path):
            print(f"Warning: Reference file not found for {candidate_file}, skipping...")
            continue
            
        print(f"Processing {candidate_file}...")
        compute_embeddings_similarity(candidate_path,reward_path)
        print(f"Completed processing {candidate_file}")

if __name__ == "__main__":
    directory_path = "/Users/vijaykumaravelrajan/translation-benchmark/output_english_to_all"
    process_directory(directory_path)

