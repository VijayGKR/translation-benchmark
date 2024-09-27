import os


base_dir = '/content/drive/MyDrive/googletranslate_llm/'
eval_dir = '/content/drive/MyDrive/google_llm_eval_data/'

# Ensure eval_data directory exists
os.makedirs(eval_dir, exist_ok=True)

# Function to extract language from file name
def extract_language(file_name):
    # Assuming the file format is gpt-4o-mini_English_to_<Language>.<extension>
    return file_name.split('_')[-1].split('.')[0]

# List all files in the base directory
files = os.listdir(base_dir)

# Filter candidates and references
candidates = sorted([f for f in files if f.endswith('.txt')])
references = sorted([f for f in files if f.endswith('.references')])
print(candidates)
print(references)

# Ensure we have matching candidate-reference pairs
for candidate, reference in zip(candidates, references):
    # Extract language from the file name (assuming the naming convention matches)
    language = extract_language(candidate)
    print(candidate)
    print(reference)
    # Define output score file path
    score_file = os.path.join(eval_dir, f'{language}.rewards')
    

print("BLEURT evaluation completed for all language pairs.")