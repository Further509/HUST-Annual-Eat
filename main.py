import requests
import json
from collections import defaultdict
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

account = input("请输入你的账户号（学号/工号）：")
JSESSIONID = input("请输入你的JSESSIONID：")

url_template = "http://ecard.m.hust.edu.cn/wechat-web/QueryController/select.html?jsoncallback=jQuery21402777983544074327_1735390337447&account={account}&curpage={page}&dateStatus={date}&typeStatus=2&_=1735390337442"
cookie = {
    "JSESSIONID": JSESSIONID,
}
data_list = []  

def get_data(account, date, url_template, cookie):
    global data_list
    # 获取第一页数据
    curpage = 1
    response = requests.get(url_template.format(account = account, page=curpage,date = date), cookies=cookie)
    response_text = response.text.strip("callJson(").rstrip(")")
    data = json.loads(response_text)

    # 检查是否有数据
    if data['retcode'] == '0':
        while True:
            # 提取当前页的数据
            for item in data['consume']:
                data_list.append({
                    'mercname': item['mercname'],
                    'tranamt': item['tranamt']
                })
            
            # 检查是否有下一页
            if int(data['nextpage']) <= curpage:  # 如果下一页编号小于等于当前页，则结束循环
                break
            curpage = int(data['nextpage'])  # 更新当前页编号
            response = requests.get(url_template.format(account=account, page=curpage, date = date), cookies=cookie)
            response_text = response.text.strip("callJson(").rstrip(")")
            data = json.loads(response_text)
            
            # 检查返回状态
            if data['retcode'] != '0':
                print("Failed to retrieve data:", data['errmsg'])
                break

# 2024年年终总结
date_list = ['2024-01-01','2023-02-01','2024-03-01','2024-04-01','2024-05-01','2024-06-01','2024-07-01','2024-08-01','2024-09-01','2024-10-01','2024-11-01','2024-12-01']

for date in date_list:
    get_data(account, date, url_template, cookie)
    
# 使用defaultdict来存储相同mercname的tranamt总和
tranamt_sum = defaultdict(float)

for item in data_list:
    tranamt_sum[item['mercname']] += int(item['tranamt'])/100

sorted_tranamt = sorted(tranamt_sum.items(), key=lambda x: x[1], reverse=True)
mercnames, amounts = zip(*sorted_tranamt)

plt.figure(figsize=(16, 9))
plt.bar(mercnames, amounts, color='skyblue') 
plt.xlabel('商户名称') 
plt.ylabel('总交易金额')  
plt.title('各商户总交易金额')  
plt.xticks(rotation=45, ha='right') 
plt.tight_layout() 
plt.show() 