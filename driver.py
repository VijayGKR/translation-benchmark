import subprocess
import os
import json
import argparse
from utils.utils import generate_reference_files 
from utils.config import Config

def run_experiment(config: Config, experiment_id):
    experiment_config = config.get_experiment_config(experiment_id)
    SOURCE_LANGUAGE = experiment_config['source_language']
    TEMPERATURE = experiment_config['temperature']
    STRATEGY = experiment_config['strategy']
    TARGET_LANGUAGES = experiment_config['target_languages']
    MODEL = experiment_config['model']

    # Create a folder for the experiment outputs
    if not os.path.exists(f"experiments/"):
        os.makedirs(f"experiments/", exist_ok=True)

    output_folder = f"experiments/{experiment_id}"
    os.makedirs(output_folder, exist_ok=True)

    if TARGET_LANGUAGES == "minimal":
        TARGET_LANGUAGES = config.experiments['language_groups']['minimal']
    elif TARGET_LANGUAGES == "full":
        TARGET_LANGUAGES = config.experiments['language_groups']['full']

    for target_language in TARGET_LANGUAGES:

        print(f"Running with LLM type: {MODEL}")
        print(f"Source Language: {SOURCE_LANGUAGE}")
        print(f"Target Language: {target_language}")
        print(f"Temperature: {TEMPERATURE}")
        print(f"Strategy: {STRATEGY}")
            
        output_file = os.path.join(output_folder, f"{MODEL}_{SOURCE_LANGUAGE}_to_{target_language}.txt")
        print(output_file)
            
        command = [
            "python3", "generate.py",
            experiment_id,
            output_file,
            target_language
        ]
            
        subprocess.run(command)

        ref_output_path = output_file.replace('.txt', '.references')
        no_header_output_path = output_file.replace('.txt', '.candidates')
        # Check if output_file exists before proceeding
        if os.path.exists(output_file):
            ref_output_path = output_file.replace('.txt', '.references')
            no_header_output_path = output_file.replace('.txt', '.candidates')
            generate_reference_files(config, experiment_id, output_file, ref_output_path=ref_output_path, no_header_output_path=no_header_output_path)
        else:
            print(f"Warning: Output file {output_file} does not exist. Skipping reference file generation.")

def main():
    parser = argparse.ArgumentParser(description="Run translation experiments.")
    parser.add_argument("--experiment_id", help="experiment id")
    parser.add_argument("--list", action="store_true", help="List available experiments")
    args = parser.parse_args()

    config = Config()
    if args.list:
        experiments = config.get_all_experiments()
        for experiment_id, experiment_config in experiments.items():
            print(f"{experiment_id}: {experiment_config}")
        return
    try:
        run_experiment(config, args.experiment_id)
        pass
    except ValueError as e:
        print(f"Error: {e}")
        print("Use --list to see available experiments.")

if __name__ == "__main__":
    main()
