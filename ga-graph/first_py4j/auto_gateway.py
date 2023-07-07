import time, subprocess
from py4j.java_gateway import JavaGateway

# クラスパスを指定してシェルコマンドを実行
args = ["java","-cp",'test/share/py4j/py4j0.10.9.5.jar:','AdditionApplication']
p = subprocess.Popen(args)

# サーバー起動前に処理が下へ行くのを防ぐ
time.sleep(3) 

gateway = JavaGateway(start_callback_server=True)
random = gateway.jvm.java.util.Random()

# num1, num2を用意
num1, num2 = 4, 5
print(num1, num2) 

# gatewayで関数を呼び出す
addition_app = gateway.entry_point
print(addition_app.addition(num1, num2)) 

# プロセスをkill
gateway.shutdown()
