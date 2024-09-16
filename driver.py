import subprocess
import os
import json
import argparse

def load_config(experiment_name):
    with open('experiment_configs.json', 'r') as config_file:
        all_configs = json.load(config_file)
    
    if experiment_name not in all_configs['experiments']:
        raise ValueError(f"Experiment '{experiment_name}' not found in configuration.")
    
    return all_configs['experiments'][experiment_name]

def run_experiment(config, experiment_name):
    BASE_PATH = config['base_path']
    SOURCE_LANGUAGE = config['source_language']
    SOURCE_CODE = config['source_code']
    SOURCE_FILE = f"{BASE_PATH}/devtest.{SOURCE_CODE}"
    LLM_TYPES = config['llm_types']
    TEMPERATURE = config['temperature']
    NUM_LINES = config['num_lines']
    STRATEGY = config['strategy']
    TARGET_LANGUAGES = config['target_languages']

    TARGET_CODES = {
        "Hindi": "hin_Deva", "Russian": "rus_Cyrl", "Arabic": "arb_Arab", "Spanish": "spa_Latn",
        "Japanese": "jpn_Jpan", "German": "deu_Latn", "Mandarin Chinese": "cmn_Hans",
        "French": "fra_Latn", "Korean": "kor_Hang", "Italian": "ita_Latn", "Bengali": "ben_Beng",
        "Urdu": "urd_Arab", "Greek": "ell_Grek", "Portuguese": "por_Latn", "Tamil": "tam_Taml",
        "Vietnamese": "vie_Latn", "Romanian": "ron_Latn", "Turkish": "tur_Latn", "Marathi": "mar_Deva",
        "Telugu": "tel_Telu", "Tagalog": "fil_Latn", "Croatian": "hrv_Latn", "Sinhala": "sin_Sinh",
        "English": "eng_Latn"
    }

    # Create a folder for the experiment outputs
    output_folder = f"output_{experiment_name}"
    os.makedirs(output_folder, exist_ok=True)

    for target_language in TARGET_LANGUAGES:
        target_code = TARGET_CODES[target_language]
        reference_file = f"{BASE_PATH}/devtest.{target_code}"
        for llm_type in LLM_TYPES:
            print(f"Running with LLM type: {llm_type}")
            print(f"Source Language: {SOURCE_LANGUAGE}")
            print(f"Target Language: {target_language}")
            print(f"Temperature: {TEMPERATURE}")
            print(f"Strategy: {STRATEGY}")
            
            output_file = os.path.join(output_folder, f"{llm_type}_{SOURCE_LANGUAGE}_to_{target_language}.txt")
            
            command = [
                "python3", "generate.py",
                llm_type,
                SOURCE_LANGUAGE,
                target_language,
                SOURCE_FILE,
                output_file,
                STRATEGY,
                str(NUM_LINES)
            ]
            
            subprocess.run(command)

def main():
    parser = argparse.ArgumentParser(description="Run translation experiments.")
    parser.add_argument("experiment", help="Name of the experiment to run")
    parser.add_argument("--list", action="store_true", help="List available experiments")
    args = parser.parse_args()

    if args.list:
        with open('experiment_config.json', 'r') as config_file:
            all_configs = json.load(config_file)
        print("Available experiments:")
        for exp_name in all_configs['experiments']:
            print(f"- {exp_name}")
        return

    try:
        config = load_config(args.experiment)
        run_experiment(config, args.experiment)
    except ValueError as e:
        print(f"Error: {e}")
        print("Use --list to see available experiments.")

if __name__ == "__main__":
    main()
