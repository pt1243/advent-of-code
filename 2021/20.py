with open("./2021/resources/20.txt") as f:
    text = f.read().strip()


def enhance_image(image_enhancement_algorithm: str, lines: list[str], steps: int) -> int:
    if image_enhancement_algorithm[0] != "#":
        raise ValueError("current implementation only works when index 0 is #")

    on_pixels: set[tuple[int, int]] = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                on_pixels.add((row, col))

    for _ in range(steps // 2):
        # step 1: only keep track of pixels that will be off afterwards; everything else is on
        off_pixels: set[tuple[int, int]] = set()
        min_row = min(pixel[0] for pixel in on_pixels) - 1
        max_row = max(pixel[0] for pixel in on_pixels) + 1
        min_col = min(pixel[1] for pixel in on_pixels) - 1
        max_col = max(pixel[1] for pixel in on_pixels) + 1
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                index_string = "".join(
                    "1" if (row + drow, col + dcol) in on_pixels else "0"
                    for drow in range(-1, 2)
                    for dcol in range(-1, 2)
                )
                if image_enhancement_algorithm[int(index_string, 2)] == ".":
                    off_pixels.add((row, col))

        # step 2: only keep track of pixels that will be on afterwards; everything else is off
        on_pixels = set()
        min_row = min(pixel[0] for pixel in off_pixels) - 1
        max_row = max(pixel[0] for pixel in off_pixels) + 1
        min_col = min(pixel[1] for pixel in off_pixels) - 1
        max_col = max(pixel[1] for pixel in off_pixels) + 1
        for row in range(min_row, max_row + 1):
            for col in range(min_col, max_col + 1):
                index_string = "".join(
                    "0" if (row + drow, col + dcol) in off_pixels else "1"
                    for drow in range(-1, 2)
                    for dcol in range(-1, 2)
                )
                if image_enhancement_algorithm[int(index_string, 2)] == "#":
                    on_pixels.add((row, col))

    return len(on_pixels)


def problem_1() -> None:
    image_enhancement_algorithm, image_lines = text.split("\n\n")
    print(enhance_image(image_enhancement_algorithm, image_lines.splitlines(), 2))


def problem_2() -> None:
    image_enhancement_algorithm, image_lines = text.split("\n\n")
    print(enhance_image(image_enhancement_algorithm, image_lines.splitlines(), 50))
