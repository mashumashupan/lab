import array
import random

import matplotlib.pyplot as plt
import numpy as np
from deap import base, creator, tools
from deap.benchmarks.tools import hypervolume
from history_evaluation_stats import HistoryEvaluationStats
from my_mutation import muSmall

from constants import PNG_PATH

class Config:
    # hyper volumeの計算に使用するreference point
    reference_point: tuple[float, float]
    # 終了条件
    hypervolume_threshold: float
    # カウントする条件
    hv_count_threshold: float

    def __init__(self, rp: tuple[float, float], hv: float, hvc: float):
        self.reference_point = rp
        self.hypervolume_threshold = hv
        self.hv_count_threshold = hvc


class NSGA2:
    def __init__(self, obfunc, write_layout_file_func, gen_len):
        ## 問題固有のパラメタ
        # 遺伝子が取り得る値の範囲を指定
        self.MIN_COORDINATE, self.MAX_COORDINATE = -10.0, 10.0
        # 1つの個体内の遺伝子の数を指定
        self.NDIM = 20
        # 散布図の軸
        self.PLOT_XLIM_MIN, self.PLOT_XLIM_MAX =  38.0, 60.0
        self.PLOT_YLIM_MIN, self.PLOT_YLIM_MAX =  1.2, 2.5

        # 適合度を最小化することで最適化されるような適合度クラスの作成
        creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
        # 個体クラスIndividualを作成
        creator.create(
            "Individual", array.array, typecode="d", fitness=creator.FitnessMin
        )

        ### 各種関数の設定
        # Toolboxの作成
        self.toolbox = base.Toolbox()

        # 遺伝子を生成する関数"attribute"を登録
        self.toolbox.register(
            "attribute", random.uniform, self.MIN_COORDINATE, self.MAX_COORDINATE
        )

        # 個体を生成する関数”individual"を登録
        # gen_len回 toolbox.attributeを実行し、その値をcreator.Individualに格納して返す関数individualを定義 => tools.initRpeatを引数なしで呼び出せるように変化
        self.toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            self.toolbox.attribute,
            gen_len,
        )

        # 個体集団を生成する関数"population"を登録
        self.toolbox.register(
            "population", tools.initRepeat, list, self.toolbox.individual
        )

        ## 目的関数の設定
        self.obfunc = obfunc

        ## layout.csvを出力用の関数を設定
        self.write_layout_file_func = write_layout_file_func

    def setting(self):
        ## 選択
        # 個体選択法"select"を登録
        self.toolbox.register("select", tools.selNSGA2)

        ## 交叉
        # 交叉を行う関数"mate"を登録
        self.toolbox.register(
            "mate",
            tools.cxSimulatedBinaryBounded,
            low=self.MIN_COORDINATE,
            up=self.MAX_COORDINATE,
            eta=20.0,
        )

        ## 突然変異
        # 変異を行う関数"mutate"を登録
        self.toolbox.register(
            "mutate",
            tools.mutPolynomialBounded,
            low=self.MIN_COORDINATE,
            up=self.MAX_COORDINATE,
            eta=40.0,
            indpb=1.0 / self.NDIM,
        )

        # オリジナルのmutation関数に変更
        # self.toolbox.register(
        #     "mutate",
        #     muSmall,
        #     low=self.MIN_COORDINATE,
        #     up=self.MAX_COORDINATE,
        # )
        # 評価関数"evaluate"を登録
        # self.toolbox.register("evaluate", self.obfunc)
        self.historyEvaluationStats = HistoryEvaluationStats(self.obfunc)
        self.toolbox.register("evaluate", self.historyEvaluationStats.evaluate_fitness)

    def main(self, fname="output.txt"):
        self.setting()
        # random.seed(1)

        NGEN = 35  # 繰り返し世代数
        MU = 20  # 集団内の個体数
        CXPB = 0.9  # 交叉率

        koalaConfig = Config((50.0, 2.0), 5.35, 5.5)
        phConfig = Config((55.0, 2.2), 1.3, 1.5)

        # TODO: 実行している配置アルゴリズムによって設定を変える
        def avg(a, b):
            # 8割型a寄りの平均値を算出
            return a * 0.8 + b * 0.2
        rp = (avg(koalaConfig.reference_point[0], phConfig.reference_point[0]), avg(koalaConfig.reference_point[1], phConfig.reference_point[1]))
        hv = avg(koalaConfig.hypervolume_threshold, phConfig.hypervolume_threshold)
        hvc = avg(koalaConfig.hv_count_threshold, phConfig.hv_count_threshold)
        # config = Config(rp, hv, hvc)
        config = phConfig

        # Hyper Volume算出用のreference point
        ref_hv = config.reference_point

        # 世代ループ中のログに何を出力するかの設定
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min, axis=0)
        stats.register("max", np.max, axis=0)

        logbook = tools.Logbook()
        logbook.header = "gen", "evals", "std", "min", "avg", "max"

        # 第一世代の生成
        pop = self.toolbox.population(n=MU)
        self.pop_init = pop[:]
        invalid_ind = [ind for ind in pop if not ind.fitness.valid]

        # TODO 削除
        self.write_layout_file_func(0, pop)

        ## clutterのstatsを算出
        self.historyEvaluationStats.add_individuals(invalid_ind, 0)
        self.historyEvaluationStats.write_csv()

        fitnesses = self.toolbox.map(
            self.toolbox.evaluate,
            invalid_ind,
            [0 for i in range(NGEN)],
            [i for i in range(self.NDIM)],
        )
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop = self.toolbox.select(pop, len(pop))

        # 軸の上限と下限をfitnesses_initから算出
        fitnesses_init = np.array(
            [list(self.pop_init[i].fitness.values) for i in range(len(self.pop_init))]
        )
        # 軸の設定(軸の最小値/最大値は、プロット点の最小値/最大値より少しずらす)
        self.PLOT_XLIM_MIN = (
                min(fitnesses_init[:, 0]) - max(fitnesses_init[:, 0]) / 100.0
        )
        self.PLOT_XLIM_MAX = (
                max(fitnesses_init[:, 0]) + max(fitnesses_init[:, 0]) / 100.0
        )
        self.PLOT_YLIM_MIN = (
                min(fitnesses_init[:, 1]) - max(fitnesses_init[:, 1]) / 10.0
        )
        self.PLOT_YLIM_MAX = (
                max(fitnesses_init[:, 1]) + max(fitnesses_init[:, 1]) / 10.0
        )
        # Hyper Volume算出用のreference point
        self.ref_hv = [max(fitnesses_init[:, 0]), max(fitnesses_init[:, 1])]
        # 初期レイアウトをcsv出力
        self.write_layout_file_func(0, pop)

        record = stats.compile(pop)
        logbook.record(gen=0, evals=len(invalid_ind), **record)
        
        with open(PNG_PATH+fname, "a") as f:        
            f.write(logbook.stream)

        # 最適計算の実行
        for gen in range(1, NGEN):
        
        # 終了条件をhvに変える → while条件へ
        # gen = 1
        # hv = 0.0
        # hv_counter = 0
        # while (hv < config.hypervolume_threshold or hv_counter < 4):
            # 子母集団生成
            offspring = tools.selTournamentDCD(pop, len(pop))
            offspring = [self.toolbox.clone(ind) for ind in offspring]

            # 交叉と突然変異
            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                # 交叉させる個体を選択
                if random.random() <= CXPB:
                    # 交叉
                    self.toolbox.mate(ind1, ind2)

                # 突然変異
                self.toolbox.mutate(ind1)
                self.toolbox.mutate(ind2)

                # 交叉と突然変異させた個体は適応度を削除する
                del ind1.fitness.values, ind2.fitness.values

            # 適応度を削除した個体について適応度の再評価を行う
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]

            ## clutterのstatsを算出
            self.historyEvaluationStats.add_individuals(invalid_ind, gen)
            self.historyEvaluationStats.write_csv()

            # 既存の評価関数
            fitnesses = self.toolbox.map(
                self.toolbox.evaluate,
                invalid_ind,
                [gen for i in range(NGEN)],
                [i for i in range(self.NDIM)],
            )
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # 過去の世代と新しい世代の中から
            # 次世代を選択
            pop = self.toolbox.select(pop + offspring, MU)

            # 統計情報を記録
            record = stats.compile(pop)
            logbook.record(gen=gen, evals=len(invalid_ind), **record)
            
            # hypervolumeを表示
            hv = hypervolume(pop, ref_hv)
            print("**** population hypervolume is %.32f ****" % hv)
            
            with open(PNG_PATH+fname, "a") as f:        
                f.write(logbook.stream)
                f.write("\n")
                f.write("**** population hypervolume is %.32f ****" % hv)
                f.write("\n")
            
            # 散布図を保存
            self.viz(pop, gen)
            
            # 終了条件をhvに変えたことにより変更
            # gen += 1
            # if hv >= config.hypervolume_threshold:
            #     hv_counter += 1

        # 最終世代のハイパーボリュームを出力
        # [11.0, 11.0] は Reference Point (参照点): 目的関数と同じだけ指定
        # ハイパーボリュームの値が大きい = パレートラインが広範囲に広がっている = 良いパレートライン
        print("Final population hypervolume is %f" % hypervolume(pop, ref_hv))

        # 最終的に残った遺伝子を全てファイル出力
        self.write_layout_file_func(gen, pop)

        return pop, self.pop_init, logbook

    ## 初期サンプルと各世代(gen)の可視化
    def viz(self, pop, gen, fname="fitness.txt"):

        fitnesses_init = np.array(
            [list(self.pop_init[i].fitness.values) for i in range(len(self.pop_init))]
        )
        fitnesses = np.array([list(pop[i].fitness.values) for i in range(len(pop))])

        fig = plt.figure()
        plt.plot(fitnesses_init[:, 0], fitnesses_init[:, 1], "b.", label="Initial")
        plt.plot(fitnesses[:, 0], fitnesses[:, 1], "r.", label="Optimized")
        
        plt.xlim(self.PLOT_XLIM_MIN, self.PLOT_XLIM_MAX)
        plt.ylim(self.PLOT_YLIM_MIN, self.PLOT_YLIM_MAX)

        # add label to each plot: init
        for i, (x, y) in enumerate(zip(fitnesses_init[:, 0], fitnesses_init[:, 1])):
            plt.annotate(str(i), (x, y))

        # add label to each plot: the generation
        for i, (x, y) in enumerate(zip(fitnesses[:, 0], fitnesses[:, 1])):
            plt.annotate(str(i), (x, y))
        
        # save fitness coordinates in a txt file
        with open(PNG_PATH+fname, "a") as f:
            if gen == 1:
                f.write("\n" + "initial generation\n")
                np.savetxt(f, fitnesses_init, delimiter=",")
                
            f.write("\n" + str(gen) + "generation\n")
            np.savetxt(f, fitnesses, delimiter=",")

        plt.legend(loc="upper right")
        plt.title("fitnesses")
        plt.xlabel("sprawl")
        plt.ylabel("clutter")
        plt.grid(True)

        fig.savefig(PNG_PATH + "result" + str(gen) + ".png")
