import argparse
import asyncio
import json
import textwrap
from typing import List, Dict, Any
from utils.utils import read_lines
from utils.config import Config
from models import LLM, LLMRateLimitError, LLMError

async def executeCalls(calls: List[Dict[str, Any]]) -> List[str]:
    """Execute a batch of LLM calls with retries"""
    async def make_call(llm: LLM, prompt: str, system_prompt: str, temperature: float) -> str:
        for _ in range(3):  # 3 retries
            try:
                return await llm(prompt, system_prompt, temperature)
            except LLMRateLimitError as e:
                print(e)
                print(f"{llm.model_name} rate limited. Waiting {e.cooldown} seconds before retrying...")
                await asyncio.sleep(e.cooldown)
            except LLMError as e:
                print(e)
                print(f"Error calling {llm.model_name}: {str(e)}")
                raise

    # Create a single LLM instance for all calls
    llm = LLM(calls[0]['model'])
    
    tasks = [
        make_call(
            llm,
            call['prompt'],
            call['system_prompt'],
            call['temperature']
        ) for call in calls
    ]

    results = await asyncio.gather(*tasks)
    return results

def generateCalls(config: Config, experiment_id: str, out_lang: str) -> List[Dict[str, Any]]:
    """Generate the list of LLM calls for the experiment"""
    experiment_config = config.get_experiment_config(experiment_id)
    print(experiment_config)
    strategy_config = config.get_strategy_config(experiment_config['strategy'])
    model_config = config.get_model_config(experiment_config['model'])
    in_lang = experiment_config['source_language']
    source_file = experiment_config['in_file']

    
    sources = read_lines(source_file, experiment_config['num_lines'])
    calls = []

    for source in sources:
        system_prompt = strategy_config['system_prompt'].format(
            in_lang=in_lang,
            out_lang=out_lang
        )
        prompt = strategy_config['prompt_template'].format(
            in_lang=in_lang,
            out_lang=out_lang,
            source=source
        )
        
        for _ in range(strategy_config['passes']):
            calls.append({
                'model': model_config['api_name'],
                'prompt': prompt,
                'system_prompt': system_prompt,
                'temperature': experiment_config.get('temperature', strategy_config['temperature'])
            })

    print(f"Generating with model: {experiment_config['model']}")
    print(f"Input language: {in_lang}")
    print(f"Output language: {out_lang}")
    print(f"Source file: {source_file}")
    print(f"Strategy: {experiment_config['strategy']}")
    print(f"Number of lines: {experiment_config['num_lines']}")

    return calls

def process_results(results: List[str], args: argparse.Namespace, config: Config) -> None:
    """Process and write results to output file"""
    experiment_config = config.get_experiment_config(args.experiment_id)
    
    header = textwrap.dedent(f"""
        MODELNAME {experiment_config['model']}
        NLINES {experiment_config['num_lines']}
        STRATEGY_NAME {experiment_config['strategy']}
        SOURCEFILE {experiment_config['in_file']}
        SOURCE {experiment_config['source_language']}
        TARGET {args.out_lang}
    """).strip()
    
    translations = [result.strip() for result in results]
    output = header + "\n\n" + "\n".join(translations)
    
    with open(args.out_file, 'w', encoding='utf-8') as f:
        f.write(output)

async def main():
    parser = argparse.ArgumentParser(description="Language Translation benchmark")
    parser.add_argument("experiment_id", help="Experiment ID from config")
    parser.add_argument("out_file", help="Output file")
    parser.add_argument("out_lang", help="Output language")

    args = parser.parse_args()
    config = Config()

    try:
        calls = generateCalls(config, args.experiment_id, args.out_lang)
        results = await executeCalls(calls)
        process_results(results, args, config)
        print(f"Results written to {args.out_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
