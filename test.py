import os
from utils import generate_reference_files

output_folder = 'closed_source_eval/googletranslate_llm'

for output_file in os.listdir(output_folder):
    if output_file.endswith('.txt'):
        output_file_path = os.path.join(output_folder, output_file)
        # Get everything before .txt in the file name
        base_name = os.path.splitext(output_file)[0]
        ref_output_path = output_file_path.replace('.txt', '.references')
        no_header_output_path = output_file_path.replace('.txt', '.candidates')
        try:
            generate_reference_files(output_file_path, strategy_name='pass@1-vanilla', num_lines=100, target_language=base_name, ref_output_path=ref_output_path, no_header_output_path=no_header_output_path)
        except Exception as e:
            print(f"Error processing {output_file}: {str(e)}")