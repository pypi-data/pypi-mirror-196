import numpy as np
import database
import excel as ec 

def random(num):
    return np.random.randn(num)

def table():
    db = database.MySQL('job')
    return db.get('select * from zhipin_job2')

def gdp():
    return ec.table(r'D:\data analysis\dataset\game\gdp.xls')

def game():
    return ec.table(r'D:\data analysis\dataset\game\Euro_2012_stats_TEAM.csv')

def army():
    raw_data = {'regiment': ['Nighthawks', 'Nighthawks', 'Nighthawks', 'Nighthawks', 'Dragoons', 'Dragoons', 'Dragoons', 'Dragoons', 'Scouts', 'Scouts', 'Scouts', 'Scouts'],
        'company': ['1st', '1st', '2nd', '2nd', '1st', '1st', '2nd', '2nd','1st', '1st', '2nd', '2nd'],
        'deaths': [523, 52, 25, 616, 43, 234, 523, 62, 62, 73, 37, 35],
        'battles': [5, 42, 2, 2, 4, 7, 8, 3, 4, 7, 8, 9],
        'size': [1045, 957, 1099, 1400, 1592, 1006, 987, 849, 973, 1005, 1099, 1523],
        'veterans': [1, 5, 62, 26, 73, 37, 949, 48, 48, 435, 63, 345],
        'readiness': [1, 2, 3, 3, 2, 1, 2, 3, 2, 1, 2, 3],
        'armored': [1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        'deserters': [4, 24, 31, 2, 3, 4, 24, 31, 2, 3, 2, 3],
        'origin': ['Arizona', 'California', 'Texas', 'Florida', 'Maine', 'Iowa', 'Alaska', 'Washington', 'Oregon', 'Wyoming', 'Louisana', 'Georgia']
    }
    return ec.table(raw_data)
    
def sample():
    tb = ec.table({'地区':['广东省','江苏省','山东省','浙江省','河南省'],\
        '2018年':[97277.77,92595.40,76469.67,56197.15,48055.86]})
    tb.set_index('地区', inplace = True)
    return tb
    

  
       
       
       
       

