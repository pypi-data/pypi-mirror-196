import pandas as pd 
from pandas.core.frame import DataFrame
from pandas.core.indexing import _LocIndexer
import pandas.core.common as com 
from zexcel.table.element import Element


class LocIndexer(_LocIndexer):
    """继承_LocIndexer，重写__getitem__, table类型转化"""
    def __init__(self, obj, name):
        self.obj = obj
        self.ndim = obj.ndim
        self.name = name

    def __getitem__(self, key):
        if type(key) is tuple:
            key = tuple(com._apply_if_callable(x, self.obj)
                        for x in key)
            try:
                if self._is_scalar_access(key):
                    return table(self._getitem_scalar(key))
            except (KeyError, IndexError):
                pass
            return table(self._getitem_tuple(key))
        else:
            # we by definition only have the 0th axis
            axis = self.axis or 0

            maybe_callable = com._apply_if_callable(key, self.obj)
            return table(self._getitem_axis(maybe_callable, axis=axis))


class Table(DataFrame, Element):
    def __init__(self, data, **kwargs):
        if(isinstance(data, DataFrame)):
            df = data
        else:
            try:
                if(data.find('xls') >= 0):
                    df = pd.read_excel(data, **kwargs)
                elif(data.find('csv') >= 0):
                    try:
                        df = pd.read_csv(data, **kwargs)
                    except:
                        try:
                            df = pd.read_csv(data, encoding='ISO-8859-1',**kwargs)
                        except:
                            df = pd.read_csv(open(data), **kwargs)
                elif(data.find('txt') >= 0):
                    df = pd.read_table(data, **kwargs)
                elif(data.find('pkl') >= 0):
                    df = pd.read_pickle(data, **kwargs)
            except Exception as e:
                df = DataFrame(data, **kwargs)
        print('haha')
        self._data = df._data # DataFrame BlockManager
        self._item_cache = df._item_cache
        df = self.from_dataframe(df)
        DataFrame().__init__(df['values'], index = df['index'], columns = df['columns']) 

    def from_dataframe(self, dataframe):
        return {'values': dataframe.values,'index': dataframe.index,'columns': dataframe.columns}

    def __getitem__(self, key):
        tmp = DataFrame(self)[key]
        try:
            tmp.columns
        except:
            return Column(DataFrame(self)[key])
        else:
            return table(DataFrame(self)[key])

    @property
    def get(self):
        """
        table(job).get[:,['title']]
        """
        _LocIndexer = DataFrame(self).loc
        return LocIndexer(_LocIndexer.obj, _LocIndexer.name)

    def save(self, filename, **kwargs):
        """
        """
        if(filename.find('xls') >= 0):
            self.to_excel(filename, **kwargs) #header=false
        elif(filename.find('csv') >= 0):
            self.to_csv(filename, **kwargs)
        elif(filename.find('pkl') >= 0):
            self.to_pickle(filename, **kwargs)

    def view(self, **kwargs):
        """在Excel中预览 
        table({'a':[1,2,3]}).view()
        """
        try:
            filename = '%s.xlsx' % t.timestamp()
            self.to_excel('%s.xlsx' % t.timestamp(), **kwargs) #header=false
            wd.open_file(filename)
        except Exception as e:
            print(e)
            print('excel files only')


    def extract(self, new, col, sep, index):
        """
        列拆分
        """
        print(self[col].str.split(sep))
        self[new] = self[col].str.split(sep, expand = True)[index]
        return self

    def transform(self, col, func):
        self[col] = self[col].transform(func)
        return self

    def decompose(self, col, sep, **kwargs):
        rst = self[col].str.split(sep,expand=True)
        for name,index in kwargs.items():
            self[name] =  rst[index]
        return self

    def transfer(self, col, func, new):
        """ 
        生成列
        table(job).transfer('gx','title',lambda x:x+'@')
        """
        self[new] = self[col].transform(func)
        return self
        
    def fill(self, value):
        return table(self.fillna(value))

    def range_columns(self):
        """ 将列名化为range """
        df = DataFrame(self)
        df = df.rename(columns={x:y for x,y in zip(df.columns,range(0,len(df.columns)))})
        return table(df)

    @property
    def dtypes(self):
        print(DataFrame(self).dtypes)
        return DataFrame(self).dtypes # 保留返回值，供pandas内部函数调用

    ############## query ####################
    @property
    def info(self):
        """
        tb.info()
        """
        return DataFrame(self).info()

    def head(self, n = 5, **kwargs):
        """
        tb.head()"""
        return table(DataFrame(self).head(n, **kwargs))

    def tail(self, n = 5, **kwargs):
        """
        tb.tail()
        """
        return table(DataFrame(self).tail(n, **kwargs))

    def filter2(self, cond):
        return table(self.loc[cond])

    def group(self, Column, **kwargs):
        from pandas.core.groupby import DataFrameGroupBy

        def _wrap_agged_blocks(self, items, blocks):
            from pandas.core.internals import BlockManager
            if not self.as_index:
                index = np.arange(blocks[0].values.shape[1])
                mgr = BlockManager(blocks, [items, index])
                result = DataFrame(mgr)

                self._insert_inaxis_grouper_inplace(result)
                result = result._consolidate()
            else:
                index = self.grouper.result_index
                mgr = BlockManager(blocks, [items, index])
                result = DataFrame(mgr)

            if self.axis == 1:
                result = result.T

            returned = self._reindex_output(result)._convert(datetime=True)
            return table(returned)
        DataFrameGroupBy._wrap_agged_blocks = _wrap_agged_blocks
        return self.groupby(Column, **kwargs)
        
    def sort(self, col, order):  
        """
        按列排序
        table(gdp).sort('2018年','asc')
        """
        return table(self.sort_values(by = col, ascending = True if order=='asc' else False))

    def countif(self, Column, value):
        """
        条件计数
        table(job).countif('title','数据分析师') 
        """
        try:
            if value:
                return self[Column].value_counts()[value]
            else:
                return self[Column].fillna(' ').value_counts()[' ']
        except:
            return 0
      
    def count_rank(self, col, order = 'desc'):
        return table(self.groupby(col).size().
            sort_values(ascending = False if order == 'desc' else True))

    def pivot(self, **kwargs):
        """
        数据透视表
        """
        return table(pd.pivot_table(self, **kwargs))

    ############## process ####################
    def nan_clear(self, **kwargs):
        return table(self.dropna(**kwargs))
  
    def unique(self, array=''):
        """行去重
        table({'a':[1,2,3,2]}).unique()
        """
        if array =='':
            return table(self.drop_duplicates())
        else:
            return table(self.drop_duplicates(array))

    def replace(self, a, b, **kwargs):
        return table(DataFrame(self).replace(a, b, **kwargs))

    def join(self, table, on, **kwargs): 
        """
        a = table({'a':[1,2,3,2],'b':[1,2,3,4]})
        b = table({'b':[1,2,3],'c':[11,22,33]})
        a.join(b,'b')
        """
        return table(pd.merge(self, table, on = on, **kwargs))

    def concat(self, table, **kwargs): #axis 1 列连接
        self = table(pd.concat([self, table], **kwargs))

    def append(self, table, **kwargs): #on
        return table(DataFrame(self).append(table, **kwargs))
    ############## define ####################
    def set_index(self, col, **kwargs):
        return table(DataFrame(self).set_index(col, **kwargs))

    def reset_index(self, **kwargs):
        return table(DataFrame(self).reset_index(**kwargs))

    def reindex(self, **kwargs):
        return table(DataFrame(self).reindex(**kwargs))

    def dtype(self, type, cols = 'all'):
        """
        数据类型转化 
        """
        for col in(self.columns if cols=='all' else cols):
            if(type=='datetime'):
                rst = pd.to_datetime(self[col])
            else:
                rst = self[col].astype(type)
            self[col] = rst
        return self

    @property
    def T(self):
        """
        转置
        table({'a':[1,2,3,2]}).T
        """
        return table(DataFrame(self).T)

    def rename_col(self, col, **kwargs): 
        """
        列改名
        table({'a':[1,2,3,2]}).rename_cols({'a':'aa'}))

        Args:
            cols: eg: {'title':'title2'}
        """
        return table(DataFrame(self).rename(columns = col, **kwargs))

    def unique_count(self,**kwargs):
        return self.nunique(**kwargs)

    ############## draw ####################
    def line(self, **kwargs):
        """
        折线图
        table(gdp).set_index('地区').T['广东省'].line()
        """
        return self.plot(**kwargs)   

    def hist(self, **kwargs):
        """ 
        频率分布直方图,对不同区间的数值进行计数
        table(job).salary_avg.hist() 
        """
        return DataFrame(self).hist(**kwargs)   

    def dot(self, **kwargs):
        """ 
        散点图 
        table({'a':[1,2,4],'b':[5,1,5]}).dot(x='a',y='b')
        """
        return self.plot.scatter(**kwargs)

    def bar(self, **kwargs):
        """条形图
        table(job).count_rank('company_industry').bar()
        """
        return self.plot.bar(**kwargs)  

    def barh(self, **kwargs):
        """横向条形图 
        table(job).count_rank('company_industry').barh()
        """
        return DataFrame(self).plot.barh(**kwargs)  

    def area(self, **kwargs):
        """面积图，适用于积累量
        """
        return self.plot.area(**kwargs)  

    def kde(self,  **kwargs):
        """ 
        核密度曲线图 
        """
        return self.plot(kind = 'kde', **kwargs)   

    def pie(self, y, **kwargs): 
        # fix
        """ 
        扇形图,适用于总体比例比较情形 
        """
        return self.plot.pie(y = y, **kwargs)
        
    def box(self, cols):
        """箱型图
        """
        return self.boxplot(Column = cols)   

    
    def funnel(self):
        """ 
        漏斗图 
        """
        return ea.funnel(self)

    def pie2(self):
        return ea.pie(self)

    def describe(self):
        return table(DataFrame(self).describe())




