"""Conservative Markdown normalization; never rewrite source content in place."""
import argparse
import json
from pathlib import Path


def clean(text):
    # Do not strip per-line whitespace: two trailing spaces can mean a hard break.
    # EOF blank lines may belong to unclosed fences/HTML blocks. Keep them too.
    return text.removeprefix('\ufeff').replace('\r\n', '\n').replace('\r', '\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    try:
        original = a.input.read_bytes()
        text = original.decode('utf-8')
        result = clean(text).encode('utf-8')
        with a.output.open('xb') as f:
            f.write(result)
        print(json.dumps({'changed': original != result, 'before_bytes': len(original), 'after_bytes': len(result), 'source_preserved': True}))
    except (OSError, ValueError) as e:
        p.exit(2, str(e) + '\n')


if __name__ == '__main__':
    main()
