import deepl
import os
import dotenv
dotenv.load_dotenv()

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
      self

# 30 langs, 100 lines
def getMachineTranslation():
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

if __name__ == "__main__":
  getMachineTranslation()