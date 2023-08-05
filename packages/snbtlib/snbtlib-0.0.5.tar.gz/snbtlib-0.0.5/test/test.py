from snbtlib.formatter import dumps, loads
from pathlib import Path


text = Path('adventure.snbt').read_text(encoding='utf-8')
Path('adventure1.snbt').write_text(dumps(loads(text)), encoding='utf-8')