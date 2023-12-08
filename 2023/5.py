with open('./2023/resources/5.txt') as f:
    lines = f.read().strip()


lines_old = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4\
"""


def get_transformed_value(target: dict[int, tuple[int, int]], value: int) -> int:
    for source_range_start, (dest_range_start, range_length) in target.items():
        if source_range_start <= value < source_range_start + range_length:
            return (value - source_range_start) + dest_range_start
    return value


def problem_1() -> None:
    seed_to_soil: dict[int, tuple[int, int]] = {}
    soil_to_fertilizer: dict[int, tuple[int, int]] = {}
    fertilizer_to_water: dict[int, tuple[int, int]] = {}
    water_to_light: dict[int, tuple[int, int]] = {}
    light_to_temperature: dict[int, tuple[int, int]] = {}
    temperature_to_humidity: dict[int, tuple[int, int]] = {}
    humidity_to_location: dict[int, tuple[int, int]] = {}

    targets = {
        "seed-to-soil": seed_to_soil,
        "soil-to-fertilizer": soil_to_fertilizer,
        "fertilizer-to-water": fertilizer_to_water,
        "water-to-light": water_to_light,
        "light-to-temperature": light_to_temperature,
        "temperature-to-humidity": temperature_to_humidity,
        "humidity-to-location": humidity_to_location,
    }

    for line_group in lines.split("\n\n"):
        if line_group.startswith("seeds"):
            seeds = {int(n): 0 for n in line_group.split(": ")[1].split()}
        else:
            split_lines = line_group.split("\n")
            target = targets[split_lines[0].split()[0]]
            for line in split_lines[1:]:
                dest_range_start, source_range_start, range_length = (int(c) for c in line.split())
                target[source_range_start] = (dest_range_start, range_length)
                # target.update({source_range_start + i: dest_range_start + i for i in range(range_length)})
                # # for i in range(range_length):
                #     target[source_range_start + i] = dest_range_start + i

    for seed in list(seeds.keys()):
        soil = get_transformed_value(seed_to_soil, seed)
        fertilizer = get_transformed_value(soil_to_fertilizer, soil)
        water = get_transformed_value(fertilizer_to_water, fertilizer)
        light = get_transformed_value(water_to_light, water)
        temperature = get_transformed_value(light_to_temperature, light)
        humidity = get_transformed_value(temperature_to_humidity, temperature)
        location = get_transformed_value(humidity_to_location, humidity)
        # soil = seed_to_soil.get(seed, seed)
        # fertilizer = soil_to_fertilizer.get(soil, soil)
        # water = fertilizer_to_water.get(fertilizer, fertilizer)
        # light = water_to_light.get(water, water)
        # temperature = light_to_temperature.get(light, light)
        # humidity = temperature_to_humidity.get(temperature, temperature)
        # location = humidity_to_location.get(humidity, humidity)
        print(
            f"{seed = }, {soil = }, {fertilizer = }, {water = }, {light = }, {temperature = }, {humidity = }, {location = }"
        )
        seeds[seed] = location

    print(min(seeds.values()))


def problem_2() -> None:
    ...
