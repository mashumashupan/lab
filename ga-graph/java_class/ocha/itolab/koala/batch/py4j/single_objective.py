import random
import subprocess
import time

import matplotlib.pyplot as plt
import numpy as np
from deap import algorithms, base, creator, tools
from deap.benchmarks.tools import hypervolume

import constants
from mydeap import GA
from py4j.java_gateway import JavaGateway


class SingleObjective_tmp():
    def __init__(self, obfunc, gen_len):
        # super(GA, self).__init__(obfunc, gen_len)
        self.obfunc = obfunc
        
    ### パラメータの設定 - オーバーライド
    def set_params(self):
        # random.seed(64)
        
        self.NGEN = 25  # 繰り返し世代数
        self.MU = 20  # 集団内の個体数
        self.CXPB = 0.9  # 交叉率
        self.MUTPB = 0.1 # 突然変異率
    
    def main(self):
        self.selection()
        self.set_params()

        pop = self.toolbox.population(n=self.POP)

        # 集団内の個体それぞれの適応度（目的関数の値）を計算
        for individual in pop:
            individual.fitness.values = self.toolbox.evaluate(individual)

        # パレート曲線上の個体(つまり、良い結果の個体)をhofという変数に格納
        hof = tools.ParetoFront()
        print("after hof")

        # 今回は最も単純なSimple GAという進化戦略を採用
        algorithms.eaSimple(
            pop,
            self.toolbox,
            cxpb=self.CXPB,
            mutpb=self.MUTPB,
            ngen=self.NGEN,
            halloffame=hof,
        )
        print("eaSimple")

        self.show_result(pop)

    ## 初期サンプルと最終世代の可視化
    def viz(self, pop, gen, fname="fitness.txt"):

        fitnesses_init = np.array(
            [list(self.pop_init[i].fitness.values) for i in range(len(self.pop_init))]
        )
        fitnesses = np.array([list(pop[i].fitness.values) for i in range(len(pop))])

        print(fitnesses_init)
        print("---------")
        print(fitnesses)

        # fig = plt.figure()
        # plt.plot(fitnesses_init[:, 0], fitnesses_init[:, 1], "b.", label="Initial")
        # plt.plot(fitnesses[:, 0], fitnesses[:, 1], "r.", label="Optimized")

        # # add label to each plot: init
        # for i, (x, y) in enumerate(zip(fitnesses_init[:, 0], fitnesses_init[:, 1])):
        #     plt.annotate(str(i), (x, y))

        # # add label to each plot: the generation
        # for i, (x, y) in enumerate(zip(fitnesses[:, 0], fitnesses[:, 1])):
        #     plt.annotate(str(i), (x, y))

        # with open(constants.PNG_PATH + fname, "a") as f:
        #     f.write("\n" + str(gen) + "generation\n")
        #     np.savetxt(f, fitnesses, delimiter=",")

        # plt.legend(loc="upper right")
        # plt.title("fitnesses")
        # plt.xlabel("sprawl")
        # plt.ylabel("clutter")
        # plt.grid(True)

        # fig.savefig(constants.PNG_PATH + "result" + str(gen) + ".png")

class Result:
    def __init__(self, pop_init, pop_last):
        self.pop_init = pop_init
        self.pop_last = pop_last
    
    ## 初期サンプルと各世代(gen)の可視化
    def viz(self, gen=25, fname="fitness.txt"):

        fitnesses_init = np.array(
            [list(self.pop_init[i].fitness.values) for i in range(len(self.pop_init))]
        )
        fitnesses = np.array([list(self.pop_last[i].fitness.values) for i in range(len(self.pop_last))])

        fig = plt.figure()
        plt.plot(fitnesses_init[:, 0], fitnesses_init[:, 1], "b.", label="Initial")
        plt.plot(fitnesses[:, 0], fitnesses[:, 1], "r.", label="Optimized")

        # add label to each plot: init
        for i, (x, y) in enumerate(zip(fitnesses_init[:, 0], fitnesses_init[:, 1])):
            plt.annotate(str(i), (x, y))

        # add label to each plot: the generation
        for i, (x, y) in enumerate(zip(fitnesses[:, 0], fitnesses[:, 1])):
            plt.annotate(str(i), (x, y))
        
        with open(constants.PNG_PATH+fname, "a") as f:
            f.write("\n" + str(gen) + "generation\n")
            np.savetxt(f, fitnesses, delimiter=",")

        plt.legend(loc="upper right")
        plt.title("fitnesses")
        plt.xlabel("sprawl")
        plt.ylabel("clutter")
        plt.grid(True)

        fig.savefig(constants.PNG_PATH + "result" + str(gen) + ".png")

        

class SingleObjective:
    def __init__(self, obfunc, gen_len):
        """
        params:

        obfunc -> 目的関数

        gen_len -> 遺伝子の個数(階層型グラフ メタノード数×2), [x1, y1, x2, y2, ...] という形式で記載
        """
        ## 問題固有のパラメタ
        # 遺伝子の長さ = メタノードの個数 x 2
        self.CHROMOSOME_LENGTH = gen_len
        # 座標の最小値
        self.MIN_COORDINATE = -10.0
        # 座標の最大値
        self.MAX_COORDINATE = 10.0

        # 最小化問題として設定(-1.0で最小化、1.0で最大化問題)
        # 目的が最小化の場合は以下のように設定
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

        # 個体の定義（list型と指定しただけで、中身の遺伝子は後で入れる）
        # 個体を準備
        # Individualクラス→ listクラスを継承し、fitness=cretor.FitnessMinというメンバ変数を追加
        creator.create("Individual", list, fitness=creator.FitnessMin)

        ### 各種関数の設定
        # 交叉、選択、突然変異などには、DEAPのToolbox内にある関数を利用
        toolbox = base.Toolbox()

        # random.uniformの別名をattribute関数として設定。各個体の遺伝子の中身を決める関数(各遺伝子は-50～50のランダムな値)
        toolbox.register(
            "attribute", random.uniform, self.MIN_COORDINATE, self.MAX_COORDINATE
        )

        # individualという関数を設定。それぞれの個体に含まれる2個の遺伝子をattributeにより決めるよ、ということ。
        # gen_len回 toolbox.attributeを実行し、その値をcreator.Individualに格納して返す関数individualを定義 => tools.initRpeatを引数なしで呼び出せるように変化
        toolbox.register(
            "individual",
            tools.initRepeat,
            creator.Individual,
            toolbox.attribute,
            gen_len,
        )

        # 集団の個体数を設定するための関数を準備
        # 個体をtoolbox.individualで作成し、listに格納して返す関数populationを定義
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        self.toolbox = toolbox

        # 目的関数の設定
        self.obfunc = obfunc

    ## 選択
    def selection(self):
        # トーナメント方式で次世代に子を残す親を選択（tornsizeは各トーナメントに参加する個体の数）
        self.toolbox.register("select", tools.selTournament, tournsize=5)

        ## 交叉
        # 交叉関数の設定。ブレンド交叉という手法を採用
        self.toolbox.register("mate", tools.cxBlend, alpha=0.2)

        ## 突然変異
        # mutUniformIntのlowとupを配列で指定
        low_coordinates = [self.MIN_COORDINATE for i in range(self.CHROMOSOME_LENGTH)]
        up_coordinates = [self.MAX_COORDINATE for i in range(self.CHROMOSOME_LENGTH)]

        # 突然変異関数の設定。indpbは各遺伝子が突然変異を起こす確率。muとsigmaは変異の平均と標準偏差
        self.toolbox.register(
            "mutate",
            tools.mutUniformInt,
            low=low_coordinates,
            up=up_coordinates,
            indpb=0.2,
        )

        # 評価したい関数の設定（目的関数のこと）
        self.toolbox.register("evaluate", self.obfunc)

    ### パラメータの設定
    def set_params(self):
        # random.seed(1)
        
        # 何世代まで行うか
        self.NGEN = 3
        # 集団の個体数 ※ javaのNUM_PER_GENERATION
        self.POP = 20
        # 交叉(crossover)確率
        self.CXPB = 0.9
        # 個体が突然変異(mutation)を起こす確率
        self.MUTPB = 0.1
        # 次世代に引き継ぐ個体数 (self.POPと同じ)
        self.MU = 20
        # 1世代の個体数
        self.LAMBDA = 100

    def show_result(self, pop):
        # 最終的な集団(pop)からベストな個体を1体選出する関数
        best_ind = tools.selBest(pop, 1)[0]
        # 結果表示
        print("最も良い個体は %sで、そのときの目的関数の値は %s" % (best_ind, best_ind.fitness.values))

    def GA_main_eaSimple(self):
        self.selection()
        self.set_params()

        pop = self.toolbox.population(n=self.POP)

        # 集団内の個体それぞれの適応度（目的関数の値）を計算
        for individual in pop:
            individual.fitness.values = self.toolbox.evaluate(individual)

        # パレート曲線上の個体(つまり、良い結果の個体)をhofという変数に格納
        hof = tools.ParetoFront()
        print("after hof")

        # 今回は最も単純なSimple GAという進化戦略を採用
        algorithms.eaSimple(
            pop,
            self.toolbox,
            cxpb=self.CXPB,
            mutpb=self.MUTPB,
            ngen=self.NGEN,
            halloffame=hof,
        )
        print("eaSimple")

        self.show_result(pop)

if __name__ == "__main__":
    # node数 x 2　が遺伝子の長さ
    ## ObjectFunction.java の _arr配列の長さも変える
    CHROMOSOME_LENGTH = 460 * 2

    # クラスパスを指定してシェルコマンドを実行
    args = [
        "java",
        "-cp",
        constants.JAR_PATH + ":" + constants.CLASS_PATH,
        "ocha.itolab.koala.batch.py4j.ObjectFunction",
    ]
    p = subprocess.Popen(args)

    # サーバー起動前に処理が下へ行くのを防ぐ
    time.sleep(3)

    gateway = JavaGateway(start_callback_server=True)
    random = gateway.jvm.java.util.Random()

    double_class = gateway.jvm.Double

    # gatewayで関数を呼び出す
    koala_to_sprawlter = gateway.entry_point

    # GAの目的関数を定義
    # ここでjavaファイルを呼び出す
    def myfunc(individual):
        double_array = gateway.new_array(double_class, CHROMOSOME_LENGTH)

        for n, indi in enumerate(individual):
            double_array[n] = float(indi)

        for n, elem in enumerate(double_array):
            res = koala_to_sprawlter.obfunc(elem, n, CHROMOSOME_LENGTH)
            # resは、[sprawl, clutter, sprawlter]のfloat配列

        return (res[2],)

    # 単目的最適化を呼び出す
    # ga = SingleObjective(myfunc, CHROMOSOME_LENGTH)
    # ga.main()

    ga = GA(myfunc, CHROMOSOME_LENGTH)
    ga.GA_main_eaSimple()

    # プロセスをkill
    gateway.shutdown()
