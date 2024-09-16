import argparse
import asyncio
import aiohttp
import json
import textwrap
from utils import read_lines, load_strategy
from models import MODELS
from models import OpenAILLM, GoogleLLM, AnthropicLLM, TogetherLLM


async def executeCalls(calls):
    async def make_call(llm, prompt, system_prompt, temperature):
        return await llm(prompt, system_prompt, temperature)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for call in calls:
            llm_type = call['model_version']
            if llm_type == 'OpenAI':
                llm = OpenAILLM(call['llm'], session)
            elif llm_type == 'Anthropic':
                llm = AnthropicLLM(call['llm'], session)
            elif llm_type == 'Google':
                llm = GoogleLLM(call['llm'], session)
            elif llm_type == 'Together':
                llm = TogetherLLM(call['llm'], session, model_name='gpt-4o')
            else:
                raise ValueError(f"Unknown LLM type: {llm_type}")
            
            tasks.append(make_call(llm, call['prompt'], call['system_prompt'], call['temperature']))

        results = await asyncio.gather(*tasks)
        return results


def generateCalls(llm, in_lang, out_lang, source_file, out_file, strategy, num_lines):
    sources = read_lines(source_file, int(num_lines))
    strategy_config = load_strategy(strategy)
    calls = []

    for source in sources:
        system_prompt = strategy_config['system_prompt'].format(in_lang=in_lang, out_lang=out_lang)
        prompt = strategy_config['prompt_template'].format(in_lang=in_lang, out_lang=out_lang, source=source)
        
        for _ in range(strategy_config['passes']):
            calls.append({
                'llm': llm,
                'model_version': MODELS[llm],
                'prompt': prompt,
                'system_prompt': system_prompt,
                'temperature': strategy_config['temperature']
            })

    print(f"Generating with LLM: {llm}")
    print(f"Input language: {in_lang}")
    print(f"Output language: {out_lang}")
    print(f"Source file: {source_file}")
    print(f"Output file: {out_file}")
    print(f"Strategy: {strategy}")
    print(f"Number of lines: {num_lines}")

    return calls

def process_results(results, args):
    header = textwrap.dedent(f"""
        MODELNAME {args.llm}
        NLINES {args.num_lines}
        STRATEGY_NAME {args.strategy}
        SOURCEFILE {args.source_file}
        SOURCE {args.in_lang}
        TARGET {args.out_lang}
    """).strip()
    
    translations = [result.strip() for result in results]
    output = header + "\n\n" + "\n".join(translations)
    
    with open(args.out_file, 'w', encoding='utf-8') as f:
        f.write(output)

async def main():
    parser = argparse.ArgumentParser(description="Language Translation benchmark")
    parser.add_argument("llm", help="Language model to use")
    parser.add_argument("in_lang", help="Input language")
    parser.add_argument("out_lang", help="Output language")
    parser.add_argument("source_file", help="Source file path")
    parser.add_argument("out_file", help="Output file path")
    parser.add_argument("strategy", help="Strategy to use")
    parser.add_argument("num_lines", help="Number of lines to use from dataset")

    args = parser.parse_args()

    calls = generateCalls(args.llm, args.in_lang, args.out_lang, args.source_file, args.out_file, args.strategy, args.num_lines)
    results = await executeCalls(calls)
    process_results(results, args)
    print(f"Results written to {args.out_file}")

if __name__ == "__main__":
    asyncio.run(main())
