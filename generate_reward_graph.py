import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from math import comb
from functools import reduce


def calculate_average_max_for_all_n_2(group1, group2):
    results = []
    # Combine group1 and group2 into tuples
    combined = list(zip(group1, group2))
    
    # Sort the combined list based on the second element (group2) in ascending order
    sorted_combined = sorted(combined, key=lambda x: x[1])
    group_size = len(sorted_combined)
     # Sort the group in descending order
    
    for n in range(1, group_size + 1):
        sum_of_maximums = sum(sorted_combined[k-1][0] * comb(k-1, n-1) for k in range(n, group_size + 1))
        average_max = sum_of_maximums / comb(group_size, n)
        results.append(average_max)
    
    return results


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

def get_all_groups(filename, filename2, group_size=100):
    all_groups = []
    all_groups2 = []
    current_group = []
    current_group2 = []
    
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
    
    with open(filename2, 'r') as file:
        for line in file:
            try:
                number = float(line.strip())
                current_group2.append(number)
                if len(current_group2) == group_size:
                    all_groups2.append(current_group2)
                    current_group2 = []
            except ValueError:
                continue  # Skip non-numeric lines
    if current_group2:  # Add the last group if it's not empty
        all_groups2.append(current_group2)
    
    return all_groups, all_groups2


def get_common_languages(gpt4o_baseline, deepl_baseline, google_baseline):
    gpt4o_langs = set(gpt4o_baseline.keys())
    deepl_langs = set(deepl_baseline.keys())
    google_langs = set(google_baseline.keys())
    return list(reduce(set.intersection, [gpt4o_langs, deepl_langs, google_langs]))

def calculate_average(baseline, languages):
    return sum(baseline[lang] for lang in languages) / len(languages)

if __name__ == "__main__":
    directory = '/Users/vijaykumaravelrajan/translation-benchmark/GEMINI_REWARD'
    output_directory = 'Compute_Reward_Graphs_By_Language_GEMINI'
    
    os.makedirs(output_directory, exist_ok=True)
    
    all_languages_results = []
    common_languages_results = []
    
    # GPT-4O baseline (keeping all existing scores)
    gpt4o_baseline = {
        'Greek_scores.txt': 0.5945,
        'Arabic_scores.txt': 0.6433,
        'German_scores.txt': 0.7077,
        'Italian_scores.txt': 0.6827,
        'Sinhala_scores.txt': 0.6732,
        'Marathi_scores.txt': 0.6351,
        'Spanish_scores.txt': 0.6565,
        'Tagalog_scores.txt': 0.6002,
        'Urdu_scores.txt': 0.5460,
        'Korean_scores.txt': 0.5860,
        'Bengali_scores.txt': 0.6433,
        'Turkish_scores.txt': 0.6619,
        'Vietnamese_scores.txt': 0.6613,
        'Croatian_scores.txt': 0.7098,
        'Telugu_scores.txt': 0.6190,
        'Romanian_scores.txt': 0.7590,
        'French_scores.txt': 0.7541,
        'Mandarin Chinese_scores.txt': 0.6747,
        'Portuguese_scores.txt': 0.7386,
        'Russian_scores.txt': 0.7061,
        'Hindi_scores.txt': 0.6598,
        'Tamil_scores.txt': 0.6818,
        'Japanese_scores.txt': 0.6562
    }
    
    # DeepL baseline
    deepl_baseline = {
        'Danish_scores.txt': 0.7384,
        'Spanish_scores.txt': 0.6672,
        'Latvian_scores.txt': 0.7219,
        'Arabic_scores.txt': 0.6395,
        'Hungarian_scores.txt': 0.6795,
        'Czech_scores.txt': 0.7344,
        'Italian_scores.txt': 0.6871,
        'Lithuanian_scores.txt': 0.7260,
        'Dutch_scores.txt': 0.6564,
        'Norwegian_scores.txt': 0.7551,
        'Bulgarian_scores.txt': 0.6759,
        'German_scores.txt': 0.7196,
        'Korean_scores.txt': 0.5938,
        'Indonesian_scores.txt': 0.7381,
        'Greek_scores.txt': 0.5849,
        'Polish_scores.txt': 0.6982,
        'Portuguese_scores.txt': 0.6841,
        'French_scores.txt': 0.7525,
        'Japanese_scores.txt': 0.6394,
        'Romanian_scores.txt': 0.7798,
        'Finnish_scores.txt': 0.6777
    }
    
    # Google baseline (new)
    google_baseline = {
        'Danish_scores.txt': 0.7165,
        'Spanish_scores.txt': 0.6751,
        'Latvian_scores.txt': 0.7298,
        'Swedish_scores.txt': 0.7105,
        'Arabic_scores.txt': 0.6423,
        'Hungarian_scores.txt': 0.6605,
        'Turkish_scores.txt': 0.6529,
        'Czech_scores.txt': 0.7086,
        'Italian_scores.txt': 0.6346,
        'Lithuanian_scores.txt': 0.7281,
        'Dutch_scores.txt': 0.6506,
        'Russian_scores.txt': 0.7047,
        'Norwegian_scores.txt': 0.8290,
        'Ukrainian_scores.txt': 0.6649,
        'Bulgarian_scores.txt': 0.6866,
        'German_scores.txt': 0.7047,
        'Korean_scores.txt': 0.6059,
        'Indonesian_scores.txt': 0.7385,
        'Greek_scores.txt': 0.5624,
        'Slovenian_scores.txt': 0.6706,
        'Polish_scores.txt': 0.6935,
        'Slovak_scores.txt': 0.7135,
        'Portuguese_scores.txt': 0.7504,
        'French_scores.txt': 0.6813,
        'Japanese_scores.txt': 0.6627,
        'Romanian_scores.txt': 0.7521,
        'Finnish_scores.txt': 0.6480,
        'Chinese_scores.txt': 0.7030
    }
    
    # Calculate common languages
    common_languages = get_common_languages(gpt4o_baseline, deepl_baseline, google_baseline)

    # Calculate overall averages for all languages
    gpt4o_overall_average = calculate_average(gpt4o_baseline, gpt4o_baseline.keys())
    deepl_overall_average = 0.6928  # Use the provided overall average
    google_overall_average = 0.6886  # Use the provided overall average

    # Calculate averages for common languages
    gpt4o_common_average = calculate_average(gpt4o_baseline, common_languages)
    deepl_common_average = calculate_average(deepl_baseline, common_languages)
    google_common_average = calculate_average(google_baseline, common_languages)

    for filename in os.listdir(directory):

        if filename.endswith('.txt'):
            print(filename)
            # Extract the language name from the filename
            language = filename.split('_')[0]
            
            # Find the corresponding .reward file
            reward_file = None
            for file in os.listdir(directory):
                if file.endswith('.reward') and language in file:
                    reward_file = file
                    break
            
            if reward_file is None:
                print(f"No corresponding .reward file found for {filename}")
                continue
            
            file_path = os.path.join(directory, filename)
            reward_path = os.path.join(directory, reward_file)
            
            group1, group2 = get_all_groups(file_path, reward_path)
            all_results = [calculate_average_max_for_all_n_2(g1, g2) for g1, g2 in zip(group1, group2)]
            average_results = np.mean(all_results, axis=0)
            
            all_languages_results.append(average_results)
            
            if filename in common_languages:
                common_languages_results.append(average_results)
            
            # Create and save individual language graph
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(range(1, len(average_results) + 1), average_results)
            
            # Add red dashed line for GPT-4O baseline
            #gpt4o_average = gpt4o_baseline.get(filename)
            #if gpt4o_average is not None:
               #ax.axhline(y=gpt4o_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {gpt4o_average:.4f}')
            
            # Add green dashed line for DeepL baseline if available
            #deepl_average = deepl_baseline.get(filename)
            #if deepl_average is not None:
               # ax.axhline(y=deepl_average, color='g', linestyle='--', label=f'DeepL Base Line: {deepl_average:.4f}')
            
            # Add blue dashed line for Google baseline if available
            #google_average = google_baseline.get(filename)
            #if google_average is not None:
               # ax.axhline(y=google_average, color='b', linestyle='--', label=f'Google Base Line: {google_average:.4f}')
            
            # Add vertical dashed line at n = 26 and shade area below
            ##ax.axvline(x=26, color='purple', linestyle='--')
            #ax.fill_between(range(1, 27), ax.get_ylim()[0], average_results[:26], alpha=0.2, color='purple', label='Pricing cheaper than base line')
            
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
    
    # Add baseline lines for overall averages (all languages)
    ax.axhline(y=gpt4o_overall_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {gpt4o_overall_average:.4f}')
    #ax.axhline(y=deepl_overall_average, color='g', linestyle='--', label=f'DeepL Base Line: {deepl_overall_average:.4f}')
    #ax.axhline(y=google_overall_average, color='b', linestyle='--', label=f'Google Base Line: {google_overall_average:.4f}')
    
    # Add vertical dashed line at n = 26 and shade area below
    ax.axvline(x=26, color='purple', linestyle='--')
    ax.fill_between(range(1, 27), ax.get_ylim()[0], all_languages_average[:26], alpha=0.2, color='purple', label='Pricing cheaper than base line')
    
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
    common_languages_average = np.mean(common_languages_results, axis=0)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(range(1, len(common_languages_average) + 1), common_languages_average)
    
    # Add baseline lines for common languages averages
    ax.axhline(y=gpt4o_common_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {gpt4o_common_average:.4f}')
    #ax.axhline(y=deepl_common_average, color='g', linestyle='--', label=f'DeepL Base Line: {deepl_common_average:.4f}')
    #ax.axhline(y=google_common_average, color='b', linestyle='--', label=f'Google Base Line: {google_common_average:.4f}')
    
    # Add vertical dashed line at n = 26 and shade area below
    ax.axvline(x=26, color='purple', linestyle='--')
    ax.fill_between(range(1, 27), ax.get_ylim()[0], common_languages_average[:26], alpha=0.2, color='purple', label='Pricing cheaper than base line')
    
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