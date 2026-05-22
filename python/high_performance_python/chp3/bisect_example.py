import bisect
import random


def find_closest(haystack, needle):
    idx = bisect.bisect_left(haystack, needle)
    if idx == len(haystack):
        return idx - 1
    elif haystack[idx] == needle:
        return idx
    elif idx > 0:
        j = idx - 1
        if haystack[idx] - needle > needle - haystack[j]:
            return j
    return idx


if __name__ == "__main__":
    important_numbers = []
    for i in range(10):
        new_number = random.randint(0, 1000)
        bisect.insort(important_numbers, new_number)

    print(important_numbers)

    closest_index = find_closest(important_numbers, -250)
    print(f"Closest value to -250: {important_numbers[closest_index]}")

    closest_index = find_closest(important_numbers, 500)
    print(f"Closest value to 500: {important_numbers[closest_index]}")

    closest_index = find_closest(important_numbers, 1100)
    print(f"Closest value to 1100: {important_numbers[closest_index]}")
