"""
键索引计数法


"""


class LSD:
    def __init__(self):
        raise NotImplementedError

    @staticmethod
    def sort(string_list: list[str], w: int):
        """
        LSD (Least Significant Digit) 基数排序, 适合字符串长度相等的情况

        """
        n = len(string_list)
        r_code_point = 256  # 扩展 ASCII 字符集大小
        aux: list[str | None] = [None] * n

        for d in range(w - 1, -1, -1):
            count = [0] * (r_code_point + 1)
            for i in range(n):
                char_idx = ord(string_list[i][d])
                count[char_idx + 1] += 1

            for r in range(r_code_point):
                count[r + 1] += count[r]

            for i in range(n):
                char_idx: int = ord(string_list[i][d])
                aux[count[char_idx]] = string_list[i]
                count[char_idx] += 1
            string_list[:] = aux


if __name__ == "__main__":
    data = [
        "4PGC938",
        "2IYE230",
        "3CIO720",
        "1ICK750",
        "1OHV845",
        "4JZY524",
        "1ICK750",
        "3CIO720",
        "1OHV845",
        "1OHV845",
        "2RLA730",
        "2RLA730",
        "3ATW723",
    ]

    LSD.sort(data, len(data[0]))

    print("排序后的结果:")
    for item in data:
        print(item)
