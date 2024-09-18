import deepl
import os
import dotenv
dotenv.load_dotenv()
from google.cloud import translate 

class DeepL():
    def __init__(self):
      self.translator = deepl.Translator(os.getenv('DEEPL_API_KEY'))

      self.target_langs = [
        'AR',
        'BG',
        'CS',
        'DA',
        'DE',
        'EL',
        'EN-US',
        'ES',
        'ET',
        'FI',
        'FR',
        'HU',
        'ID',
        'IT',
        'JA',
        'KO',
        'LT',
        'LV',
        'NB',
        'NL',
        'PL',
        'PT-PT',
        'RO',
        'RU',
        'SK',
        'SL',
        'SV',
        'TR',
        'UK',
        'ZH-HANS'
      ]

    def getResult(self, source_text, target_lang):
      return self.translator.translate_text(source_text, target_lang=target_lang).text
    
class GoogleTranslate():
    def __init__(self):
        self.project_id = "translationbenchmark"
        self.client = translate.TranslationServiceClient()
        self.location = "us-central1"
        self.parent = f"projects/{self.project_id}/locations/{self.location}"

        # target langs pulled 
        # removed en from nmt
        self.target_langs_nmt = [
          "af",
          "sq",
          "am",
          "ar",
          "hy",
          "as",
          "ay",
          "az",
          "bm",
          "eu",
          "be",
          "bn",
          "bho",
          "bs",
          "bg",
          "ca",
          "ceb",
          "zh-CN",
          "zh-TW",
          "co",
          "hr",
          "cs",
          "da",
          "dv",
          "doi",
          "nl",
          "eo",
          "et",
          "ee",
          "fil",
          "fi",
          "fr",
          "fy",
          "gl",
          "ka",
          "de",
          "el",
          "gn",
          "gu",
          "ht",
          "ha",
          "haw",
          "he",
          "hi",
          "hmn",
          "hu",
          "is",
          "ig",
          "ilo",
          "id",
          "ga",
          "it",
          "ja",
          "jv",
          "kn",
          "kk",
          "km",
          "rw",
          "gom",
          "ko",
          "kri",
          "ku",
          "ckb",
          "ky",
          "lo",
          "la",
          "lv",
          "ln",
          "lt",
          "lg",
          "lb",
          "mk",
          "mai",
          "mg",
          "ms",
          "ml",
          "mt",
          "mi",
          "mr",
          "mni-Mtei",
          "lus",
          "mn",
          "my",
          "ne",
          "no",
          "ny",
          "or",
          "om",
          "ps",
          "fa",
          "pl",
          "pt",
          "pa",
          "qu",
          "ro",
          "ru",
          "sm",
          "sa",
          "gd",
          "nso",
          "sr",
          "st",
          "sn",
          "sd",
          "si",
          "sk",
          "sl",
          "so",
          "es",
          "su",
          "sw",
          "sv",
          "tl",
          "tg",
          "ta",
          "tt",
          "te",
          "th",
          "ti",
          "ts",
          "tr",
          "tk",
          "ak",
          "uk",
          "ur",
          "ug",
          "uz",
          "vi",
          "cy",
          "xh",
          "yi",
          "yo",
          "zu"
        ]
      
        self.target_langs_llm = [
          'AR',
          'ZH-CN',
          'FR',
          'DE',
          'HI',
          'IT',
          'JA',
          'KO',
          'PT',
          'RU',
          'ES'
        ]
    
    def getResult(self, source_text, target_lang, model):
      # general/nmt or general/translation-llm
      model_path = f"{self.parent}/models/{model}"
      response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": [source_text],
                "mime_type": "text/plain",
                "target_language_code": target_lang,
                "source_language_code": "en",
                "model": model_path,
            }
        )
      return response.translations[0].translated_text


# 30 langs, 100 lines
def getDeepLTranslation():
  deepl = DeepL()

  english_gt_path = "floresp-v2.0-rc.3/devtest/devtest.eng_Latn"
  english_gt = []
  with open(english_gt_path, 'r') as file:
    english_gt = file.readlines()

  english_gt = english_gt[:100]
  print(len(english_gt))

  for lang in deepl.target_langs:
    with open(f'closed_source_eval/deepl/{lang}.txt', 'w') as file:
      for line in english_gt:
        file.write(str(deepl.getResult(line, lang)))
    print("wrote to ", lang)

# 30 langs, 100 lines
def getGoogleTranslation():
  google = GoogleTranslate()
  english_gt_path = "floresp-v2.0-rc.3/devtest/devtest.eng_Latn"
  english_gt = []
  with open(english_gt_path, 'r') as file:
    english_gt = file.readlines()

  english_gt = english_gt[:100]
  print(len(english_gt))

  # for lang in google.target_langs_nmt:
  #   with open(f'closed_source_eval/googletranslate_nmt/{lang}.txt', 'w') as file:
  #     for line in english_gt:
  #       file.write(str(google.getResult(line, lang, "general/nmt")))
  #   print("wrote to ", lang)
  
  for lang in google.target_langs_llm:
    with open(f'closed_source_eval/googletranslate_llm/{lang}.txt', 'w') as file:
      for line in english_gt:
        file.write(str(google.getResult(line, lang, "general/translation-llm"))+'\n')
    print("wrote to ", lang)

if __name__ == "__main__":
  getGoogleTranslation()
