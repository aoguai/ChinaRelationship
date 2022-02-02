# ChinaRelationship
一个简单的中国亲戚关系计算器 python实现版本
每年的春节，都会有一些自己几乎没印象但父母就是很熟的亲戚，关系凌乱到你自己都说不清。
今年趁着春节在家没事情干，正好之前知道有中国亲戚关系计算器，想着自己实现一下，特此记录。
## 算法实现与介绍
由于本人能力有限，只完成了基本功能....
### 需求
* 计算亲戚关系链得出我应该怎么称呼的结果
### 数据定义
    
1. 定义关系字符和修饰符
```python
【关系】f:父,m:母,h:夫,w:妻,s:子,d:女,xb:兄弟,ob:兄,lb:弟,xs:姐妹,os:姐,ls:妹

【修饰符】 &o:年长,&l:年幼,#:隔断,[a|b]:并列
```
2. 关系对应数据集合、关系过滤数据集合（data.json 和 filter.json）

原来参考的[作者](https://github.com/joywt/relationship)的关系过滤数据集合json有点问题，改了一下

 >**filter 数据集的用途：比如 m,h 是我的妈妈的丈夫就是爸爸，也就是 f。 filter 的作用是去重和简化，需要把 exp 用 str 进行替换**
 
### 算法实现
需要解决的情况基本有以下三种：
>我的爸爸 = 爸爸，

>我的哥哥的弟弟 = 自己/弟弟/哥哥，

>我的哥哥的老公 = ？

#### 分析
三种结果：1.单结果 2.多结果 3.错误提示 ，那么我们的算法要兼容以上三种情况
下面我们来一步步实现。

#### 算法主要函数一：transformTitleToKey
该函数主要负责**将文字转换成关系符号**
```python
# 将文字转换成关系符号
def transformTitleToKey(text):
    result = text.replace("的", ",").replace("我", "").replace("爸爸", "f").replace("父亲", "f").replace("妈妈","m").replace("母亲", "m").replace("爷爷","f,f").replace("奶奶","m,m").replace("老公","h").replace("丈夫", "h").replace("老婆", "w").replace("妻子", "h").replace("儿子", "s").replace("女儿", "d").replace("兄弟", "xd").replace("哥哥", "ob").replace("弟弟","lb").replace("姐妹","xs").replace("姐姐", "os").replace("妹妹", "ls").strip(",")
    return result
```
这里简化了原参考[作者](https://github.com/joywt/relationship)的写法，更 ~~简单（不是）~~ 符合计算器设定
![计算器](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_0.png)
#### 算法主要函数二：FilteHelper
该函数主要负责**去重和简化**
```python
# 去重和简化
# 去重和简化
def FilteHelper(text):
    result = text
    filterName = '/filter.json'  # filter.json文件路径
    if not os.path.isfile(filterName):
        return "filterName文件不存在"
    with open(filterName, "r") as f:
        obj = list(ijson.items(f, 'filter'))
    for i in range(len(obj[0])):
        users = obj[0][i]['exp']
        if re.match(obj[0][i]['exp'], result):  # 符合正则
            result1 = re.findall(obj[0][i]['exp'], result)
            result = obj[0][i]['str']
            a = 0
            result2 = ""
            try:
                for i in result1:
                    result = result.replace("$" + str(a + 1), result1[a])
                    a = a + 1
                while result.find("#") != -1:
                    result_l = result
                    resultList = list(set(result_l.split("#")))  # # 是隔断符，所以分割文本
                    for key in resultList:
                        result = FilteHelper(key)
                        if (result.find("#") == -1):  # 当关系符号不含#时加入最终结果中
                            result2 = result2 + result
                return result2
            except Exception as e:
                return text
    return text
```
这里原参考[作者](https://github.com/joywt/relationship)解释的有点乱，我就以我个人见解参考着写了出来...能跑....有错欢迎指出
个人测试单结果，多结果都能实现，**建议多结果实现参考输出和代码详细理解**
#### 算法主要函数三：dataValueByKeys
该函数主要负责**从数据源中查找对应 key 的结果**
```python
def dataValueByKeys(data_text):
    dataName = '/data.json'  # data.json文件路径
    if not os.path.isfile(dataName):
        return "data文件不存在"
    fo = open(dataName, 'r', encoding='utf-8')
    ID_Data = demjson.decode(fo.read())
    fo.close()
    try:
        if ID_Data[data_text]:
            cityID = ID_Data[data_text]
            text = ""
            for key in cityID:
                text = text + key + '\\'
            return text.strip("\\")
        else:
            return "未找到"
    except Exception as e: # 处理多结果
        result = ""
        resultList = FilteHelper(strInsert(data_text, 0, ',')).split(",")
        for key in resultList:
            result = result + dataValueByKeys(key)
        return result
```

### 输出与效果
![relationship_1](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_1.png)
![relationship_2](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_2.png)
![relationship_3](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_3.png)
![relationship_4](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_4.png)
 <br>基本达到效果
 
## 一些细节与已知问题
 首先，是性别：如果‘我’是女性，那么‘我的父亲的儿子’可以为[‘哥哥’，‘弟弟’]，而不可以包含‘我’。（上述代码没实现）<br>
另外，关于夫妻关系：在正常情况下，男性称谓只可以有‘妻子’，女性称谓只可以有‘丈夫’。（上述代码已实现）<br>
第三，多种可能：‘我的父亲的儿子’ 可以是[‘我’，‘哥哥’，‘弟弟’]，再若是再往后计算，如‘我的父亲的儿子的儿子’ ，需要同时考虑‘我的儿子’，‘哥哥的儿子’，‘弟弟的儿子’这三种可能。（上述代码已实现）<br>
已知问题：某些涉及自己的多重可能还存在莫名BUG

## 参考
站在巨人的肩膀上
### [hinese kinship system.中国亲戚关系计算器 - 家庭称谓/称呼计算/亲戚关系算法](https://github.com/mumuy/relationship)
### 算法主要参考了这个[亲戚关系计算器](https://github.com/joywt/relationship)
