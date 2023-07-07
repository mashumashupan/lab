import math

import numpy as np


class Color:
    """
    num_colors: 用意する色数を指定(default=300)
    """

    # デフォルトで300色用意
    def __init__(self, num_colors=700):
        self.num_colors = num_colors
        self.color_dict = {}
        self.make_color_dict()

    def make_color_dict(self, start=100, end=16777000):
        """
        input: 用意する色数を指定

        return: {色番号: 「#000000」の色表記} を持つ辞書を返す
        """
        # 100から16777000の間をself.num_colors(メタノード数: 何色の辞書を作るか) で分割
        cols = np.linspace(start, end, self.num_colors).tolist()
        cols = list(map(math.floor, cols))

        for k in range(self.num_colors):
            color = hex(cols[k])
            # color 0xが先頭につくのでカット
            color = color[2:]
            # 6桁になるまで0で埋める
            while len(color) < 6:
                color = "0" + color

            # カラーコードの先頭に#をつける
            color = "#" + color
            self.color_dict[k] = color
