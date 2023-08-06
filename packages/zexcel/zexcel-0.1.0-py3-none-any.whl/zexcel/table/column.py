from pandas.core.series import Series
from zexcel.element import Element


class Column(Series, Element):
    def __init__(self, data, **kwargs):
        if(isinstance(data, Series)):
            s = data
        else:
            s = Series(data, **kwargs)
        s = self.from_series(s)
        super().__init__(s['values'], index = s['index'])

    def from_series(self, series):
        return {'values': series.values,'index': series.index}

    def transform(self, func):
        self = Column(self.map(func))
        return self

    def map(self, func, **kwargs):
        return Column(Series(self).map(func, **kwargs))
        
    def head(self, n = 5, **kwargs):
        return Column(Series(self).head(n, **kwargs))

    def tail(self, n = 5, **kwargs):
        return Column(Series(self).tail(n, **kwargs))

    def sort(self, order = 'desc'):
        """排序
        Column([3,1,2,0]).sort('desc')
        """
        return Column(self.sort_values(ascending = False if order == 'desc' else True))

    def pct_change(self):
        return Column(Series(self).pct_change())

    def avg(self):
        return self.mean()

    def fill(self, value = None, method = None):
        if(value): 
            return Column(self.fillna(value))
        elif(method == 'avg'):
            return Column(Series(self).fillna(self.avg()))

    def corr(self, col):
        """计算两列的相关系数 
        Column([3,1,2,0]).corr(Column([1,2,3,4])))
        """
        return Column(Series(self).corr(col))

    def to_frame(self, **kwargs):
        return table(Series(self).to_frame(**kwargs))

    def save(self, filename, **kwargs):
        if(filename.find('xls') >= 0):
            self.to_excel(filename, **kwargs)
        elif(filename.find('csv') >= 0):
            """ISO-8859-1,utf-8,cp1252
            """
            self.to_csv(filename, **kwargs)
    
    def dtype2(self, type): #fix pandas内部命名干扰
        """类型转换
        Column(['1','2','3']).dtype('int')
        """
        return Column(self.astype(type))

    def line(self, **kwargs):
        return self.plot.line(**kwargs)

    def bar(self, **kwargs):
        return self.plot.bar(**kwargs)   

    def hist(self, **kwargs):
        """频率分布 
        Column([1,2,3]).hist(bins=5)

        Args:
            bins:区间划分个数
        """
        return self.plot.hist(**kwargs)

    def box(self, **kwargs):
        """箱形图 
        Column([3,1,2,0]).box()
        """
        return self.plot.box(**kwargs)
        
    @staticmethod
    def dtindex(date, periods, **kwargs): #dates('1/1/2000', periods=9, freq='T')
        return pd.date_range(date, periods = periods, **kwargs)
