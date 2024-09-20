from comet import download_model, load_from_checkpoint
import os

class Reward:
    def __init__(self):
        self.model = None

    def get_reward():
        print("choose a child class")

class CometKiwiReward(Reward):
    def __init__(self):
        model_name = "Unbabel/wmt22-cometkiwi-da"
        model_path = download_model(model_name)
        self.model = load_from_checkpoint(model_path)

    def get_reward(self, source, mt, n_pass, n_lines):
        source_lines = []
        mt_lines = []

        # Read input files and convert to lists
        with open(source, 'r') as file:
          source_lines = file.readlines()

        source_lines = source_lines[:n_lines]
        # print(len(source_lines))

        n_source_lines = []
        for line in source_lines:
            n_source_lines.extend([line]*n_pass)
    
        with open(mt, 'r') as file:
          mt_lines = file.readlines()
        
        # print(len(n_source_lines))
        # print(len(mt_lines))
        # parse the data into comet format
        data = [
            { "src": src, "mt": mt_} for src, mt_ in zip(n_source_lines, mt_lines)
        ]
        model_output = self.model.predict(data, batch_size=8, gpus=0)
        return model_output
    
class LLMJudge(Reward):
    def __init__(self, model, ):
        self.model = 'openai'

    def get_reward(self, source, target):
        return self.model.predict(source, target)

if __name__ == "__main__":
    reward = CometKiwiReward()
    # reward.get_reward("example_files/source.txt", "example_files/generated.txt")
    #reward.get_reward("floresp-v2.0-rc.3/devtest/devtest.eng_Latn", "floresp-v2.0-rc.3/devtest/devtest.kor_Hang")
    # reward.get_reward("example_files/english_gt.txt", "example_files/arabic_mt.txt")
    # reward.get_reward("example_files/english_gt.txt", "example_files/arabic_gt.txt")
    dir_name = "output_english_to_all"
    model_name = 'gpt-4o-mini'
    language_list = ['Arabic', 'Bengali', 'Croatian', 'French', 'German', 'Greek', 'Hindi', 'Italian', 'Japanese', 'Korean', 'Mandarin Chinese', 'Marathi', 'Portuguese', 'Romanian', 'Russian', 'Sinhala', 'Spanish', 'Tagalog', 'Tamil', 'Telugu', 'Turkish', 'Urdu', 'Vietnamese']

    n_pass = 100
    n_lines = 50

    for language in language_list:
        reward_list = reward.get_reward("floresp-v2.0-rc.3/devtest/devtest.eng_Latn", f"{dir_name}/{model_name}_English_to_{language}.candidates", n_pass=n_pass, n_lines=n_lines)
        reward_list = reward_list['scores']
        reward_list = [str(reward)+'\n' for reward in reward_list]
        with open(f"COMET_QE/{model_name}_English_to_{language}.reward", 'w') as file:
            file.writelines(reward_list)
