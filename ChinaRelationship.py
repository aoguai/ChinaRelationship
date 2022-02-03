# 【关系】f:父,m:母,h:夫,w:妻,s:子,d:女,xb:兄弟,ob:兄,lb:弟,xs:姐妹,os:姐,ls:妹
# 【修饰符】 &o:年长,&l:年幼,#:隔断,[a|b]:并列
import os
import re

import demjson
import ijson as ijson


# 在字符串指定位置插入字符
# str_origin：源字符串  pos：插入位置  str_add：待插入的字符串
#
def strInsert(strOrigin, pos, strAdd):
    strList = list(strOrigin)  # 字符串转list
    strList.insert(pos, strAdd)  # 在指定位置插入字符串
    strOut = ''.join(strList)  # 空字符连接
    return strOut

# 检查整个字符串是否包含中文
def isChinese(string):
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


# 将文字转换成关系符号
def transformTitleToKey(text):
    result = text.replace("的", ",").replace("我", "").replace("爸爸", "f").replace("父亲", "f").replace("妈妈", "m").replace(
        "母亲", "m").replace("爷爷", "f,f").replace("奶奶", "f,m").replace("外公", "m,f").replace("姥爷", "m,f").replace("外婆", "m,m").replace("姥姥", "m,m").replace("老公", "h").replace("丈夫", "h").replace("老婆",
                                                                                                           "w").replace(
        "妻子", "h").replace("儿子", "s").replace("女儿", "d").replace("兄弟", "xd").replace("哥哥", "ob").replace("弟弟",
                                                                                                         "lb").replace(
        "姐妹", "xs").replace("姐姐", "os").replace("妹妹", "ls").strip(",")
    return result


def errorMessage(key):
    message = key
    if key.find("ob,h") != -1 or key.find("xb,h") != -1 or key.find("lb,h") != -1 or key.find("os,w") != -1 or key.find("ls,w") != -1 or key.find("xs,w") != -1 or key.find("f,h") != -1 or key.find("m,w") != -1 or key.find("d,w") != -1 or key.find("s,h") != -1:
        message = "根据我国法律暂不支持同性婚姻，怎么称呼你自己决定吧"
    elif (key.find("h,h") != -1 or key.find("w,w") != -1):
        message = "根据我国法律暂不支持重婚，怎么称呼你自己决定吧"
    return message


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
        if users == result:
            return obj[0][i]['str']
        elif re.match(obj[0][i]['exp'], result):  # 符合正则
            result1 = re.findall(obj[0][i]['exp'], result)  # 返回string中所有与pattern匹配的全部字符串,返回形式为数组
            print(result1)
            a = 0
            result2 = ""
            if len(result1)>1:
                try:
                    for i in len(result1):
                        result = result.replace("$" + str(a + 1), result1[a])
                        a = a + 1
                    if result.find("#") != -1:
                        result_l = result
                        resultList = list(set(result_l.split("#")))  # # 是隔断符，所以分割文本
                        for key in resultList:
                            result = FilteHelper(key.strip(","))
                            if (result.find("#") == -1):  # 当关系符号不含#时加入最终结果中
                                result2 = result2 + result
                        return result2
                    else:
                        return text
                except Exception as e:
                    return text
            else:
                return str(result1).replace("[\'", "").replace("\']", "")
        elif re.match(obj[0][i]['exp'], strInsert(result, 0, ',')):  # 符合正则
            result1 = re.findall(obj[0][i]['exp'], strInsert(result, 0, ','))  # 返回string中所有与pattern匹配的全部字符串,返回形式为数组
            a = 0
            result2 = ""
            if len(result1)>1:
                try:
                    for i in len(result1):
                        result = result.replace("$" + str(a + 1), result1[a])
                        a = a + 1
                    if result.find("#") != -1:
                        result_l = result
                        resultList = list(set(result_l.split("#")))  # # 是隔断符，所以分割文本
                        for key in resultList:
                            result = FilteHelper(key.strip(","))
                            if (result.find("#") == -1):  # 当关系符号不含#时加入最终结果中
                                result2 = result2 + result
                        return result2
                    else:
                        return text
                except Exception as e:
                    return text
            else:
                return str(result1).replace("[\'", "").replace("\']", "")
    return text

# 从数据源中查找对应 key 的结果
def dataValueByKeys(data_text):
    if(isChinese(data_text)):  # 判断是否含有中文，含有的是特殊回复
        return data_text
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
    except Exception as e:
        result = ""
        resultList = FilteHelper(strInsert(data_text, 0, ',')).split(",")
        for key in resultList:
            result = result + dataValueByKeys(key)
        return result


def calculate(text):
    keys = errorMessage(transformTitleToKey(text))
    result = ""
    resultList = list(set(dataValueByKeys(FilteHelper(keys)).split("\\")))
    for key in resultList:
        result = result + key.strip(",") + '\\'
    return result.strip("\\")


txt = input()
print(calculate(txt))
