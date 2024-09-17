import sys
import os
import matplotlib.pyplot as plt
import numpy as np

def calculate_average_max(filename, group_size=100):
    max_values = []
    current_group = []
    
    with open(filename, 'r') as file:
        for line in file:
            try:
                number = float(line.strip())
                current_group.append(number)
                
                if len(current_group) == group_size:
                    max_values.append(max(current_group))
                    current_group = []
            except ValueError:
                continue  # Skip non-numeric lines
    
    # Handle any remaining numbers
    if current_group:
        max_values.append(max(current_group))
    
    if max_values:
        average_max = sum(max_values) / len(max_values)
        return average_max
    else:
        return 0

if __name__ == "__main__":
    directory = '/Users/vijaykumaravelrajan/Downloads/eval_data_gpt-4o'
    results = {}
    group_size = 1  # Default group size, can be changed here

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            result = calculate_average_max(file_path, group_size)
            results[filename] = result

    # Calculate overall average
    overall_average = np.mean(list(results.values()))

    # Output averages to a text file
    output_file = 'averages.txt'
    with open(output_file, 'w') as f:
        for filename, average in results.items():
            f.write(f"{filename}: {average:.4f}\n")
        f.write(f"\nOverall Average: {overall_average:.4f}")

    # Create bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(results.keys(), results.values())
    plt.xlabel('Files')
    plt.ylabel('Average Max Score')
    plt.title(f'Average Max Score for Every {group_size} Numbers in Each File')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Add overall average line
    plt.axhline(y=overall_average, color='r', linestyle='--', label='Overall Average')
    plt.legend()

    # Save the plot as an image file
    plt.savefig('average_max_scores.png')
    plt.close()

    print(f"Results have been saved to {output_file}")
    print(f"Graph has been saved as average_max_scores.png")
    print(f"Overall Average: {overall_average:.4f}")
