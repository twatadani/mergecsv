''' subjectdata.py - 1名分のデータを格納するクラスSubjectDataを記載するモジュール '''

__author__ = 'Takeyuki Watadani<watadat-tky@umin.ac.jp>'
__date__ = '2021/9/1'
__version__ = '1.0'
__status__ = 'dev'

class SubjectData:
    ''' 
    1名分のデータを保持するクラス
    '''

    def __init__(self, id: str, data: dict):
        '''  
        SubjectDataのイニシャライザ
        idはこのsubjectを識別するID文字列を与える。
        dataはdict形式で、CSVから読み取ったデータを与える。test用のCSVの場合、
        {
            'thalamus': '0.2357',
            'caudate': '0.1234'
        }
        のような形式で与える。
        '''
        self.__subjectid = id
        self.__data = data

        # obj.thalamusで'0.2357'を取得できるattributeを与える
        for key in data:
            setattr(self, key, self.__data[key])
        return


    @property
    def id(self):
        ''' obj.idでsubjectidを取得できるようにする '''
        return self.__subjectid