# mergecsv by Takeyuki Watadani
20210901CSVを統合するスクリプト

---

# MergeCSV - CSVを統合するスクリプト

## インストール

GitHubからこのスクリプトをcloneすることでインストールが行われます。

```sh
$ cd (スクリプトをインストールするディレクトリ)
$ git clone https://github.com/twatadani/mergecsv
$ cd mergecsv
```
## Python3が使用可能かの確認

```sh
$ python --version

Python 3.8.8
```

Python 3.x系ならば大抵動作するはず。

---

## How to Use

### 1. config.jsonをエディットする

mergecsvディレクトリ内にconfig.jsonという設定用ファイルがあるのでCSVファイルの置き場所などの設定事項をconfig.json内のコメントに従って記載する。

### 2. スクリプトを実行する

コマンドラインから

```sh
$ python ./mergecsv.py
```

を実行するとCSVの統合処理が行われる。

---

## 本スクリプトで統合するCSVのファイル形式についての仕様

#### pt1/acapulco/data.csv  

| LOCATION | MEASUREMENT |  
| -------- | ----------- |  
| thalamus | 0.2357      |  
| caudate  | 0.1234      |
...  

#### pt2/acapulco/data.csv  

| LOCATION | MEASUREMENT |  
| -------- | ----------- |  
| thalamus | 0.2376      |  
| caudate  | 0.1333      |
...

のようなCSVファイルが複数あったとき、統合結果として

#### merged.csv

| LOCATION | pt1 | pt2 |  
| -------- | --- | --- | 
| thalamus | 0.2357 | 0.2376 |
| caudate  | 0.1234 | 0.1333 |
...

のように統合を行う。  
