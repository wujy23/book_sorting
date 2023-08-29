import numpy as np
import pandas as pd
import random

data2 = pd.read_csv('output.csv')
arr = data2.to_numpy()
arr = arr[:,1:]


def canopy(data, T1, T2):  #T2为外圈 T1为内圈
    
    a = data
    np.fill_diagonal(a, 0)
    MAX = np.max(a)
    
    print(MAX)
    
    canopies = []
    while len(data) > 0:
        # 随机选择一个数据点
        point = random.randint(0,len(data) - 1)
        # 创建一个新的canopy
        new_canopy = [point]

     #   print(new_canopy)
        # 将该数据点从数据集中删除
        temp = data[point,:]
    #    print(temp)
        del_row = [point]
        del_inf = [point]
        
        
        for i in range(len(data)):
            # 计算数据点与新canopy的距离
         #   print(i)
            dist = MAX - temp[i]
            
            if dist <= T2:
                new_canopy.append(i)
            if dist <= T1 :
                if i != point: 
                    del_row.append(i)
                    del_inf.append(i)
      
        canopies.append(new_canopy)
         
        print(del_row)
         
        data = np.delete(data,del_row,axis = 0)
        data = np.delete(data,del_inf,axis = 1)
   
    return canopies
     

k = canopy(arr,220,220)
result = pd.DataFrame(k)
result.to_excel('my_result.xlsx', index=False)
 
print(len(k))





