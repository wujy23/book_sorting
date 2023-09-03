from functions import get_closest,matrix_update,temp_L_update, get_value,get_score,exchange,sorted_matrix
import numpy as np

def C_H(L, A_matrix, capacity): 
    #L = np.array(sorted(L, key=lambda x: x[1] ,reverse = False))  #测试用，可忽略
    #for i in range(len(SKU)):  #第i个点为质心搜索起始点
#    L_repre = []  # 质心集合
   
    distribution_plan = []
    A_matrix = sorted_matrix(A_matrix)    
    matrix = list(A_matrix)
    while np.size(L,axis = 0) > 0:   #阶段1，获取初始解，L非空时，即分配未结束，持续循环   
        
        print("剩余SKU数量",np.size(L,axis = 0))
        
        temp_centriod = L[-1] #temp = [i,mu_i]，即为质心
#        L_repre.append(temp_centriod[0]) #temp[0] 为质心坐标
       
        if(A_matrix[int(temp_centriod[0])] == None): #后续点相似度值均为0，全部归入一组
            last_group = np.empty(len(L))
            for i in range(len(L)):
                last_group[i] = L[i][0]
            break  
            

        group,matrix,L = get_group(L,matrix,capacity,temp_centriod) #获取group，并更新matrix,L(删去已分配的商品)
        distribution_plan.append(group)
    
    
    distribution_plan = np.array(distribution_plan) #获取初始分配方案的各组得分，dis_score[i] = [group_i,score_i]
    distribution_score = np.empty((0,2))
    
    
    for i in range(len(distribution_plan)):
        score = np.array([distribution_plan[i] , get_score(distribution_plan[i],A_matrix)])
        distribution_score = np.vstack((distribution_score,score))
    
    distribution_score = sorted(distribution_score, key=lambda x: x[1] ,reverse = True)#排序,降序，使得后续交换时，优先优化初始得分高的货架
    distribution_score = optimize(distribution_score,A_matrix)
    last_group_score = np.array([last_group,0])
    distribution_score = np.vstack((distribution_score,last_group_score))
    return distribution_score
             
def get_group(L,matrix,capacity,centriod):          
        
        temp_L = np.array(L)
        group = np.array([centriod[0]]) 
        
        while True: #循环读取距离中心点最近的数组，直至货架满    
            
            closest = get_closest(matrix,centriod[0],capacity) #与当前质心相似度排名最高的点的集合
        
            if closest == None:    #没有相近点，货架更新停止
                matrix = matrix_update(matrix,centriod[0]) #更新相似度矩阵，删去cur对应的行和列
                temp_L = temp_L_update(temp_L,centriod) #更新temp_L，删去cur对应行  
                return group,matrix,temp_L

            
            closest_value = get_value(closest,L) #相应相似度矩阵,closest_value已排序，c_v[-1]最大
             
            while len(group) < capacity and np.size(closest_value,axis=0) != 0:  #当货架未满且最相近集合非空时
                cur = closest_value[-1]#取最相近同族货物
                group = np.hstack((group,cur[0]))    #归入同一货架
                closest_value = closest_value[:-1] #删去上述货物
               
                matrix = matrix_update(matrix,cur[0]) #更新相似度矩阵，删去cur对应的行和列
                temp_L = temp_L_update(temp_L,cur) #更新temp_L，删去cur对应行           

            if len(group) != capacity: #货架不满，继续补货
                continue
            else:
                matrix = matrix_update(matrix,centriod[0]) #更新相似度矩阵，删去cur对应的行和列
                temp_L = temp_L_update(temp_L,centriod) #更新temp_L，删去cur对应行  
                return group,matrix,temp_L #货架满，返回当前组和更新后L，寻找下一个质心

def optimize(dis_score,matrix):
    print('共',np.size(dis_score,0),"组，开始优化")
    
    for a in range(np.size(dis_score,0)):  #a , b为两相互交换元素的分配方案的索引,故 a！=b
        for b in range(np.size(dis_score,0)):
            if a == b: continue
            
            for i in range(np.size(dis_score[a][0],0)): #i ，j 为方案的元素
                for j in range(np.size(dis_score[b][0],0)):
                    temp_a =  np.array(dis_score[a][0])
                    temp_b =  np.array(dis_score[b][0])
                    
                    temp_a , temp_b = exchange(temp_a,i,temp_b,j) 
                    
                    if get_score(temp_a,matrix) + get_score(temp_b,matrix) > get_score(dis_score[a][0],matrix) + get_score(dis_score[b][0],matrix):
                        dis_score[a][0] = temp_a
                        dis_score[b][0] = temp_b
    
    for i in range(np.size(dis_score,0)):
        dis_score[i][1] = get_score(dis_score[i][0],matrix)
    
    return dis_score
                           
             



#--------------------------------------------test_code------------------------------------
#
# L = np.array([[0,100],[1,80],[2,70],[3,60]])
# matrix = [[[1, 5], [2, 2], [3, 3]], [[0, 5], [2, 3], [3, 4]], [[0, 2], [1, 3], [3, 5]], [[0, 3], [1, 4], [2, 5]], None]
# capacity = 2
# # centriod = [0,100]
# # group,matrix,L = get_group(L,matrix,capacity,centriod)
# plan = C_H(L,matrix,capacity)
# # print(group,matrix,L)  
# print(plan)              
# group_1 = np.array([[0,100],[1,80]])
# group_2 = np.array([[2,70],[3,60]])
# dis_score = np.array([[group_1,60],
#                       [group_2,30]])
# print(optimize(dis_score,matrix))
  
                
                
         