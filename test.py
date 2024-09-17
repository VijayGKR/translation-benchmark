import os
from utils import generate_reference_files

output_folder = 'output_english_to_all'
for output_file in os.listdir(output_folder):
    if output_file.endswith('.txt'):
        output_file_path = os.path.join(output_folder, output_file)
        ref_output_path = output_file_path.replace('.txt', '.references')
        no_header_output_path = output_file_path.replace('.txt', '.candidates')
        generate_reference_files(output_file_path, ref_output_path=ref_output_path, no_header_output_path=no_header_output_path)