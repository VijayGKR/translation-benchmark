import json
import os

def read_lines(file_path, num):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines[:num]

def load_strategy(strategy_name):
    with open('strategies.json', 'r') as f:
        strategies = json.load(f)
    if strategy_name not in strategies:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    return strategies[strategy_name]

def generate_reference_files(output_file_path, ref_output_path=None, no_header_output_path=None):
    # Read the header of the output file
    with open(output_file_path, 'r', encoding='utf-8') as f:
        header_lines = []
        for line in f:
            if line.strip() == '':
                break
            header_lines.append(line.strip())
    
    # Parse header information
    header_info = dict(line.split(' ', 1) for line in header_lines if ' ' in line)
    
    # Use header information, falling back to function parameters if not found
    strategy_name = header_info.get('STRATEGY_NAME')
    num_lines = int(header_info.get('NLINES', 0))
    target_language = header_info.get('TARGET')

    if not all([strategy_name, num_lines, target_language]):
        raise ValueError("Missing required information from header or function arguments")

    # Load strategy
    strategy = load_strategy(strategy_name)
    passes = strategy.get('passes', 1)

    # Determine reference file path
    language_map = {
        "Hindi": "hin_Deva",
        "Russian": "rus_Cyrl",
        "Arabic": "arb_Arab",
        "Spanish": "spa_Latn",
        "Japanese": "jpn_Jpan",
        "German": "deu_Latn",
        "Mandarin Chinese": "cmn_Hans",
        "French": "fra_Latn",
        "Korean": "kor_Hang",
        "Italian": "ita_Latn",
        "Bengali": "ben_Beng",
        "Urdu": "urd_Arab",
        "Greek": "ell_Grek",
        "Portuguese": "por_Latn",
        "Tamil": "tam_Taml",
        "Vietnamese": "vie_Latn",
        "Romanian": "ron_Latn",
        "Turkish": "tur_Latn",
        "Marathi": "mar_Deva",
        "Telugu": "tel_Telu",
        "Tagalog": "fil_Latn",
        "Croatian": "hrv_Latn",
        "Sinhala": "sin_Sinh"
    }
    lang_code = language_map.get(target_language)
    if not lang_code:
        raise ValueError(f"Unsupported target language: {target_language}")
    
    ref_file_path = f"/Users/vijaykumaravelrajan/Downloads/floresp-v2.0-rc.3/devtest/devtest.{lang_code}"

    # Read lines from reference file
    ref_lines = read_lines(ref_file_path, num_lines)

    # Generate reference content
    ref_content = []
    for line in ref_lines:
        ref_content.extend([line] * passes)

    # Determine output file paths
    if ref_output_path is None:
        ref_output_path = f"{os.path.splitext(output_file_path)[0]}.ref"
    if no_header_output_path is None:
        no_header_output_path = f"{os.path.splitext(output_file_path)[0]}.no_header"

    # Write reference content to the specified file
    with open(ref_output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(ref_content))

    # Write the content without header to the specified file
    with open(no_header_output_path, 'w', encoding='utf-8') as f:
        f.writelines(line for line in open(output_file_path, 'r', encoding='utf-8') if line.strip() and not any(key in line for key in header_info))

    return ref_output_path, no_header_output_path
