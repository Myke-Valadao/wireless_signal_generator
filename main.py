import argparse
from src.config import DEFAULTS
from src.generator import generate_data

def main():
    parser = argparse.ArgumentParser(description="Gerador de sinais wireless simulados.")
    for key, value in DEFAULTS.items():
        arg_type = type(value) if not isinstance(value, list) else lambda s: list(map(int, s.split(',')))
        parser.add_argument(f'--{key}', type=arg_type, default=value)

    args = parser.parse_args()
    args_dict = vars(args)

    generate_data(**args_dict)

if __name__ == "__main__":
    main()
