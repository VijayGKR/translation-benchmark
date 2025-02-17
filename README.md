# Translation Benchmark

This project benchmarks translation quality by leveraging BLEURT as a neural evaluation metric and using the FLORES+ corpus as a parallel dataset. All supported models rely on asynchronous calls to Openrouter.

## Getting Started

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```bash
   git clone <repository-url>
   ```

2. **Obtain the FLORES+ Corpus**  
   Download the FLORES+ corpus from Hugging Face:  
   [FLORES+ Dataset on Hugging Face](https://huggingface.co/datasets/openlanguagedata/flores_plus)  
   *Note: You will need a Hugging Face account to access the dataset.*

3. **Configure the Environment**  
   - Create a `.env` file based on the provided example (`.env.example`)
   - Set your Openrouter API key in the `.env` file
   - For the `FLORES_PATH` variable, set the absolute path to your unzipped FLORES+ folder
   - Set the `BASE_PATH` variable to the absolute path of your project directory

4. **Install Dependencies**  
   (Optional) Create a virtual environment named `venv` (it will be automatically excluded by `.gitignore`):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   otherwise, just run 
   ```
   pip install -r requirements.txt
   ```

## Translation Evaluation Workflow

### 1. Generate Translations

1. **Configure Your Experiment**  
   - Modify `experiments.yaml` to define your experiment parameters
   - To add a new model, update the models.yaml file by adding a name as well a corresponding api name
     - You can find the api name for a model by going to https://openrouter.ai/models, and copying the api name string in grey

2. **Run the Translation Driver**  
   Execute the driver script with your experiment ID:
   ```bash
   python driver.py --experiment_id your_experiment_id
   ```
   *Note: The Openrouter API may occasionally return errors. You can either modify the experiment yaml to retry failed languages or improve the error handling.*
   To test your installation, run the 4o-mini-test experiment

3. **Verify the Outputs**  
   Check that your generated .references files match the formats in the `examples` folder.

### 2. Evaluate Translation Quality

BLEURT evaluation requires GPU resources. You can either:
- Run locally if you have GPU support
- Use Google Colab (recommended)

#### Using Google Colab:
1. Upload your experiment output folder to Google Drive
2. Open and run the provided iPython notebook
3. Configure the file paths in the notebook to match your setup
4. The notebook will generate `.eval` files containing scores for each translation

#### Using Local GPU:
1. Install BLEURT and its dependencies
2. Modify the evaluation script to handle local paths
3. Run the evaluation on your local machine

### 3. Generate Coverage Analysis

After obtaining the evaluation scores:
1. Move the `.eval` files to your project's `evals` folder
2. Run the coverage analysis:
   ```bash
   python coverage.py --experiment_id your_experiment_id
   ```
3. Review the generated coverage graphs in the `evals/your_experiment_id_graphs` folder

## Reference Implementation
Sample files for a complete pass of Gemini 2.0 Flash are provided in the repository. Check the `experiments.yaml` file for its configuration details.
