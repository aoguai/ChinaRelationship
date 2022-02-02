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


# 将文字转换成关系符号
def transformTitleToKey(text):
    result = text.replace("的", ",").replace("我", "").replace("爸爸", "f").replace("妈妈",
                                                                                "m").replace(
        "老公",
        "h").replace(
        "老婆", "w").replace("儿子", "s").replace("女儿", "d").replace("兄弟", "xd").replace("哥哥", "ob").replace("弟弟",
                                                                                                         "lb").replace(
        "姐妹",
        "xs").replace(
        "姐姐", "os").replace("妹妹", "ls").strip(",")
    return result


def errorMessage(key):
    message = key
    if key == "ob,h" or key == "xb,h" or key == "lb,h" or key == "os,w" or key == "ls,w" or key == "xs,w":
        message = "根据我国法律暂不支持同性婚姻，怎么称呼你自己决定吧"
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


# 从数据源中查找对应 key 的结果
def dataValueByKeys(data_text):
    dataName = '/data.json'
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
    keys = errorMessage(transformTitleToKey(txt))
    if keys != "根据我国法律暂不支持同性婚姻，怎么称呼你自己决定吧":
        result = dataValueByKeys(FilteHelper(keys))
        return result
    else:
        return keys


txt = input()
print(calculate(txt))