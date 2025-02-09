import sys
import os
import matplotlib.pyplot as plt
import numpy as np
from math import comb
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
if __name__ == "__main__":
    directory = '/Users/vijaykumaravelrajan/translation-benchmark/COMET_WMT20_EVAL'
    output_directory = 'Compute_Graphs_By_Language_COMET20'
    
    os.makedirs(output_directory, exist_ok=True)
    
    all_languages_results = []
    
    # Exact averages provided
    averages = {
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
    
    overall_average = 0.6631
    
    for filename in os.listdir(directory):
        if filename.endswith('.eval'):
            file_path = os.path.join(directory, filename)
            
            all_groups = get_all_groups(file_path)
            all_results = [calculate_average_max_for_all_n(group) for group in all_groups]
            average_results = np.mean(all_results, axis=0)
            
            all_languages_results.append(average_results)
            
            # Create and save individual language graph
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(range(1, len(average_results) + 1), average_results)
            
            # Add red dashed line for language average
            language_average = averages.get(filename)
            if language_average is not None:
                ax.axhline(y=language_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {language_average:.4f}')
            
            # Add blue dashed line at n = 26 and shade area below
            ax.axvline(x=26, color='b', linestyle='--')
            ax.fill_between(range(1, 27), ax.get_ylim()[0], average_results[:26], alpha=0.2, color='b', label='Pricing cheaper than base line')
            
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
    #ax.axhline(y=overall_average, color='r', linestyle='--', label=f'GPT-4O Base Line: {overall_average:.4f}')
    
    # Add blue dashed line at n = 26 and shade area below
    ax.axvline(x=26, color='b', linestyle='--')
    ax.fill_between(range(1, 27), ax.get_ylim()[0], all_languages_average[:26], alpha=0.2, color='b', label='Pricing cheaper than base line')
    
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
    print("All graphs have been generated and saved.")