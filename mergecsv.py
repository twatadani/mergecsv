''' mergecsv.py - MERGECSVのメイン実行スクリプト 

Usage:
1. config.jsonをedit
2. $ python ./mergecsv.py

'''

import json
import csv
import os.path
import os
from glob import iglob

from subjectdata import SubjectData

__author__ = 'Takeyuki Watadani<watadat-tky@umin.ac.jp>'
__date__ = '2021/9/1'
__version__ = '2.0'
__status__ = 'validation'

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
gstr = os.path.join(srcdir, '**/acapulco/data.csv')
gresult = iglob(gstr, recursive=True)

# CSVファイルを読み込む

# 最初に読み込むファイルの先頭行を統合後のタイトルにする
measurements = []

mergedrow = [] # 最終的に書き込むデータ

sniffer = csv.Sniffer()

# 1つずつCSVファイルを読み込み、subjectdataのsetを作成する
dataset = set()

for srccsv in gresult:
    with open(srccsv, mode='r') as csvfp:
        basename = os.path.basename(srccsv)
        

        # CSVの形式を推測する
        dialect = sniffer.sniff(csvfp.read(256))
        csvfp.seek(0)

        subjectid = os.path.basename(srccsv.split('/acapulco/')[0])
        print(subjectid, 'のdata.csvを読み込みます。')

        reader = csv.reader(csvfp, dialect)
        tmp1st = reader.__next__() # タイトル行は読み捨てる
        
        # 1行ずつデータを読み込み、SubjectDataオブジェクトを作成し、datasetに追加する
        datadict = {}
        for row in reader:
            if not row[0] in measurements:
                measurements.append(row[0])
            datadict[row[0]] = row[1]
        dataset.add(SubjectData(subjectid, datadict))

# datasetは順不同になってしまうので出力前にソートを行う
sortedset = sorted(dataset, key=lambda x: x.id)

# 統合後のCSV書き込み
with open(dstcsv, mode='w') as dstfp:
    writer = csv.writer(dstfp, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

    # タイトル行の作成
    titlerow = [ 'LOCATION' ]
    for dat in sortedset:
        titlerow.append(dat.id)

    # タイトル行の書き込み
    writer.writerow(titlerow)

    # データ行の書き込み
    for location in measurements:
        row = [ location ]
        for dat in sortedset:
            row.append(getattr(dat, location))
        writer.writerow(row)

print('CSV統合が完了しました。出力ファイルは', dstcsv, 'です。')
