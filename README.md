# ChinaRelationship

一个简单的中国亲戚关系计算器 python实现版本

每年的春节，都会有一些自己几乎没印象但父母就是很熟的亲戚，关系凌乱到你自己都说不清。

今年（2022年）趁着春节在家没事情干，正好之前知道有中国亲戚关系计算器，想着自己实现一下，特此记录。

## 如何使用

该程序的默认数据和过滤文件分别为`data.json`和`filter.json`。

如果您需要更改这些文件的位置，请在类的构造函数中传入相应的参数。

您可以按如下方式使用该程序：
```python
from RelationshipCounter import RelationshipCounter

rc = RelationshipCounter()
rc.transform_key_to_title(rc.transform_title_to_key("我的爸爸"))
rc.transform_key_to_title(rc.transform_title_to_key("我的父亲的儿子"))
rc.transform_key_to_title(rc.transform_title_to_key("我的哥哥的丈夫"))
rc.transform_key_to_title(rc.transform_title_to_key("我的哥哥的弟弟"))
rc.transform_key_to_title(rc.transform_title_to_key("我的爸爸的爸爸"))
rc.transform_key_to_title(rc.transform_title_to_key("我的哥哥的姐姐的妹妹"))
```

## 算法与函数介绍

简单介绍一下实现思路

### 数据定义与准备

1. 定义关系字符和修饰符

    关系：f:父,m:母,h:夫,w:妻,s:子,d:女,xb:兄弟,ob:兄,lb:弟,xs:姐妹,os:姐,ls:妹
    
    修饰符：&o:年长,&l:年幼,#:隔断,[a|b]:并列

2. 关系对应数据集合、关系过滤数据集合（data.json 和 filter.json）
3. 分析算法要兼容的结果

   需要解决的情况基本有以下三类：  
    >我的爸爸 = 爸爸，  
    
    >我的哥哥的弟弟 = 自己/弟弟/哥哥，  
    
    >我的哥哥的老公 = ？  

### 算法实现与函数说明

`transform_title_to_key`

将中文称呼转换为关联字符。例如，"我的爸爸"被转换为"f"。函数使用过滤器过滤掉不良关系。

这里简化了原参考[作者](https://github.com/joywt/relationship)的写法，更 ~~简单（不是）~~ 符合计算器设定

![计算器](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_0.png)

`transform_key_to_title`

将关联字符转换为中文称呼。例如，"f"被转换为"父亲"。

`error_message`

检查是否存在不合法关系链并返回相应错误信息。

### 输出与效果

![relationship_1](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_1.png)
![relationship_2](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_2.png)
![relationship_3](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_3.png)
![relationship_4](https://github.com/aoguai/ChinaRelationship/blob/main/images/relationship_4.png)

基本达到效果

## 一些细节与已知问题
* 如果‘我’是女性，那么‘我的父亲的儿子’可以为[‘哥哥’，‘弟弟’]，而不可以包含‘我’。（上述代码未实现）
* 关于夫妻关系：在正常情况下，男性称谓只可以有‘妻子’，女性称谓只可以有‘丈夫’。（上述代码已实现）
* 多种可能：‘我的父亲的儿子’ 可以是[‘我’，‘哥哥’，‘弟弟’]，再若是再往后计算，如‘我的父亲的儿子的儿子’ ，需要同时考虑‘我的儿子’，‘哥哥的儿子’，‘弟弟的儿子’这三种可能。（上述代码已实现）

已知问题：某些涉及自己的多重可能还存在莫名BUG

## 参考
[hinese kinship system.中国亲戚关系计算器 - 家庭称谓/称呼计算/亲戚关系算法](https://github.com/mumuy/relationship)
算法主要参考了[亲戚关系计算器](https://github.com/joywt/relationship)