import csv 


class CSVWriter:
    def __init__(self, file, header=None):
        f = open(file,'w')
        if(header): 
            writer =  csv.DictWriter(f, header, lineterminator='\n')
            writer.writeheader()
        else:
            writer =  csv.writer(f,lineterminator='\n')
        self.instance = writer

    def add(self, row):
        """添加记录
        csv_w('gx.csv').add([1,2,3])
        data = {'title': '大家有听过这种说法吗？还是老人太迷信了？', 'user': '特耐磨付', 'time': '2020-01-09 15:06:29'}
        csv_w('gx3.csv',['title','user','time']).add(data)"""
        self.instance.writerow(row)
       

def CSVReader:
    def __init__(self):
        f = open(file,'r')
        self.instance = csv.reader(f, lineterminator='\n')


