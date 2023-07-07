# グラフ x 遺伝的アルゴリズム

## 環境構築方法

### 定数を管理するファイルを作成

1. 以下の 2 つのプログラムを、指定の場所に作成する

#### 1 つ目: Python ファイル

##### 作成場所

> java_class/ocha/itolab/koala/batch/py4j/constants.py

##### テンプレート

```python
JAR_PATH = "path"

CLASS_PATH = "path"

PNG_PATH =
```

##### テンプレートを編集

以下の 3 つの絶対パス

- ga_graph/test/share/py4j/py4j0.10.9.5.jar
- ga_graph/java_class
- ga_graph/Koala-manygen/plot_result/

#### 2 つ目: Java ファイル

##### 作成場所

> Koala-manygen/src/ocha/itolab/koala/batch/py4j/Constants.java

##### テンプレート

```java
package ocha.itolab.koala.batch.py4j;

public final class Constants {
    private Constants() {
    }
    public static class Path {
        public static final String RESULT = "path";
        public static final String DATA_CSV = "path";
    }
}
```

##### テンプレートを編集

以下の 2 つの絶対パス

- ga_graph/Koala-manygen/result
- ga_graph/Koala-manygen/NBAF_Coauthorship_12dim.csv

### Java の準備 (基本的に Mac かつ Eclipse 入れてない場合)

1. `Koala-manygen`フォルダへ移動. `ga-graph`フォルダにいる場合は、以下のコマンドで OK
   > cd Koala-manygen
1. 以下のコマンドで、Java ファイルをことごとくコンパイル。(**ただし、Windows の場合は、コロンではなく、セミコロンに変えること**)。また、Eclipse でまとめてコンパイルできるなら、省略できるプロセスかも...?
   > javac -cp ../test/share/py4j/py4j0.10.9.5.jar:../java_class/ -d ../java_class/ src/ocha/itolab/koala/batch/py4j/\*.java
1. Java の設定は OK なはずなので、次は Python の準備へ

### Python の準備

1. Python をインストール
1. 仮想環境を構築。環境名は**test**とする[詳細な方法はこちら](https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e) 。
1. 仮想環境を起動。`ga-graph`のフォルダにて、以下のコマンドを実行
   > source test/bin/activate
1. 必要な python ライブラリをインストール。`requirements.txt`に全て記載したので、`ga-graph`のフォルダにて以下のコマンドを実行すれば大丈夫なはず

   > pip install -r requirements.txt

1. main.py がある階層へ移動. `ga-graph`のフォルダからであれば、以下のコマンドで OK
   > java_class/ocha/itolab/koala/batch/py4j
1. 以下のコマンドで、メインプログラムを実行。最適化スタート
   > python3 main.py

たぶんこれで実験できるはず...

---

## Java 側の py4j の起動方法

javac でコンパイル

> javac -cp test/share/py4j/py4j0.10.9.5.jar AdditionApplication.java

実行

> java -cp test/share/py4j/py4j0.10.9.5.jar: AdditionApplication

-cp で classpath を指定している。linux の場合、実行の際には jar ファイル名の後に、**:コロン** が必要。Windoows の場合は、セミコロン。

# Java プログラム

## うまくいったコンパイル方法

> ga_graph/Koala-manygen
> にて、下記コマンドを実行

> javac -cp ../test/share/py4j/py4j0.10.9.5.jar:../java_class/ -d ../java_class/ src/ocha/itolab/koala/batch/py4j/\*.java

### Windows 版コマンド

javac -cp ..\test\share\py4j\py4j0.10.9.5.jar;..\java_class\ -d ..\java_class\ -d ..\java_class\ src\ocha\itolab\koala\core\data\*.java

- -d オプションが、class ファイルの格納場所を指定
- cp py4j の jar ファイルと他の class ファイルが入ったディレクトリを指定

## Java プログラムが実行できないとき

- ソースコード内で package を import 使用している時は、実行コマンドにもパッケージ名を追加. [参考](https://teratail.com/questions/53923)

## constants ファイル

## openGL のために必要なファイル

[こちら](https://jogamp.org/deployment/v2.3.2/jar/)か 4 つダウンロード

- gluegen-rt-natives-xxxx.jar
- gluegen-rt.jar
- jogl-all-natives-xxxx.jar
- jogl-all.jar

※ なお xxxx には「macosx-universal」「windows-i586」など自分の使っている OS に対応する単語が入る

## OpenGL のコンパイル

### 注意

Windows のパス名は \ ではなく、\\\ を使う

### 環境構築

- 必要な jar ファイルをダウンロード
- itolab scrapbox に従って Eclipse 環境を整える。
- 以下のサイトから必要な jar ファイルをダウンロードし、Eclipse の環境に加える
  - http://www.java2s.com/Code/Jar/g/Downloadgluegenrtnativeswindowsamd64jar.htm
  - http://www.java2s.com/Code/Jar/g/Downloadgluegenrtnativeswindowsamd64jar.htm
  - https://jar-download.com/artifacts/org.jogamp.jogl/jogl-all/2.3.2/source-code

### 実行方法

1. Eclipse 上でコンパイルし、ObjectFunction プログラムを実行(Java を起動)。Server Gateway Started! が表示されることを確認

1. class ファイルがあるディレクトリで、以下のコマンドを実行(Python を起動)

   > python main.py

   を実行。

# 参考資料

- Java と Python の橋渡し[URL](https://qiita.com/riverwell/items/e90cbbfdac439e6e9d30)
- [DEAP ライブラリ](https://dse-souken.com/2021/05/25/ai-19/)
