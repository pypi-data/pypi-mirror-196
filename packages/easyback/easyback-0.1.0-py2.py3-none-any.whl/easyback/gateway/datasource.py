import pandas as pd
def read_csv(path:str)->pd.DataFrame:
    '''
        从csv 中读取数据
    '''
    return pd.read_csv(path)

def read_db()->pd.DataFrame:
    '''
        从db 中读取数据
    '''
    pass

def read_api()->pd.DataFrame:
    '''
        从api 中读取数据
    '''
    pass