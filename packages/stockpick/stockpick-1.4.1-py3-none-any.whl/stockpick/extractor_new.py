#1.识别指标
#如PE
#分完美匹配，其次别名，其次考虑错别字或者字向量相近

#2.指标对应类型：数字型、枚举
#数字型：走范围逻辑、相等逻辑（模糊？）、排序逻辑，默认单向范围
#枚举型：走枚举逻辑，考虑相近说法

#3.判断and or not 及先后结合顺序，默认and
#找到指标后 连接后面所有对应直到找到下一个指标
#问题：对应可能在前面 如：大于10倍市盈

#4.异常处理
#如果没找到指标：考虑用实体识别方式
#如果找到指标后面无对应或对应奇怪

#TODO:
#数字后处理，如%，万，倍等，是否应该推理单位？单位合理性
#等于的处理？默认等于上下的范围？
#"或"的情况？
#判断冲突？
#汉字数字情况
#指标分配范围时 多个范围冲突如>30又>20，同一级别应只保留一个最可能的
#分段后处理，会损失一部分情况？有没有更好办法
#找同义词存入词表 OR定位实体对应相应词（需要训练NER模型）
#复杂情况：如20倍市盈率以下
#指标+范围分数计算优化，如指标限定范围或者指标范围可能性分数
#TOPn情况更多情况


#topn情况：
#前[num]
#最大/小的[num]个 出现最大/最小可无num 默认为1
#topn 分词时会分成一个



import os
import re
from jieba import Tokenizer
from jieba.posseg import POSTokenizer
import stockpick.utils as utils
import stockpick.corpus_process as corpus_process

_pseg_dict = {}
_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__), path))
class Extractor():
    def init(self, **kwargs):
        """
          Args:
              ``` dt ```                : class Tokenizer from jieba
              ``` user_dict_path ```    : user cut dict path
        """
        _cut = Tokenizer()
        _cut.load_userdict(_get_module_path("gupiao_dict.txt"))

        _pseg_dict["gupiao"] = POSTokenizer(_cut)


    def __init__(self):
        self.init()
        self.index_alias, self.enum_value, self.direct_enum_value, self.scope_word_alias, self.scope_word_order, self.index_unit, self.unit_transform = corpus_process.get_corpus()

    def _extract_keyword(self, txt):
            # 为【分母】10-20%
            pattern = "(投资比例|比例)?(" + self.scope_case[
                "case2"] + ")([^0-9\-,，]*)的?【?(-?[0-9]+(\.[0-9]+)?)】?(%|％|倍)?[\-—~～到至]【?(-?[0-9]+(\.[0-9]+)?)】?(%|％|倍)($|[^0-9\-~]+)"
            res = re.search(pattern, txt)
            if res:
                scope_word = res.group(2)
                denominator_keyword = res.group(3)
                ratio1 = float(res.group(4))
                ratio2 = float(res.group(7))
                unit = res.group(9)
                if unit == "倍":
                    ratio1 *= 100
                    ratio2 *= 100
                threshold_type, high_threshold, low_threshold = self.process_num(scope_word, ratio1, ratio2,
                                                                                 self.find_include(res.group(4) + unit,
                                                                                                   txt),
                                                                                 self.find_include(res.group(7) + unit,
                                                                                                   txt))
                index_type = "比例数值"
            else:
                # 占【分母】的比例低于10%
                pattern = "占([^,，]*)的?比例(合计|为)?(" + self.scope_case[
                    "case1"] + ")【?(-?[0-9]+(\.[0-9]+)?)】?(%|％|倍)($|[^0-9\-~～到至]+)"
                res = re.search(pattern, txt)
                if res:
                    scope_word = res.group(3)
                    denominator_keyword = res.group(1)
                    ratio = float(res.group(4))
                    unit = res.group(6)
                    if unit == "倍":
                        ratio *= 100
                    threshold_type, high_threshold, low_threshold = self.process_num(scope_word, ratio, None,
                                                                                     self.find_include(
                                                                                         res.group(4) + unit, txt),
                                                                                     None)
                    index_type = "比例数值"
                else:
                    # 不超过【分母】5倍
                    pattern = "(投资比例|比例)?(" + self.scope_case[
                        "case1"] + ")([^0-9\-,，]*)的?【?(-?[0-9]+(\.[0-9]+)?)】?(%|％|倍)($|[^0-9\-~～到至]+)"
                    res = re.search(pattern, txt)
                    if res:
                        scope_word = res.group(2)
                        denominator_keyword = res.group(3)
                        ratio = float(res.group(4))
                        unit = res.group(6)
                        if unit == "倍":
                            ratio *= 100
                        threshold_type, high_threshold, low_threshold = self.process_num(scope_word, ratio, None,
                                                                                         self.find_include(
                                                                                             res.group(4) + unit, txt),
                                                                                         None)
                        index_type = "比例数值"
                    else:
                        pattern = "([^0-9\-,，]*)的?【?(-?[0-9]+(\.[0-9]+)?)】?(%|倍)(" + self.scope_case["case3"] + ")"
                        res = re.search(pattern, txt)
                        if res:
                            denominator_keyword = res.group(1)
                            scope_word = res.group(5)
                            ratio = float(res.group(2))
                            unit = res.group(4)
                            if unit == "倍":
                                ratio *= 100
                            threshold_type, high_threshold, low_threshold = self.process_num(scope_word, ratio, None,
                                                                                             self.find_include(
                                                                                                 res.group(2) + unit,
                                                                                                 txt), None)
                            index_type = "比例数值"
                        else:
                            pattern = "(.*)(" + self.scope_case["case4"] + ").*[：:为是]【?(-?[0-9]+(\.[0-9]+)?)】?(%|％|倍)"
                            res = re.search(pattern, txt)
                            if res:
                                scope_word = res.group(2)
                                denominator_keyword = res.group(1)
                                ratio = float(res.group(3))
                                unit = res.group(5)
                                if unit == "倍":
                                    ratio *= 100
                                threshold_type, high_threshold, low_threshold = self.process_num(scope_word, ratio,
                                                                                                 None,
                                                                                                 self.find_include(
                                                                                                     res.group(
                                                                                                         3) + unit,
                                                                                                     txt), None)
                                index_type = "比例数值"
                            else:
                                pattern = "(" + self.scope_case["case1"] + ")【?([0-9]+(\.[0-9]+)?)】?年($|[^0-9\-~～到至]+)"
                                res = re.search(pattern, txt)
                                if res:
                                    denominator_keyword = txt[:res.start()]
                                    index_type = "绝对数值"
                                    scope_word = res.group(1)
                                    ratio = res.group(2)
                                    threshold_type, high_threshold, low_threshold = self.process_num(scope_word, ratio,
                                                                                                     None,
                                                                                                     self.find_include(
                                                                                                         res.group(
                                                                                                             2) + "年",
                                                                                                         txt), None)
                                else:
                                    # 不超过该股票前60交易日日均成交金额的30%
                                    pattern = "(" + self.scope_case[
                                        "case1"] + ")(([^0-9\-,，]*)前[0-9]+([^0-9\-,，]*))【?(-?[0-9]+(\.[0-9]+)?)】?(%|％|倍)($|[^0-9\-~～到至]+)"
                                    res = re.search(pattern, txt)
                                    if res:
                                        denominator_keyword = res.group(2)
                                        index_type = "比例数值"
                                        scope_word = res.group(1)
                                        ratio = res.group(5)
                                        unit = res.group(7)
                                        threshold_type, high_threshold, low_threshold = self.process_num(
                                            scope_word, float(ratio), None, self.find_include(ratio + unit, txt), None)
                                    else:
                                        pattern = "申报的(数量|金额)(" + self.scope_case["case1"] + ")([^0-9])+$"
                                        res = re.search(pattern, txt)
                                        if res:
                                            denominator_keyword = res.group(3)
                                            index_type = "比例数值"
                                            scope_word = res.group(2)
                                            ratio = 100
                                            threshold_type, high_threshold, low_threshold = self.process_num(
                                                scope_word, float(ratio), None)
                                        else:
                                            # 0.90＜N＜0.92，商品期货合约价值（轧差）：-18~18%
                                            pattern = "(.*)[:：](-?[0-9]+(\.[0-9]+)?)[%％]?[\-—~～到至](-?[0-9]+(\.[0-9]+)?)[%％]"
                                            res = re.search(pattern, txt)
                                            if res:
                                                denominator_keyword = res.group(1)
                                                index_type = "比例数值"
                                                ratio1 = res.group(2)
                                                ratio2 = res.group(4)
                                                threshold_type, high_threshold, low_threshold = self.process_num(
                                                    "范围", float(ratio1), float(ratio2))
                                            else:
                                                pattern = "(.*)[:：为](-?[0-9]+(\.[0-9]+)?)[%％]"
                                                res = re.search(pattern, txt)
                                                if res:
                                                    denominator_keyword = res.group(1)
                                                    index_type = "比例数值"
                                                    ratio = res.group(2)
                                                    threshold_type, high_threshold, low_threshold = self.process_num(
                                                        "<=", float(ratio), None)


    # 单位转换，提取数字
    def _transform_number(self, index, num_str):
        regex = "(-?[\d]+\.?[\d]*)(.*)"
        res = re.match(regex, num_str)
        number = res.group(1)
        unit = res.group(2)
        default_unit = self.index_unit[index]["default_unit"]
        if default_unit in self.unit_transform:
            times = self.unit_transform[default_unit].get(unit, 1)
        else:
            times = self.unit_transform["null"].get(unit, 1)
        return float(number) * times


    def _extract_num_combine(self, li, index):
        symbol = li[0]
        new_li = [symbol]
        for elem in li[1:]:
            new_li.append(self._transform_number(index, elem))
        return new_li




    def process_sentence(self, sentence):
        parts = re.split("[,，!！?？、。]", sentence.lower())
        res = []
        for part in parts:
            index_hits, l = self._extract_keyword(part)
            res.extend(self._combine(index_hits, l))
        return res







ex = Extractor()
#sentences = corpus_process.get_sentence()
sentences = ["市值-100.7~300.6亿以内?市盈大于2小于3市净率在1-3之间"]
for sentence in sentences:
    print(sentence)
    res = ex.process_sentence(sentence)
    print(res)
    print("\n\n\n")






































