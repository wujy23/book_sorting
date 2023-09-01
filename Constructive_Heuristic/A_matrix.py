import numpy as np

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
    A_matrix = np.zeros((length,length)) #构造空矩阵
    id = {}

    for i in range(length):
        id[SKU[i]] = i
    
    for i in range(len(orders)):
        cur = orders[i]
        for j in range(len(cur)):
            cur_row = id[cur[j]]
            for k in range(len(cur)):
                if(k != j):
                    A_matrix[cur_row][id[cur[k]]] += 1
    
    print("got_matrix")
    
    return A_matrix
    

