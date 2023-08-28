import numpy as np
import pandas as  pd

orders = pd.read_csv('orders.csv', header=None)

orders = orders.apply(lambda x: x.dropna().tolist(), axis=1)

orders = orders.to_list()

with open('SKU.txt', 'r') as f:
    lines = f.readlines()
    lines = set([line.strip() for line in lines])

# 查找所有包含货物集合子集的订单 
#orders = orders[orders.apply(lambda x: set(x).issubset(lines))]
#output = pd.DataFrame(orders)
#output.to_csv('now_oders.csv',encoding='utf_8_sig')
order_del = []
for i  in range(len(orders)):
    order = orders[i]
  #  print('正在处理订单',i,'内容为：',order)
    flag  = -1
    cur_del = []
    for j in range(len(order)):
        if order[j] in lines:
            flag += 1
        else:
            cur_del.append(order[j])
    if flag < 1:
        order_del.append(orders[i])
       # print('需删除订单：',order_del)
    else:
       # print('需修改当前订单:',order)
        for k in range(len(cur_del)):
            order.remove(cur_del[k])
       # print(order)   
        orders[i] = order   
for i in range(len(order_del)):
   # print(order_del[i])
    orders.remove(order_del[i])
'''        
for order in orders:           
    for book in order:
     if(book in lines):
        pass
     else:
        print("Error")
'''

orders = np.array(orders)

lines = list(lines)

length = len(lines)
id = {}
for i in range(length):
    id[lines[i]] = i

df = pd.DataFrame.from_dict(id, orient='index',columns=['id'])
df = df.reset_index().rename(columns = {'index':'book'})

df.to_csv('book_id.csv',encoding="utf_8_sig")

sum = np.zeros((length,length))

for i in range(len(orders)):
    cur = orders[i]
    for j in range(len(cur)):
        cur_row = id[cur[j]]
        for k in range(len(cur)):
            if(k != j):
                sum[cur_row][id[cur[k]]] += 1

output = pd.DataFrame(sum)
output.to_csv('output.csv')
