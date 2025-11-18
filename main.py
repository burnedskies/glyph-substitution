import string
import argparse

from fontTools.ttLib import TTFont


def rotN(charset: str, n: int = 13) -> list[tuple[str, str]]:
    """
    Returns
    -------
    list[tuple[str, str]]
        A list of 2-tuples (char, partner) where `partner` is the character obtained
        by offseting `char` by `n` positions. The list contains one entry for every 
        character in the charset.
    """
    swaps = []
    for idx, char in enumerate(charset):
        swaps.append((
            char,
            charset[(idx + n) % len(charset)]
        ))

    return swaps

def swap(table, left, right):
    table[left], table[right] = table[right], table[left]

def swap_glyphs(swaps: list[tuple[str, str]], font: TTFont) -> TTFont:
    if "glyf" not in font:
        raise Exception("font does not have a glyf table")
    if "hmtx" not in font:
        raise Exception("font does not have an hmtx table")
    
    for l, r in swaps:
        swap(font["glyf"], l, r)
        swap(font["hmtx"], l, r) # horizontal metrix (spacing)

    return font

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output", default="rot13.ttf")
    parser.add_argument("-r", "--rotations", type=int, default=13)

    args = parser.parse_args()
    with TTFont(args.input) as font:
        swaps = []
        swaps.extend(rotN(string.ascii_lowercase, args.rotations))
        swaps.extend(rotN(string.ascii_uppercase, args.rotations))

        # Since pairs (1, 2) and (2, 1) are equivalent, extract unique
        # pairs to avoid swapping twice (effectively canceling the op)
        unique_swaps = set(tuple(sorted(s)) for s in swaps)

        swapped_font = swap_glyphs(unique_swaps, font)
        swapped_font.save(args.output)