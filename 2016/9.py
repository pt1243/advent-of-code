from functools import cache


with open('./2016/resources/9.txt') as f:
    text = f.read().strip()


@cache
def get_decompressed_length_recursive(text: str) -> int:
    if "(" not in text:
        return len(text)

    i = text.find("(")
    rparen_idx = text.find(")", i)
    n_chars, repeat = (int(c) for c in text[i + 1 : rparen_idx].split("x"))
    repeated_chars = text[rparen_idx + 1 : rparen_idx + n_chars + 1]
    return (
        get_decompressed_length_recursive(text[:i])
        + repeat * get_decompressed_length_recursive(repeated_chars)
        + get_decompressed_length_recursive(text[rparen_idx + n_chars + 1 :])
    )


def problem_1() -> None:
    new_length = 0
    i = 0
    while i < len(text):
        if text[i] == "(":
            rparen_idx = text.find(")", i)
            n_chars, repeat = (int(c) for c in text[i + 1 : rparen_idx].split("x"))
            new_length += n_chars * repeat
            i = rparen_idx + n_chars + 1
        else:
            new_length += 1
            i += 1
    print(new_length)


def problem_2() -> None:
    print(get_decompressed_length_recursive(text))
