from lxml import etree
import requests
import heapq
import time
import re

# 要爬取的url，注意：在开发者工具中，这个url指的是第一个url
url = "https://www.douban.com/group/656297/"

# 模仿浏览器的headers
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}
# 匹配关键字 若匹配到返回True 否则返回False
def compilText(pattern, compilStr):
    return pattern.search(compilStr) is not None

contents = []
count = 0
flag = 0
# for i in range(0,10):
while(1):
    try: 
        flag += 1
        curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("----------"+'第' + str(flag) + '次 ' + curtime +"----------")
        # get请求，传入参数，返回结果集
        resp = requests.get(url,headers=headers)
        # 将结果集的文本转化为树的结构
        tree = etree.HTML(resp.text)
        for id in range(2,25):
            title = tree.xpath('//*[@id="group-topics"]/div[2]/table/tr[' + str(id) + ']/td[1]/a/text()')[0].replace('\n','').replace('\r','').replace(' ','')
            info_url  = tree.xpath('//*[@id="group-topics"]/div[2]/table/tr[' + str(id) + ']/td[1]/a/@href')[0].replace('\n','').replace('\r','').replace(' ','')
            topicId = info_url.rsplit('/', 2)[-2]
            # print(title,info_url,topicId)
            if compilText(re.compile("开车"),title):
                contents.append((topicId,title,info_url))
                count += 1
        contents = list(set(contents))
        heapq._heapify_max(contents)
        if len(contents) > 10:
            contents = contents[:10]
        for content in contents:
            print(content)
        print(len(contents),count)
        print("--------------------")
        time.sleep(60)
    except Exception as e:
            import traceback
            print(traceback.format_exc())
            print('异常')
            time.sleep(10)
for content in contents:
    print(content)
print("总计：",len(contents),count)
'''
256834546   33

256834596   34

256834736   36

猜测帖子可以按照topicid来判断发帖时间排序
'''