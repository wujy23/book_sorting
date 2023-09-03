import numpy as np
import pandas as pd

def get_mu(orders,SKU): #用于更新mu值 orders 为二维数组，为订单集合 SKU为一维数组，为需考虑的SKU
    Mu = np.zeros(len(SKU)) #创建空Mu数组

    id = {}
    for i in range(len(SKU)):
     id[SKU[i]] = i  #书名转换为id，便于后续赋值
    
    for i in range(len(orders)):
        order = orders[i]
        for j in range(len(order)):
            Mu[ id[order[j]] ] += 1  #出现一次对应mu值加一
    
    Mu_i = np.zeros((len(SKU),2))
    for i in range(len(SKU)):
        Mu_i[i][0] = i
        Mu_i[i][1] = Mu[i] #绑定mu_i 与 i，便于后续排序
    
    Mu_i = sorted(Mu_i, key=lambda x: x[1] ,reverse = False)
    
    return Mu_i

# def close_th(matrix ,j ,centriod):
#     centriod = int(centriod)
#     if matrix[j][centriod] == 0:
#         return (matrix.shape[0] - 1)  #与质心相似度为0，输出排序为最后
    
#     rank = 1
#     for t in range(matrix.shape[0]):
#         if matrix[j][t] > matrix[j][centriod]:
#             rank += 1
    
#     return rank  
#当前矩阵不需要
        
def get_closest(matrix , centroid,capacity):
    closest = [] #matrix[centroid] 一定不为空 
    for i in range(len(matrix)): #第 i 近
        for j in range(len(matrix)): # j 为遍历寻优的迭代变量  
            if i >= capacity:
                break    
            if matrix[j] == None:
                continue
            if len(matrix[j])  <= i:
                continue            
            if matrix[j][i][0] == centroid: #matrix的每一项都是排好序的，第i个元素一定第i大
                closest.append(j)
        if  closest: #若集合不为空
            return closest      

def matrix_update(matrix,del_element):
    for i in range(len(matrix)):
        if matrix[i] == None:
            continue
        if i == del_element:
            matrix[i] = None
            continue
#        temp_row = list(matrix[i])
        for j in range(len(matrix[i])):
            if matrix[i][j][0] == del_element:
                if len(matrix[i]) == 1:
                    matrix[i] == None
                else :
                    del matrix[i][j]
                break
    return matrix

def temp_L_update(temp_L,del_element):
    condition = np.any(temp_L != del_element , axis = 1) #axis = 1: 沿着行比较
    new_temp_L = temp_L[condition]   #删去L集合中的cur
    return new_temp_L

def get_value(closest,L):
    closest_value = np.empty((0,2))
    for j in range(len(L)):
        for i in range(len(closest)): 
            if closest[i] == L[j][0]:
                closest_value = np.vstack((closest_value,L[j]))                
    return closest_value

def get_score(group,A_matrix):
    score = 0
    for i in range(len(group)):
        if i == 0:
            continue
        
        cur = int(group[i])
        for j in range(len(A_matrix[cur])):
            if A_matrix[cur][j][0] == group[0]:
                score += A_matrix[cur][j][1]
    
    return score

def exchange(a,i,b,j):
    temp_a = np.array(a)
    temp_b = np.array(b)
    temp_a[i] = b[j]
    temp_b[j] = a[i]
    return temp_a,temp_b

def sorted_matrix(matrix):
    for i in range(len(matrix)):
        if  matrix[i] == None:
            continue
        matrix[i] = sorted(matrix[i],key = lambda x : x[1],reverse=True)
    return matrix


# closest = np.array([3,2,1])
# L = np.array([[2,11],[1,22],[4,33],[3,44]])
# print(get_value(closest,L)) 