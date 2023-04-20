import json
import re


class RelationshipCounter:
    def __init__(self, data_file="data.json", filter_file="filter.json", reverse=False):
        self.data = self.load_json(data_file)
        self.filter = self.load_json(filter_file)["filter"]
        self.reverse = reverse  # 是否反转

    def load_json(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)

    # 称谓转换成关联字符
    def transform_title_to_key(self, string):
        result = string.replace("的", ",").replace("我", "").replace("爸爸", "f").replace("父亲", "f").replace("妈妈", "m").replace(
            "母亲", "m").replace("爷爷", "f,f").replace("奶奶", "f,m").replace("外公", "m,f").replace("姥爷", "m,f").replace("外婆",
                                                                                                               "m,m").replace(
            "姥姥", "m,m").replace("老公", "h").replace("丈夫", "h").replace("老婆", "w").replace("妻子", "h").replace("儿子",
                                                                                                         "s").replace(
            "女儿", "d").replace("兄弟", "xd").replace("哥哥", "ob").replace("弟弟", "lb").replace("姐妹", "xs").replace("姐姐",
                                                                                                           "os").replace(
            "妹妹", "ls").strip(",") + ","
        for f in self.filter:
            exp = "^" + f["exp"].replace("&", "\\&").replace(",", ".*") + "$"
            result = re.sub(exp, f["str"].replace("$", "\\"), result)
        if self.reverse:
            result = result.replace("f", "m").replace("m", "f")
        if result.endswith(","):
            result = result[:-1]
        return result

    # 错误关系判断
    def error_message(self, key):
        if key.find("ob,h") != -1 or key.find("xb,h") != -1 or key.find("lb,h") != -1 or key.find("os,w") != -1 or key.find(
                "ls,w") != -1 or key.find("xs,w") != -1 or key.find("f,h") != -1 or key.find("m,w") != -1 or key.find(
            "d,w") != -1 or key.find("s,h") != -1:
            return "根据我国法律暂不支持同性婚姻，怎么称呼你自己决定吧"
        elif key.find("h,h") != -1 or key.find("w,w") != -1:
            return "根据我国法律暂不支持重婚，怎么称呼你自己决定吧"
        return key

    # 关系链转换成称谓
    def transform_key_to_title(self, string):
        if not string:
            return None
        result = []
        seen = set()
        for s in string.split("#"):
            if s != self.error_message(s):
                return self.error_message(s)
            if s in self.data and self.data[s][0] not in seen:
                result.append(self.data[s][0])
                seen.add(self.data[s][0])
        # 如果结果为空，再使用逗号分割子字符串
        if not result:
            for s in string.split(','):
                if s != self.error_message(s):
                    return self.error_message(s)
                if s in self.data and self.data[s][0] not in seen:
                    result.append(self.data[s][0])
                    seen.add(self.data[s][0])
        result_str = ','.join(result)
        if self.reverse:
            result_str = result_str.replace("父", "母").replace("母", "父")
        return result_str


if __name__ == '__main__':
    rc = RelationshipCounter()
    print(rc.transform_key_to_title(rc.transform_title_to_key("我的爸爸")))
    print(rc.transform_key_to_title(rc.transform_title_to_key("我的父亲的儿子")))
    print(rc.transform_key_to_title(rc.transform_title_to_key("我的哥哥的丈夫")))
    print(rc.transform_key_to_title(rc.transform_title_to_key("我的哥哥的弟弟")))
    print(rc.transform_key_to_title(rc.transform_title_to_key("我的爸爸的爸爸")))
    print(rc.transform_key_to_title(rc.transform_title_to_key("我的哥哥的姐姐的妹妹")))
