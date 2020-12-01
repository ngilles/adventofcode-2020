
from pathlib import Path
from contextlib import contextmanager

from dotenv import load_dotenv

load_dotenv()

@contextmanager
def puzzle_input(day: int, root: Path = Path('.puzzle_inputs')):
    if root.exists and not root.is_dir:
        raise Exception('.puzzle_inputs should be a directory!')
    
    if not root.exists:
        root.mkdir()

    input_name = f'day_{day}.txt'
    # input_url = 'https://adventofcode.'
    input_path = root / input_name

    # automatic download? in the future!

    with open(input_path, 'r') as f:
        yield f

    
