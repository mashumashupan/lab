from py4j.java_gateway import JavaGateway

# JVMへ接続
gateway = JavaGateway() 

# java.util.Randomインスタンスを作成
random = gateway.jvm.java.util.Random()   

# Random.nextIntを呼び出し
number1, number2 = 5, 6
print("input value: ", number1, number2) # (2, 7)

#AdditionApplicationのインスタンスを取得
addition_app = gateway.entry_point        

# additionを呼び出し
sum_num = addition_app.addition(number1, number2)    
print(sum_num) # 11
