import numpy as np
import matplotlib.pyplot as plt


NaN = np.nan

def randint(bound, **props):  #size #high #dtype
    return np.random.randint(bound, **props)

def random(row, col):
    return np.random.randn(row*col).reshape(row, col)

# def random(num):
#     return np.random.randn(num)


#联合分布
def joint(xs, ys, **props):
    sns.jointplot(x=xs, y=ys, **props)
    return plt

#盒形图
def box(**props):
    sns.boxplot(**props)
    return plt



