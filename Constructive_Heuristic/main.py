import numpy as np
import pandas  as pd
from Constructive_Heuristic import C_H
from functions import get_mu
from A_matrix import get_matrix

if __name__ == "__main__":
  
    with open('E:\\VScode - file\\python\\book_sorting\\data\\SKU.txt', 'r',encoding='GBK') as f:
        SKU = f.readlines()
        SKU = [i.strip() for i in SKU]  #line.strip() 消除字符串前后的空格
   
    orders = pd.read_csv('E:\\VScode - file\\python\\book_sorting\\data\\orders.csv',header=None)
    orders = orders.apply(lambda x: x.dropna().tolist(), axis=1) #消除空格
    orders = orders.to_list()
    
    Valuable_orders,A_matrix = get_matrix(orders,SKU)  #get_matrix 要求orders为list
                                      #A_matrix : ndarray,A[i] 为第i个sku与其他商品的相似度向量，[[k,data]] k为sku下标，data为相似度值

    Valuable_orders = np.array(Valuable_orders)             
    L = np.array(get_mu(Valuable_orders,SKU))
    
    capacity = 10
  #  capacity = 2
    distribution_score =  C_H(L, A_matrix, capacity) #dis_score 为三维数组，基本形式为：[ [[group_i],socre_i] ]
   # print(distribution_score)
    
    output = pd.DataFrame(distribution_score)
    output.to_csv('distribution.csv')
     