import sys 
sys.path.append('../src')


from zexcel.table import Table


t = Table('gx.csv')
t.save('haha.xlsx')