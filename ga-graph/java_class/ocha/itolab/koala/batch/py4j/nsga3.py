# pytype: skip-file
# 必要なライブラリーのインポート
import random
from math import factorial

import matplotlib.pyplot as plt
import numpy
from deap import algorithms, base, creator, tools

from constants import PNG_PATH

class NSGA3:
    def __init__(self, obfunc, gen_len):
        # 問題設定
        self.NOBJ = 2
        K = 10
        # self.NDIM = self.NOBJ + K - 1
        self.NDIM = 20
        self.P = 12
        H = factorial(self.NOBJ + self.P - 1) / (
            factorial(self.P) * factorial(self.NOBJ - 1)
        )
        self.MIN_COORDINATE, self.MAX_COORDINATE = -10.0, 10.0

        # アルゴリズムのパラメータ
        self.MU = int(H + (4 - H % 4))
        self.NGEN = 10 # 繰り返し世代数
        self.CXPB = 1.0 #交叉率
        self.MUTPB = 1.0 # 突然変異率

        # reference point
        self.ref_points = tools.uniform_reference_points(self.NOBJ, self.P)

        # 適合度を最小化することで最適化されるような適合度クラスの作成
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,) * self.NOBJ)
        # 個体クラスIndividualを作成
        creator.create("Individual", list, fitness=creator.FitnessMin)

        # Toolboxの作成
        toolbox = base.Toolbox()
        # 遺伝子を生成する関数"attribute"を登録
        toolbox.register(
            "attribute", random.uniform, self.MIN_COORDINATE, self.MAX_COORDINATE
        )
        # 個体を生成する関数”individual"を登録
        toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.attribute,
            gen_len,
        )
        # 個体集団を生成する関数"population"を登録
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        self.toolbox = toolbox

        ## 目的関数の設定
        self.obfunc = obfunc

    def setting(self):
        # 評価関数"evaluate"を登録
        self.toolbox.register("evaluate", self.obfunc)

        ## 交叉
        # 交叉を行う関数"mate"を登録
        self.toolbox.register(
            "mate",
            tools.cxSimulatedBinaryBounded,
            low=self.MIN_COORDINATE,
            up=self.MAX_COORDINATE,
            eta=30.0,
        )

        ## 突然変異
        # 変異を行う関数"mutate"を登録
        self.toolbox.register(
            "mutate",
            tools.mutPolynomialBounded,
            low=self.MIN_COORDINATE,
            up=self.MAX_COORDINATE,
            eta=20.0,
            indpb=1.0 / self.NDIM,
        )
        # 個体選択法"select"を登録
        self.toolbox.register("select", tools.selNSGA3, ref_points=self.ref_points)

    def main(self, seed=None):
        self.setting()
        # random.seed(1)

        # 世代ループ中のログに何を出力するかの設定
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean, axis=0)
        stats.register("std", numpy.std, axis=0)
        stats.register("min", numpy.min, axis=0)
        stats.register("max", numpy.max, axis=0)

        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        # 第一世代の生成
        pop = self.toolbox.population(n=self.MU)
        self.pop_init = pop[:]
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]
        fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        record = stats.compile(pop)
        logbook.record(gen=0, evals=len(invalid_ind), **record)
        print(logbook.stream)

        # 最適計算の実行
        for gen in range(1, self.NGEN):
            # 子母集団生成
            offspring = algorithms.varAnd(pop, self.toolbox, self.CXPB, self.MUTPB)

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            # 適合度計算
            fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # 次世代選択
            pop = self.toolbox.select(pop + offspring, self.MU)

            record = stats.compile(pop)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            print(logbook.stream)

            # 散布図を保存
            self.viz(pop, gen)

        return pop, self.pop_init, logbook

    def viz(self, pop, gen):
        fig = plt.figure(figsize=(7, 7))
        ax = fig.add_subplot(111, projection="3d")

        p = numpy.array([ind.fitness.values for ind in pop])
        ax.scatter(p[:, 0], p[:, 1],  p[:, 2],marker="o", s=24, label="Final Population")

        ref_points = tools.uniform_reference_points(self.NOBJ, self.P)

        ax.scatter(
            ref_points[:, 0],
            ref_points[:, 1],
            ref_points[:, 2],
            marker="o",
            s=24,
            label="Reference Points",
        )

        ax.view_init(elev=11, azim=-25)
        ax.autoscale(tight=True)
        plt.legend()
        plt.tight_layout()

        fig.savefig(PNG_PATH + "result" + str(gen) + ".png")


if __name__ == "__main__":
    nsga3 = NSGA3()
    pop, pop_init, stats = nsga3.main()
    pop_fit = numpy.array([ind.fitness.values for ind in pop])
