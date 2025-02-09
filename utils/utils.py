import os
from utils.config import Config
import dotenv

dotenv.load_dotenv()

def read_lines(file_path, num):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines[:num]

def generate_reference_files(config: Config, experiment_id, output_file_path, target_language=None, ref_output_path=None, no_header_output_path=None):
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
    experiment_config = config.get_experiment_config(experiment_id)
    strategy_name = experiment_config['strategy']
    num_lines = int(header_info.get('NLINES', 0))
    target_language = header_info.get('TARGET')

    if not all([strategy_name, num_lines, target_language]):
        raise ValueError("Missing required information from header or function arguments")

    # Load strategy
    strategy = config.get_strategy_config(strategy_name)
    passes = strategy.get('passes', 1)

    # Determine reference file path
    language_map = {
    # Existing mappings
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
    "Sinhala": "sin_Sinh",
    
    # Additional codes from the image with both language name and two-letter ISO code as keys
    "ZH-HANS": "cmn_Hans",
    "AF": "afr_Latn",
    "SQ": "als_Latn",
    "AM": "amh_Ethi",
    "AR": "arb_Arab",
    "HY": "hye_Armn",
    "AS": "asm_Beng",
    "AY": "ayr_Latn",
    "AZ": "azj_Latn",
    "BM": "bam_Latn",
    "EU": "eus_Latn",
    "BE": "bel_Cyrl",
    "BN": "ben_Beng",
    "BHO": "bho_Deva",
    "BS": "bos_Latn",
    "BG": "bul_Cyrl",
    "CA": "cat_Latn",
    "CEB": "ceb_Latn",
    "ZH-CN": "cmn_Hans",
    "ZH-TW": "cmn_Hant",
    "HR": "hrv_Latn",
    "CS": "ces_Latn",
    "DA": "dan_Latn",
    "NL": "nld_Latn",
    "EO": "epo_Latn",
    "ET": "ekk_Latn",
    "EE": "ewe_Latn",
    "FIL": "fil_Latn",
    "FI": "fin_Latn",
    "FR": "fra_Latn",
    "GL": "glg_Latn",
    "KA": "kat_Geor",
    "DE": "deu_Latn",
    "EL": "ell_Grek",
    "GN": "gug_Latn",
    "GU": "guj_Gujr",
    "HT": "hat_Latn",
    "HA": "hau_Latn",
    "HE": "heb_Hebr",
    "HI": "hin_Deva",
    "HU": "hun_Latn",
    "IS": "isl_Latn",
    "IG": "ibo_Latn",
    "ILO": "ilo_Latn",
    "ID": "ind_Latn",
    "GA": "gle_Latn",
    "IT": "ita_Latn",
    "JA": "jpn_Jpan",
    "JV": "jav_Latn",
    "KN": "kan_Knda",
    "KK": "kaz_Cyrl",
    "KM": "khm_Khmr",
    "RW": "kin_Latn",
    "GOM": "gom_Deva",
    "KO": "kor_Hang",
    "KU": "kmr_Latn",
    "CKB": "ckb_Arab",
    "KY": "kir_Cyrl",
    "LO": "lao_Laoo",
    "LV": "lvs_Latn",
    "LN": "lin_Latn",
    "LT": "lit_Latn",
    "LG": "lug_Latn",
    "LB": "ltz_Latn",
    "MK": "mkd_Cyrl",
    "MAI": "mai_Deva",
    "MG": "plt_Latn",
    "MS": "zsm_Latn",
    "ML": "mal_Mlym",
    "MT": "mlt_Latn",
    "MI": "mri_Latn",
    "MR": "mar_Deva",
    "MNI-MTEI": "mni_Mtei",
    "LUS": "lus_Latn",
    "MN": "khk_Cyrl",
    "MY": "mya_Mymr",
    "NE": "npi_Deva",
    "NO": "nob_Latn",
    "NY": "nya_Latn",
    "OR": "ory_Orya",
    "OM": "gaz_Latn",
    "PS": "pbt_Arab",
    "FA": "pes_Arab",
    "PL": "pol_Latn",
    "PT": "por_Latn",
    "PA": "pan_Guru",
    "QU": "quy_Latn",
    "RO": "ron_Latn",
    "RU": "rus_Cyrl",
    "SM": "smo_Latn",
    "SA": "san_Deva",
    "GD": "gla_Latn",
    "NSO": "nso_Latn",
    "SR": "srp_Cyrl",
    "ST": "sot_Latn",
    "SN": "sna_Latn",
    "SD": "snd_Arab",
    "SI": "sin_Sinh",
    "SK": "slk_Latn",
    "SL": "slv_Latn",
    "SO": "som_Latn",
    "ES": "spa_Latn",
    "SU": "sun_Latn",
    "SW": "swh_Latn",
    "SV": "swe_Latn",
    "TL": "fil_Latn",
    "TG": "tgk_Cyrl",
    "TA": "tam_Taml",
    "TT": "tat_Cyrl",
    "TE": "tel_Telu",
    "TH": "tha_Thai",
    "TI": "tir_Ethi",
    "TS": "tso_Latn",
    "TR": "tur_Latn",
    "TK": "tuk_Latn",
    "AK": "twi_Latn",
    "UK": "ukr_Cyrl",
    "UR": "urd_Arab",
    "UG": "uig_Arab",
    "UZ": "uzn_Latn",
    "VI": "vie_Latn",
    "CY": "cym_Latn",
    "XH": "xho_Latn",
    "YI": "ydd_Hebr",
    "YO": "yor_Latn",
    "ZU": "zul_Latn",
    "zh-hans": "cmn_Hans",
    "af": "afr_Latn",
    "sq": "als_Latn",
    "am": "amh_Ethi",
    "ar": "arb_Arab",
    "hy": "hye_Armn",
    "as": "asm_Beng",
    "ay": "ayr_Latn",
    "az": "azj_Latn",
    "bm": "bam_Latn",
    "eu": "eus_Latn",
    "be": "bel_Cyrl",
    "bn": "ben_Beng",
    "bho": "bho_Deva",
    "bs": "bos_Latn",
    "bg": "bul_Cyrl",
    "ca": "cat_Latn",
    "ceb": "ceb_Latn",
    "zh-cn": "cmn_Hans",
    "zh-tw": "cmn_Hant",
    "hr": "hrv_Latn",
    "cs": "ces_Latn",
    "da": "dan_Latn",
    "nl": "nld_Latn",
    "eo": "epo_Latn",
    "et": "ekk_Latn",
    "ee": "ewe_Latn",
    "fil": "fil_Latn",
    "fi": "fin_Latn",
    "fr": "fra_Latn",
    "gl": "glg_Latn",
    "ka": "kat_Geor",
    "de": "deu_Latn",
    "el": "ell_Grek",
    "gn": "gug_Latn",
    "gu": "guj_Gujr",
    "ht": "hat_Latn",
    "ha": "hau_Latn",
    "he": "heb_Hebr",
    "hi": "hin_Deva",
    "hu": "hun_Latn",
    "is": "isl_Latn",
    "ig": "ibo_Latn",
    "ilo": "ilo_Latn",
    "id": "ind_Latn",
    "ga": "gle_Latn",
    "it": "ita_Latn",
    "ja": "jpn_Jpan",
    "jv": "jav_Latn",
    "kn": "kan_Knda",
    "kk": "kaz_Cyrl",
    "km": "khm_Khmr",
    "rw": "kin_Latn",
    "gom": "gom_Deva",
    "ko": "kor_Hang",
    "ku": "kmr_Latn",
    "ckb": "ckb_Arab",
    "ky": "kir_Cyrl",
    "lo": "lao_Laoo",
    "lv": "lvs_Latn",
    "ln": "lin_Latn",
    "lt": "lit_Latn",
    "lg": "lug_Latn",
    "lb": "ltz_Latn",
    "mk": "mkd_Cyrl",
    "mai": "mai_Deva",
    "mg": "plt_Latn",
    "ms": "zsm_Latn",
    "ml": "mal_Mlym",
    "mt": "mlt_Latn",
    "mi": "mri_Latn",
    "mr": "mar_Deva",
    "mni-mtei": "mni_Mtei",
    "lus": "lus_Latn",
    "mn": "khk_Cyrl",
    "my": "mya_Mymr",
    "ne": "npi_Deva",
    "no": "nob_Latn",
    "ny": "nya_Latn",
    "or": "ory_Orya",
    "om": "gaz_Latn",
    "ps": "pbt_Arab",
    "fa": "pes_Arab",
    "pl": "pol_Latn",
    "pt": "por_Latn",
    "pa": "pan_Guru",
    "qu": "quy_Latn",
    "ro": "ron_Latn",
    "ru": "rus_Cyrl",
    "sm": "smo_Latn",
    "sa": "san_Deva",
    "gd": "gla_Latn",
    "nso": "nso_Latn",
    "sr": "srp_Cyrl",
    "st": "sot_Latn",
    "sn": "sna_Latn",
    "sd": "snd_Arab",
    "si": "sin_Sinh",
    "sk": "slk_Latn",
    "sl": "slv_Latn",
    "so": "som_Latn",
    "es": "spa_Latn",
    "su": "sun_Latn",
    "sw": "swh_Latn",
    "sv": "swe_Latn",
    "tl": "fil_Latn",
    "tg": "tgk_Cyrl",
    "ta": "tam_Taml",
    "tt": "tat_Cyrl",
    "te": "tel_Telu",
    "th": "tha_Thai",
    "ti": "tir_Ethi",
    "ts": "tso_Latn",
    "tr": "tur_Latn",
    "tk": "tuk_Latn",
    "ak": "twi_Latn_akua1239",
    "uk": "ukr_Cyrl",
    "ur": "urd_Arab",
    "ug": "uig_Arab",
    "uz": "uzn_Latn",
    "vi": "vie_Latn",
    "cy": "cym_Latn",
    "xh": "xho_Latn",
    "yi": "ydd_Hebr",
    "yo": "yor_Latn",
    "zu": "zul_Latn"
}

    lang_code = language_map.get(target_language)
    if not lang_code:
        return None, None
    
    ref_file_path = f"{config.base['paths']['base_flores']}/devtest.{lang_code}"

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
