import numpy as np
import pandas as pd

def get_matrix(orders,SKU): #orders 二维list ,SKU 一维list
    order_del = []#需删除订单集合
    print("get_matrix_begin")
    for i  in range(len(orders)):
        order = orders[i] #取当前处理的订单，order数据类型为list
    
        flag  = 0 #输出标识符，表订单中需处理订单的数量
        cur_del = [] #当前订单中的无效部分集合
        
        for j in range(len(order)):
            if order[j] in SKU:
                flag += 1  #只要订单出现过两本以上需求书籍，为有效订单
            else :
                cur_del.append(order[j])
                
        if flag < 2: #无效订单，计入需删除集合
            order_del.append(orders[i])
        else: #有效订单，删除订单中的无效部分
            for k in range(len(cur_del)):
                order.remove(cur_del[k])   
            
            orders[i] = order   
            
    for i in range(len(order_del)):#删除无效订单
             orders.remove(order_del[i])
             
    orders = np.array(orders) 
    length = len(SKU) #矩阵规模
#    A_matrix = np.zeros((length,length)) #构造空矩阵                   稠密矩阵
    A_matrix = [None]*length#每个单元格储存第i个sku与其他sku间的关系
    id = {}

    for i in range(length):
        id[SKU[i]] = i
    
    for i in range(len(orders)):
        cur = orders[i]
        for j in range(len(cur)):

            cur_row = id[cur[j]]
            cur_sku = A_matrix[cur_row]
            if np.all(cur_sku) == None:
                #cur_sku = np.empty((0,2),dtype=int) #构造稀疏向量， [ [k,data], ] k表示纵坐标
                cur_sku = []
            for k in range(len(cur)):#j,k为出现在同一订单中的两商品
                if(k != j):
                    col = id[cur[k]]
                    #A_matrix[cur_row][id[cur[k]]] += 1
                    flag = False #标识符，表示k,j关系是否已存在
                    for t in range(len(cur_sku)):  #检验
                         if cur_sku[t][0] == col: #k，j关系已存在
                                cur_sku[t][1] += 1 #data + 1
                                flag = True 
                    if not flag: #k，j关系不存在
                        new_element = [col,1]
                        cur_sku.append(new_element)#添加
            
            A_matrix[cur_row] = cur_sku #更新 
            
                                       
    print("got_matrix")
    
    return orders,A_matrix   #nparray
    

#---------------------------------------------------------------test_code----------------------------------------------------------
# with open('E:\\VScode - file\\python\\book_sorting\\test\\test_SKU.txt', 'r',encoding='utf_8') as f:
#         SKU = f.readlines()
#         SKU = [i.strip() for i in SKU]  #line.strip() 消除字符串前后的空格
   
# orders = pd.read_csv('E:\\VScode - file\\python\\book_sorting\\test\\test_orders.csv',header=None)
# orders = orders.apply(lambda x: x.dropna().tolist(), axis=1) #消除空格
# orders = orders.to_list()

# matrix = get_matrix(orders,SKU)
# print(matrix)
# print(matrix[4] == None)



# output = pd.DataFrame(matrix)
# output.to_csv('sparse_A_matirx.csv')