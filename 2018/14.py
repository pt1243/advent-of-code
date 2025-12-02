with open("./2018/resources/14.txt") as f:
    number_of_recipes = int(f.read().strip())


def part_1() -> None:
    recipes = [3, 7]
    index_1, index_2 = 0, 1
    while len(recipes) < number_of_recipes + 10:
        total = recipes[index_1] + recipes[index_2]
        if total >= 10:
            recipes.append(1)
        recipes.append(total % 10)
        index_1 += 1 + recipes[index_1]
        index_1 %= len(recipes)
        index_2 += 1 + recipes[index_2]
        index_2 %= len(recipes)
    print("".join(str(x) for x in recipes[number_of_recipes : number_of_recipes + 10]))


def part_2() -> None:
    recipes = [3, 7]
    index_1, index_2 = 0, 1
    target_digits = [int(c) for c in str(number_of_recipes)]
    len_target_digits = len(target_digits)
    while True:
        total = recipes[index_1] + recipes[index_2]
        if total >= 10:
            recipes.append(1)
        recipes.append(total % 10)
        index_1 += 1 + recipes[index_1]
        index_1 %= len(recipes)
        index_2 += 1 + recipes[index_2]
        index_2 %= len(recipes)
        if len(recipes) >= len_target_digits:
            if recipes[-len_target_digits - 1 : -1] == target_digits:
                print(len(recipes) - len_target_digits - 1)
                return
            if recipes[-len_target_digits:] == target_digits:
                print(len(recipes) - len_target_digits)
                return
