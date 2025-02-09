# Translation Benchmark

This project benchmarks translation quality by leveraging BLEURT as a neural evaluation metric and using the FLORES+ corpus as a parallel dataset. All supported models rely on asynchronous calls to Openrouter.

## Getting Started

1. **Clone the Repository**  
   Clone this repository to your local machine:
   ```
   git clone <repository-url>
   ```

2. **Obtain the FLORES+ Corpus**  
   Download the FLORES+ corpus from Hugging Face:  
   [FLORES+ Dataset on Hugging Face](https://huggingface.co/datasets/openlanguagedata/flores_plus)  
   *Note: You will need a Hugging Face account to access the dataset.*

3. **Configure the Environment**  
   - Create a `.env` file based on the provided example (e.g., `.env.example`).  
   - In the `.env` file, set your Openrouter API key.  
   - For the `FLORES_PATH` variable, copy the unzipped folder to your workspace and run `pwd` (or an equivalent command) to get its absolute path.

4. **Install Dependencies**  
   If you decide to use a virtual environment, name it `venv` (it will be automatically excluded by `.gitignore`).  
   Install project dependencies with:
   ```
   pip install -r requirements.txt
   ```

## Generating Translations

1. **Configure Your Experiment**  
   Modify the `experiments.yaml` and `models.yaml` files (consult the Openrouter documentation for details) to match your specific requirements.

2. **Run the Translation Driver**  
   Execute the driver script with your experiment ID. For example, if your experiment ID is `gpt_4o_mini_English_to_All`, run:
   ```
   python driver.py --experiment_id gpt_4o_mini_English_to_All
   ```

3. **Verify the Outputs**  
   Check the generated output files against the formats provided in the `examples` folder.

