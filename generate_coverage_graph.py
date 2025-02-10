import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from math import comb
from utils.config import Config
import argparse
import dotenv

dotenv.load_dotenv()   

def calculate_average_max_for_all_n(group):
    results = []
    group_size = len(group)
    sorted_group = sorted(group)
     # Sort the group in descending order
    
    for n in range(1, group_size + 1):
        sum_of_maximums = sum(sorted_group[k-1] * comb(k-1, n-1) for k in range(n, group_size + 1))
        average_max = sum_of_maximums / comb(group_size, n)
        results.append(average_max)
    
    return results

def get_all_groups(filename, group_size=100):
    all_groups = []
    current_group = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                number = float(line.strip())
                current_group.append(number)
                if len(current_group) == group_size:
                    all_groups.append(current_group)
                    current_group = []
            except ValueError:
                continue  # Skip non-numeric lines
    if current_group:  # Add the last group if it's not empty
        all_groups.append(current_group)
    return all_groups

def get_common_languages(gpt4o_baseline, deepl_baseline, google_baseline):
    gpt4o_langs = set(gpt4o_baseline.keys())
    deepl_langs = set(deepl_baseline.keys())
    google_langs = set(google_baseline.keys())
    return list(set.intersection(gpt4o_langs, deepl_langs, google_langs))

def calculate_average(baseline, languages):
    return sum(baseline[lang] for lang in languages) / len(languages)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--experiment_id', type=str, required=True)
    args = parser.parse_args()

    if not args.experiment_id:
        raise ValueError('Experiment ID is required')
    
    Config = Config()
    
    directory = Config.base['paths']['base_path'] + '/evals/' + f'{args.experiment_id}'
    print(directory)
    if not os.path.exists(directory):
        print(f'Experiment {args.experiment_id} does not exist')
        exit(1)
    output_directory = Config.base['paths']['base_path'] + '/evals/' + f'{args.experiment_id}_graphs'
    
    strategy = Config.get_experiment_config(args.experiment_id)['strategy']
    group_size = Config.get_strategy_config(strategy)['passes']
    print(f'Group size: {group_size}')
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory, exist_ok=True)
    
    all_languages_results = []
    
    # Exact GPT-4O baseline averages provided
    averages = {
        'Greek_scores.eval': 0.5945,
        'Arabic_scores.eval': 0.6433,
        'German_scores.eval': 0.7077,
        'Italian_scores.eval': 0.6827,
        'Sinhala_scores.eval': 0.6732,
        'Marathi_scores.eval': 0.6351,
        'Spanish_scores.eval': 0.6565,
        'Tagalog_scores.eval': 0.6002,
        'Urdu_scores.eval': 0.5460,
        'Korean_scores.eval': 0.5860,
        'Bengali_scores.eval': 0.6433,
        'Turkish_scores.eval': 0.6619,
        'Vietnamese_scores.eval': 0.6613,
        'Croatian_scores.eval': 0.7098,
        'Telugu_scores.eval': 0.6190,
        'Romanian_scores.eval': 0.7590,
        'French_scores.eval': 0.7541,
        'Mandarin Chinese_scores.eval': 0.6747,
        'Portuguese_scores.eval': 0.7386,
        'Russian_scores.eval': 0.7061,
        'Hindi_scores.eval': 0.6598,
        'Tamil_scores.eval': 0.6818,
        'Japanese_scores.eval': 0.6562
    }
    
    overall_average = 0.6631
    
    # DeepL baseline
    deepl_baseline = {
        'Greek_scores.eval': 0.5849,
        'Arabic_scores.eval': 0.6395,
        'German_scores.eval': 0.7196,
        'Italian_scores.eval': 0.6871,
        'Spanish_scores.eval': 0.6672,
        'Korean_scores.eval': 0.5938,
        'Portuguese_scores.eval': 0.6841,
        'French_scores.eval': 0.7525,
        'Japanese_scores.eval': 0.6394,
        'Romanian_scores.eval': 0.7798
    }

    # Google baseline
    google_baseline = {
        'Greek_scores.eval': 0.5624,
        'Arabic_scores.eval': 0.6423,
        'German_scores.eval': 0.7047,
        'Italian_scores.eval': 0.6346,
        'Spanish_scores.eval': 0.6751,
        'Korean_scores.eval': 0.6059,
        'Turkish_scores.eval': 0.6529,
        'Portuguese_scores.eval': 0.7504,
        'Russian_scores.eval': 0.7047,
        'French_scores.eval': 0.6813,
        'Japanese_scores.eval': 0.6627,
        'Romanian_scores.eval': 0.7521,
        'Chinese_scores.eval': 0.7030
    }
    
    for filename in os.listdir(directory):
        if filename.endswith('.eval'):
            file_path = os.path.join(directory, filename)
            
            all_groups = get_all_groups(file_path, group_size)
            all_results = [calculate_average_max_for_all_n(group) for group in all_groups]
            average_results = np.mean(all_results, axis=0)
            
            all_languages_results.append(average_results)
            
            # Create and save individual language graph
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(range(1, len(average_results) + 1), average_results)
            
            # Add baseline lines
            language_average = averages.get(filename)
            if language_average is not None:
                ax.axhline(y=language_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {language_average:.4f}')
            
            deepl_average = deepl_baseline.get(filename)
            if deepl_average is not None:
                ax.axhline(y=deepl_average, color='g', linestyle='--', label=f'DeepL Base Line: {deepl_average:.4f}')
            
            google_average = google_baseline.get(filename)
            if google_average is not None:
                ax.axhline(y=google_average, color='b', linestyle='--', label=f'Google Base Line: {google_average:.4f}')
            
            # Add blue dashed line at n = 26 and shade area below
            # ax.axvline(x=26, color='b', linestyle='--')
            #ax.fill_between(range(1, 27), ax.get_ylim()[0], average_results[:26], alpha=0.2, color='b', label='Pricing cheaper than base line')
            
            ax.set_xlabel('n (number of elements chosen)')
            ax.set_ylabel('Average Max Score')
            ax.set_title(f'Average Max Score for Different n Across All Groups in {filename}')
            ax.grid(True)
            ax.legend()
            plt.tight_layout()
            
            output_file = os.path.join(output_directory, f'{os.path.splitext(filename)[0]}_graph.png')
            plt.savefig(output_file)
            plt.close()
            
            print(f"Graph saved for {filename}")
    
    # Create and save the average across all languages graph
    all_languages_average = np.mean(all_languages_results, axis=0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(range(1, len(all_languages_average) + 1), all_languages_average)
    
    # Add red dashed line for overall average
    ax.axhline(y=overall_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {overall_average:.4f}')
    
    # Add blue dashed line at n = 26 and shade area below
    # ax.axvline(x=26, color='b', linestyle='--')
    #ax.fill_between(range(1, 27), ax.get_ylim()[0], all_languages_average[:26], alpha=0.2, color='b', label='Pricing cheaper than base line')
    
    ax.set_xlabel('n (number of elements chosen)')
    ax.set_ylabel('Average Max Score')
    ax.set_title('Average Max Score for Different n Across All Languages')
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    
    output_file = os.path.join(output_directory, 'all_languages_average_graph.png')
    plt.savefig(output_file)
    plt.close()
    
    print("Graph saved for average across all languages")

    # Create and save the average across common languages graph
    common_languages = get_common_languages(averages, deepl_baseline, google_baseline)
    gpt4o_common_average = calculate_average(averages, common_languages)
    deepl_common_average = calculate_average(deepl_baseline, common_languages)
    google_common_average = calculate_average(google_baseline, common_languages)

    common_languages_average = np.mean([result for i, result in enumerate(all_languages_results) 
                                      if os.listdir(directory)[i] in common_languages], axis=0)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(range(1, len(common_languages_average) + 1), common_languages_average)

    # Add baseline lines for common languages averages
    ax.axhline(y=gpt4o_common_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {gpt4o_common_average:.4f}')
    ax.axhline(y=deepl_common_average, color='g', linestyle='--', label=f'DeepL Base Line: {deepl_common_average:.4f}')
    ax.axhline(y=google_common_average, color='b', linestyle='--', label=f'Google Base Line: {google_common_average:.4f}')

    ax.set_xlabel('n (number of elements chosen)')
    ax.set_ylabel('Average Max Score')
    ax.set_title('Average Max Score for Different n Across Common Languages')
    ax.grid(True)
    ax.legend()
    plt.tight_layout()

    output_file = os.path.join(output_directory, 'common_languages_average_graph.png')
    plt.savefig(output_file)
    plt.close()

    print("Graph saved for average across common languages")
    print("All graphs have been generated and saved.")