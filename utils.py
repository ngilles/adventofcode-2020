
from pathlib import Path
from contextlib import contextmanager
import io

from dotenv import load_dotenv

load_dotenv()

@contextmanager
def puzzle_input(day: int, example: str = None, force_example=False, root: Path = Path('.puzzle_inputs')):
    if root.exists() and not root.is_dir():
        raise Exception('.puzzle_inputs should be a directory!')
    
    if not root.exists():
        root.mkdir()

    input_name = f'day_{day}.txt'
    # input_url = 'https://adventofcode.'
    input_path = root / input_name

    # automatic download? in the future!
    if input_path.exists() and not force_example:
        with open(input_path, 'r') as f:
            yield f
    elif example:
        yield io.StringIO(example)
    else:
        raise Exception('Data not found, and no example provided')


    
