import subprocess
import time

import constants
from mydeap import GA
from nsga2 import NSGA2
from nsga3 import NSGA3
from py4j.java_gateway import JavaGateway
import random as rnd

# node数 x 2　が遺伝子の長さ
## ObjectFunction.java の _arr配列の長さも変える
CHROMOSOME_LENGTH = 460 * 2

# クラスパスを指定してシェルコマンドを実行
args = [
    "java",
    "-Xmx4096M",
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

    # 配置手法アルゴリズムをランダムに選択  1: Koala 3: PH
    # method = rnd.choice([1, 3])
    method = 3
    for n, elem in enumerate(double_array):
        res = koala_to_sprawlter.obfunc(elem, n, CHROMOSOME_LENGTH, method)
        # resは、[sprawl, clutter, sprawlter]のfloat配列

    return (res[0], res[1])


# GAプログラムを呼び出す
# ga = GA(myfunc, CHROMOSOME_LENGTH)
# ga.GA_main_eaMuCommaLambda()

# NSGA-IIを呼び出す
ga = NSGA2(myfunc, CHROMOSOME_LENGTH)
try:
    ga.main()
except Exception as e:
    print(e)

# NSGA-IIIを呼び出す
# ga = NSGA3(myfunc, CHROMOSOME_LENGTH)
# ga.main()

# プロセスをkill
gateway.shutdown()
