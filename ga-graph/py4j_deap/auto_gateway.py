import time, subprocess
from py4j.java_gateway import JavaGateway
import mydeap


# クラスパスを指定してシェルコマンドを実行
args = ["java","-cp",'../test/share/py4j/py4j0.10.9.5.jar:','ObjectFunction']
p = subprocess.Popen(args)

# サーバー起動前に処理が下へ行くのを防ぐ
time.sleep(3) 

gateway = JavaGateway(start_callback_server=True)
random = gateway.jvm.java.util.Random()

# gatewayで関数を呼び出す
additional_function = gateway.entry_point


# GAの目的関数を定義
# ここでjavaファイルを呼び出す
def myfunc(individual):
    x = individual[0]
    y = individual[1]

    # [x1, y1, x2, y2, ...] の場合
    # pos_x_list = list(filter(lambda i: i%2==0, individual))
    # pos_y_list = list(filter(lambda i: i%2!=0, individual))

    res = additional_function.obfunc(x, y)
    
    # パターン2
    # res = addition_app.obfunc(pos_x_list, pos_y_list)

    return res, 

# GAプログラムを呼び出す
ga = mydeap.GA(myfunc, 2)
ga.GA_main()


# プロセスをkill
gateway.shutdown()
