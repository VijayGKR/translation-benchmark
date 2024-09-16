import json

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