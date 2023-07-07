# csv_viewer

基本的には Python プログラムのみで構成

- Streamlit による可視化システム
- csv ファイルから html への変換プログラム
  - まとめて変換
  - リンク指定で 1 つを変換

## 環境構築

Makefile があるので make コマンドで基本的に完結するはず

### 1. Python の仮想環境を構築。

以下のコマンドを`csv_viewer`フォルダの中で実行

> make venv

`streaml_csv`という名前の仮想環境ができる

### 2. 仮想環境を起動

> source ./streamlit_csv/bin/activate

### 3. 必要な python ライブラリをインストール

> pip install -r requirements.txt

多分ここまでで環境は構築できたはず。

---

## csv ファイルを html へ一括変換

### 1. ファイルの用意

result ディレクトリの中に、2 つのディレクトリを作成

- `csv_files`: GA で出力された csv ファイルを全て格納
- `html_files`: html 変換後のファイルが入るので最初は空

### 2. csv を html に一括変換

parser.py を実行し、csv ファイルを html に書き換える

> make html

**注意)**

`result` ディレクトリの中に、`html_files`という名前のディレクトリがないとエラーになるので注意

### 3. 生成された html ファイルを確認

`html_files`に生成される html ファイルの絶対パスをコピーし、Google ブラウザに貼り付ければ結果が見れるはず

---

## テスト用：csv ファイルを html へ **1 つのみ**変換

仮想環境が起動していることを確認した上で、下記コードを実行

> python graphParser.py csv ファイルの絶対パス

`test.html`と言うファイル名で生成されているはず。

---

## グラフ可視化システムの使用方法

**ファイル番号を直接指定しているので、エラーになる可能性大です。もし、このシステムが必要でデバッグに困った場合は、遠慮なく村上まで連絡ください。**

### 1. 上記の方法で、html ファイルを作成

### 2. streamlit を起動

> make local
