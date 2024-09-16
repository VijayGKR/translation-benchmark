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

    def get_reward(self, source, mt):
        source_lines = []
        mt_lines = []

        # Read input files and convert to lists
        with open(source, 'r') as file:
          source_lines = file.readlines()
        with open(mt, 'r') as file:
          mt_lines = file.readlines()
        
        # parse the data into comet format
        data = [
            { "src": src, "mt": mt_} for src, mt_ in zip(source_lines, mt_lines)
        ]
        model_output = self.model.predict(data, batch_size=8, gpus=0)
        print(model_output)
    
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
    reward.get_reward("example_files/english_gt.txt", "example_files/tamil_mt.txt")
    reward.get_reward("example_files/english_gt.txt", "example_files/tamil_gt.txt")