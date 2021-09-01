''' mergecsv.py - MERGECSVのメイン実行スクリプト 

Usage:
1. config.jsonをedit
2. $ python ./mergecsv.py

'''

import json
import csv
import os.path
import os
from glob import glob

__author__ = 'Takeyuki Watadani<watadat-tky@umin.ac.jp>'
__date__ = '2021/9/1'
__version__ = '1.0'
__status__ = 'initial'

# config.jsonの読み込み

with open('config.json', mode='r') as cjfp:
    cfdict = json.load(cjfp)

srcdir = os.path.expanduser(os.path.expandvars(cfdict['SRCCSVDIR']))
dstcsv = os.path.expanduser(os.path.expandvars(cfdict['DSTCSV']))

# 格納先のディレクトリが存在しない場合はディレクトリを作成する
dstdir = os.path.dirname(dstcsv)
if not os.path.exists(dstdir):
    print('結果格納先のディレクトリが存在しないので新しく作成します。')
    print('作成されるディレクトリ:', dstdir)
    os.makedirs(dstdir)

# 読み込むCSVファイル群をリストアップする
gstr = os.path.join(srcdir, '**/*.csv')
gresult = glob(gstr, recursive=True)

# globでリストアップされたものは順番が保証されていないので、ソートする
gresult.sort()

# CSVファイルを読み込む

# 最初に読み込むファイルの先頭行を統合後のタイトルにする
pttitle = 'Patient'
titlerow = None
first_title_read = False

mergedrow = [] # 最終的に書き込むデータ

sniffer = csv.Sniffer()

# 1つずつCSVファイルを読み込む
for srccsv in gresult:
    with open(srccsv, mode='r') as csvfp:
        basename = os.path.basename(srccsv)
        print(basename, 'を読み込みます。')

        # CSVの形式を推測する
        dialect = sniffer.sniff(csvfp.read(256))
        csvfp.seek(0)

        ptname = basename.split('.')[0]
        reader = csv.reader(csvfp, dialect)
        tmp1st = reader.__next__()
        if not first_title_read:
            tmp1st.insert(0, pttitle)
            titlerow = tmp1st
            first_title_read = True
        # 1行ずつデータを読み込み、先頭にpt名を付加する
        for row in reader:
            row.insert(0, ptname)
            mergedrow.append(row)

# 統合後のCSV書き込み
with open(dstcsv, mode='w') as dstfp:
    writer = csv.writer(dstfp, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    # タイトル行の書き込み
    writer.writerow(titlerow)
    # データ行の書き込み
    for row in mergedrow:
        writer.writerow(row)

print('CSV統合が完了しました。出力ファイルは', dstcsv, 'です。')
