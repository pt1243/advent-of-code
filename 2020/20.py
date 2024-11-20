from collections import defaultdict
import numpy as np
import numpy.typing as npt


with open("./2020/resources/20.txt") as f:
    text = f.read().strip()


def extract_tiles(text: str) -> dict[int, npt.NDArray[np.bool_]]:
    tiles: dict[int, npt.NDArray[np.bool_]] = {}
    for tile_group in text.split("\n\n"):
        lines = tile_group.splitlines()
        tile_id = int(lines[0].split()[1].strip(":"))
        tile = np.array([[char == "#" for char in row] for row in lines[1:]])
        tiles[tile_id] = tile
    return tiles


def get_connections(tiles: dict[int, npt.NDArray[np.bool_]]) -> defaultdict[int, set[int]]:
    connections: defaultdict[int, set[int]] = defaultdict(set)
    for tile_id, tile in tiles.items():
        for other_tile_id, other_tile in tiles.items():
            if tile_id == other_tile_id:
                continue
            tiles_match = False

            top_row = tile[0, :]
            bottom_row = tile[-1, :]
            left_column = tile[:, 0]
            right_column = tile[:, -1]
            other_top_row = other_tile[0, :]
            other_bottom_row = other_tile[-1, :]
            other_left_column = other_tile[:, 0]
            other_right_column = other_tile[:, -1]
            if (
                np.all(top_row == other_top_row)
                or np.all(top_row == other_top_row[::-1])
                or np.all(top_row == other_left_column)
                or np.all(top_row == other_left_column[::-1])
                or np.all(top_row == other_right_column)
                or np.all(top_row == other_right_column[::-1])
                or np.all(top_row == other_bottom_row)
                or np.all(top_row == other_bottom_row[::-1])
            ):
                tiles_match = True
            if (
                np.all(left_column == other_top_row)
                or np.all(left_column == other_top_row[::-1])
                or np.all(left_column == other_left_column)
                or np.all(left_column == other_left_column[::-1])
                or np.all(left_column == other_right_column)
                or np.all(left_column == other_right_column[::-1])
                or np.all(left_column == other_bottom_row)
                or np.all(left_column == other_bottom_row[::-1])
            ):
                tiles_match = True
            if (
                np.all(right_column == other_top_row)
                or np.all(right_column == other_top_row[::-1])
                or np.all(right_column == other_left_column)
                or np.all(right_column == other_left_column[::-1])
                or np.all(right_column == other_right_column)
                or np.all(right_column == other_right_column[::-1])
                or np.all(right_column == other_bottom_row)
                or np.all(right_column == other_bottom_row[::-1])
            ):
                tiles_match = True
            if (
                np.all(bottom_row == other_top_row)
                or np.all(bottom_row == other_top_row[::-1])
                or np.all(bottom_row == other_left_column)
                or np.all(bottom_row == other_left_column[::-1])
                or np.all(bottom_row == other_right_column)
                or np.all(bottom_row == other_right_column[::-1])
                or np.all(bottom_row == other_bottom_row)
                or np.all(bottom_row == other_bottom_row[::-1])
            ):
                tiles_match = True

            if tiles_match:
                connections[tile_id].add(other_tile_id)
    return connections


def problem_1() -> None:
    tiles = extract_tiles(text)
    connections = get_connections(tiles)

    product = 1
    for tile_id, other_tile_connections in connections.items():
        if len(other_tile_connections) == 2:
            product *= tile_id
    print(product)


def problem_2() -> None:
    tiles = extract_tiles(text)
    connections = get_connections(tiles)

    edge_tiles = {tile_id for tile_id, connections_list in connections.items() if len(connections_list) <= 3}
    remmaining_edge_tiles = edge_tiles.copy()
    corner_tiles = {tile_id for tile_id, connections_list in connections.items() if len(connections_list) == 2}

    ordered_edge_tiles = [min(corner_tiles)]
    remmaining_edge_tiles.remove(min(corner_tiles))
    while remmaining_edge_tiles:
        next_tile = min(
            {tile_id for tile_id in remmaining_edge_tiles if ordered_edge_tiles[-1] in connections[tile_id]}
        )
        ordered_edge_tiles.append(next_tile)
        remmaining_edge_tiles.remove(next_tile)

    corner_indices = [i for i, tile_id in enumerate(ordered_edge_tiles) if tile_id in corner_tiles]
    width = corner_indices[1] + 1
    height = corner_indices[2] - corner_indices[1] + 1
    arranged_tile_ids = np.zeros((height, width), int)
    arranged_tile_ids[0, :-1] = ordered_edge_tiles[: corner_indices[1]]
    arranged_tile_ids[:-1, -1] = ordered_edge_tiles[corner_indices[1] : corner_indices[2]]
    arranged_tile_ids[-1, :0:-1] = ordered_edge_tiles[corner_indices[2] : corner_indices[3]]
    arranged_tile_ids[:0:-1, 0] = ordered_edge_tiles[corner_indices[3] :]
    used_tiles = edge_tiles.copy()
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            next_tile = (
                (connections[arranged_tile_ids[i - 1, j]] & connections[arranged_tile_ids[i, j - 1]]) - used_tiles
            ).pop()
            arranged_tile_ids[i, j] = next_tile
            used_tiles.add(next_tile)

    single_tile_height, single_tile_width = tiles[arranged_tile_ids[0, 0]].shape
    single_tile_height -= 2
    single_tile_width -= 2

    oriented_tiles: dict[int, npt.NDArray[np.bool_]] = {}
    first_tile = tiles[arranged_tile_ids[0, 0]]
    second_tile = tiles[arranged_tile_ids[0, 1]]
    third_tile = tiles[arranged_tile_ids[1, 0]]

    found = False
    for i in range(4):
        current_first = np.rot90(first_tile, i)
        for j in range(4):
            current_second = np.rot90(second_tile, j)
            if np.all(current_first[:, -1] == current_second[:, 0]):
                found = True
                break
            current_second = np.flipud(current_second)
            if np.all(current_first[:, -1] == current_second[:, 0]):
                found = True
                break
        if found:
            break
    else:
        raise ValueError("could not orient first and second tiles")

    for i in range(4):
        current_third = np.rot90(third_tile, i)
        if np.all(current_third[0, :] == current_first[-1, :]):
            break
        current_third = np.fliplr(current_third)
        if np.all(current_third[0, :] == current_first[-1, :]):
            break
        flipped_current_first = np.flipud(current_first)
        if np.all(current_third[0, :] == flipped_current_first[-1, :]):
            current_first = flipped_current_first
            current_second = np.flipud(current_second)
            break
        current_third = np.fliplr(current_third)
        if np.all(current_third[0, :] == flipped_current_first[-1, :]):
            current_first = flipped_current_first
            current_second = np.flipud(current_second)
            break
    else:
        raise ValueError("could not orient based on third tile")
    oriented_tiles[arranged_tile_ids[0, 0]] = current_first
    oriented_tiles[arranged_tile_ids[0, 1]] = current_second
    oriented_tiles[arranged_tile_ids[1, 0]] = current_third

    def orient_next_tile(row: int, col: int) -> None:
        tile_id = arranged_tile_ids[row, col]
        if tile_id in oriented_tiles:
            return
        tile = tiles[tile_id]
        if col == 0:
            target_tile = oriented_tiles[arranged_tile_ids[row - 1, col]]
            matching_edge = target_tile[-1, :]
        else:
            target_tile = oriented_tiles[arranged_tile_ids[row, col - 1]]
            matching_edge = target_tile[:, -1]
        for i in range(4):
            current_tile = np.rot90(tile, i)
            if col == 0:
                if np.all(current_tile[0, :] == matching_edge):
                    oriented_tiles[tile_id] = current_tile
                    return
                flipped = np.fliplr(current_tile)
                if np.all(flipped[0, :] == matching_edge):
                    oriented_tiles[tile_id] = flipped
                    return
            else:
                if np.all(current_tile[:, 0] == matching_edge):
                    oriented_tiles[tile_id] = current_tile
                    return
                flipped = np.flipud(current_tile)
                if np.all(flipped[:, 0] == matching_edge):
                    oriented_tiles[tile_id] = flipped
                    return
        raise ValueError(f"could not find orientation for tile {tile_id}")

    for i in range(height):
        for j in range(width):
            orient_next_tile(i, j)

    final_height = single_tile_height * height
    final_width = single_tile_width * width
    final_arranged_tiles = np.zeros((final_height, final_width), bool)
    for i in range(height):
        for j in range(width):
            final_arranged_tiles[
                i * single_tile_height : (i + 1) * single_tile_height,
                j * single_tile_width : (j + 1) * single_tile_width,
            ] = oriented_tiles[arranged_tile_ids[i, j]][1:-1, 1:-1]

    sea_monster_text = [
        "                  # ",
        "#    ##    ##    ###",
        " #  #  #  #  #  #   ",
    ]
    sea_monster_array = np.array([[char == "#" for char in line] for line in sea_monster_text])
    sea_monster_height, sea_monster_width = sea_monster_array.shape
    not_part_of_sea_monster = np.sum(final_arranged_tiles)
    for rot in range(4):
        rotated_tiles = np.rot90(final_arranged_tiles, rot)
        for i in range(final_height - sea_monster_height + 1):
            for j in range(final_height - sea_monster_width + 1):
                if np.all(
                    (sea_monster_array == rotated_tiles[i : i + sea_monster_height, j : j + sea_monster_width])[
                        sea_monster_array
                    ]
                ):
                    not_part_of_sea_monster -= np.sum(sea_monster_array)
        flipped_rotated_tiles = np.flipud(rotated_tiles)
        for i in range(final_height - sea_monster_array.shape[0]):
            for j in range(final_height - sea_monster_array.shape[1]):
                if np.all(
                    (sea_monster_array == flipped_rotated_tiles[i : i + sea_monster_height, j : j + sea_monster_width])[
                        sea_monster_array
                    ]
                ):
                    not_part_of_sea_monster -= np.sum(sea_monster_array)
    print(not_part_of_sea_monster)
