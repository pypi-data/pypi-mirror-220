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
    stock_dict = {}
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
        self._pseg = _pseg_dict['gupiao']
        self.index_alias, self.enum_value, self.direct_enum_value, self.scope_word_alias, self.scope_word_order, self.index_unit,\
        self.unit_transform, self.match_words_dict, self.all_unit, Extractor.stock_dict, self.index_dict = corpus_process.get_corpus()


    def add_stock(self, stock_name, stock_code):
        res = re.search("^([a-zA-Z]{2})([a-zA-Z0-9]+)$", stock_code)
        if not res:
            return False
        letter_res = res.group(1).lower()
        number_res = res.group(2)
        Extractor.stock_dict[number_res + "." + letter_res] = stock_code
        code_lower = stock_code.lower()
        Extractor.stock_dict[code_lower] = stock_code
        Extractor.stock_dict[stock_name.replace(" ", "")] = stock_code
        Extractor.stock_dict[number_res] = stock_code
        return True



    def _extract_keyword(self, query):
        # concat_words = {"且": "&&", "并且": "&&", "&&": "&&", "&": "&&", "而且": "&&", "或": "||", "|": "||", "||": "||", "或者": "||", "or": "||", "and": "&&"}
        between_pattern = "(-?[\d]+\.?[\d]*(倍|亿|%|万|万亿)?)[—\-－一–~～到至](-?[\d]+\.?[\d]*(倍|亿|%|万|万亿)?)"
        all_words = set(self.index_alias.keys()).union(set(self.scope_word_alias.keys())).union(
            set(self.direct_enum_value.keys()))

        query = query.strip().lower()
        words = [w for w in self._pseg.cut(query) if w.word.strip()]
        # 助词去掉
        words = list(filter(lambda x: not x.flag.startswith("u"), words))
        _type = None
        word_list = [w.word for w in words]
        tag_list = [w.flag for w in words]
        index_hits = utils.max_backward_match(word_list, all_words)
        index_hits_type = []
        for i, index_hit in enumerate(index_hits):
            type = ""
            allowed_order = []
            hit_name = index_hit[0]
            if hit_name in self.index_alias:
                type = "指标"
                hit_name = self.index_alias[hit_name]
            elif hit_name in self.scope_word_alias:
                type = "范围类型"
                allowed_order = self.scope_word_order[hit_name]
                hit_name = self.scope_word_alias[hit_name]
            elif hit_name in self.direct_enum_value:
                type = "枚举指标"
                hit_name = self.direct_enum_value[hit_name]
            index_hits_type.append([hit_name, index_hit[1], index_hit[2], allowed_order, type])
        index_hits_final = []
        for i, iht in enumerate(index_hits_type):
            if iht[-1] == "枚举指标":
                index_hits_final.append(iht)
            if iht[-1] == "指标":
                if iht[0] in self.enum_value:
                    enum_result = self.enum_value[iht[0]]
                    end_index = len(word_list) if i + 1 >= len(index_hits_type) else index_hits_type[i + 1][1]
                    # 允许一个匹配
                    for j in range(iht[2], end_index):
                        if word_list[j] in enum_result:
                            index_hits_final.append(
                                [iht[0] + word_list[j], iht[1], iht[2], j, "枚举指标"])
                            break
                else:
                    index_hits_final.append(iht)

            elif iht[-1] == "范围类型":
                allowed_order = iht[3]
                for order in allowed_order:
                    if order == "after":
                        end_index = len(word_list) if i + 1 >= len(index_hits_type) else index_hits_type[i + 1][1]
                        value_list = []
                        for j in range(iht[2], end_index):
                            if tag_list[j] == "m" or word_list[j].isdigit() or \
                                    (j == end_index - 1 and word_list[j] in self.all_unit) or (j == iht[2] and word_list[j] == "-"):
                                value_list.append(word_list[j])
                            else:
                                break
                        if len(value_list) != 0 and not (len(value_list) == 1 and value_list[0] == "-"):
                            index_hits_final.append(
                                [[iht[0], "".join(value_list)], iht[1], iht[2] + len(value_list), "数字范围"])
                            break
                    elif order == "before":
                        start_index = 0 if i == 0 else index_hits_type[i - 1][2]
                        value_list = []
                        for j in range(iht[1] - 1, start_index-1, -1):
                            if tag_list[j] == "m" or word_list[j].isdigit() or \
                                    (j == iht[1] - 1 and word_list[j] in self.all_unit) or (
                                    j == start_index and word_list[j] == "-"):
                                value_list.append(word_list[j])
                            else:
                                break
                        value_list.reverse()
                        if len(value_list) != 0 and not (len(value_list) == 1 and value_list[0] == "-"):
                            index_hits_final.append(
                                [[iht[0], "".join(value_list)], iht[1] - len(value_list), iht[2], "数字范围"])
                            break
                    elif order == "null":
                        index_hits_final.append([[iht[0]], iht[1], iht[2], "数字范围"])
                        break
        index_hits_final_tmp = list(filter(lambda x: x[-1] != "数字范围", index_hits_final))
        index_hits = []
        if len(index_hits_final_tmp) > 0:
            left_start = 0
            left_end = index_hits_final_tmp[0][1]
            between_res = re.search(between_pattern, "".join(word_list[left_start:left_end]))
            if between_res:
                index_hits.append([["~", between_res.group(1), between_res.group(3)], left_start, left_end, "数字范围"])
        for i, index in enumerate(index_hits_final_tmp):
            right_start = index[2]
            right_end = len(word_list) if (i == len(index_hits_final_tmp) - 1 or len(index_hits_final_tmp) == 1) else \
                index_hits_final_tmp[i + 1][1]
            between_res = re.search(between_pattern, "".join(word_list[right_start:right_end]))
            if between_res:
                index_hits.append([["~", between_res.group(1), between_res.group(3)], right_start, right_end, "数字范围"])
        for index in index_hits_final:
            index_hits.append(index)
        #去掉数字范围中冲突的
        removed = set()
        index_hits_copy = index_hits.copy()
        for i, index in enumerate(index_hits_copy):
            if index[-1] == "数字范围":
                for j, index2 in enumerate(index_hits_copy):
                    if i != j and index2[1] >= index[1] and index2[2] <= index[2]:
                        removed.add(j)
        index_hits = []
        for i, index in enumerate(index_hits_copy):
            if i not in removed:
                index_hits.append(index)
        return index_hits, len(word_list)


    # 一个指标对应范围去掉冲突和无用的
    def _func(self, di, value_list):
        x = sorted(di.items(), key=lambda d: d[1], reverse=True)
        new_di = dict()
        allowed = []
        if len(x) >= 1:
            new_di[x[0][0]] = x[0][1]
            value = value_list[x[0][0]][0][0]
            if value in (">", ">="):
                allowed = ["<", "<="]
            elif value in ("<", "<="):
                allowed = [">", ">="]
        if len(x) >= 2:
            value = value_list[x[1][0]][0][0]
            valid = False
            for elem in allowed:
                valid = valid | (value == elem)
            if valid:
                new_di[x[1][0]] = x[1][1]
        return new_di

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

    # 优先级：
    # 范围在指标后优先
    # 距离越近越加分 +1/(距离+1)
    def _combine(self, index_hits, l):
        result = []
        index2value = dict()
        value2index = dict()
        index_list = []
        value_list = []
        for ih in index_hits:
            if ih[-1] == "枚举指标":
                result.append(ih[0])
                index_list.append(ih)
            elif ih[-1] == "指标":
                index_list.append(ih)
            elif ih[-1] == "数字范围":
                value_list.append(ih)
            else:
                print("error!")
                return []
        for i, index in enumerate(index_list):
            left_start = 0 if (i == 0 or len(index_list) == 1) else index_list[i - 1][2]
            left_end = index[1]
            right_start = index[2]
            right_end = l if (i == len(index_list) - 1 or len(index_list) == 1) else index_list[i + 1][1]
            if index[-1] == "指标":
                index2value[i] = {}
                for ii, value in enumerate(value_list):
                    if value[1] >= right_start and value[2] <= right_end:
                        # 后面优先，距离越近分数越高
                        index2value[i][ii] = 0.3 + 1 / (value[1] - right_start + 1)
                for ii in range(len(value_list) - 1, -1, -1):
                    value = value_list[ii]
                    if value[1] >= left_start and value[2] <= left_end:
                        index2value[i][ii] = 1 / (left_end - value[2] + 1)
                index2value[i] = self._func(index2value[i], value_list)
        for index, value_score in index2value.items():
            for value, score in value_score.items():
                if value not in value2index:
                    value2index[value] = dict()
                if score >= 0.5:
                    value2index[value][index] = score
        save1_value_index = dict()
        index_value = dict()
        for value, index_score in value2index.items():
            if len(index_score) > 0:
                save1_value_index[value] = sorted(index_score.items(), key=lambda d: d[1], reverse=True)[0][0]
                index = save1_value_index[value]
                if index not in index_value:
                    index_value[index] = []
                index_value[index].append(value)

        res = []
        for index, value in index_value.items():
            elem = [index_list[index][0]]
            for v in value:
                elem.append(self._extract_num_combine(value_list[v][0], index_list[index][0]))
            res.append(elem)

        for elem in result:
            res.append(elem)
        return res


    def process_sentence(self, sentence):
        stock_pick_words = ["选出", "找出", "股票"]
        parts = re.split("[,，!！?？、。]", sentence.lower())
        res = []
        stock_pick_flag = False
        for part in parts:
            index_hits, l = self._extract_keyword(part)
            res.extend(self._combine(index_hits, l))
            words = [w.word for w in self._pseg.cut(part)]
            for spw in stock_pick_words:
                if spw in words:
                    stock_pick_flag = True
                    break
            if stock_pick_flag:
                res.extend([self.match_words_dict[elem[0]] for elem in utils.max_backward_match(words, self.match_words_dict.keys())])
        #暂时过滤掉部分逻辑
        final_res = []
        for elem in res:
            if not isinstance(elem, str):
                final_res.append(elem)
        return final_res


    def analyze_query(self, query, is_question):
        #1.分词
        #2.最大后向匹配提取股票+指标并归一化
        #3.根据提取结果和text关键词判断 f10，诊股，选股，选股则调接口
        #返回类型和结果
        query_type, stocks, indexs, details = "", [], [], []
        q = query.strip().lower()
        query_cut = [word.word for word in self._pseg.lcut(q)]
        stocks = utils.max_backward_match(query_cut, self.stock_dict, pos_include=False)
        indexs = utils.max_backward_match(query_cut, self.index_dict, pos_include=False)
        stocks = [self.stock_dict[stock] for stock in stocks]
        indexs = [self.index_dict[index] for index in indexs]
        if len(stocks) != 0:
            if len(indexs) != 0:
                query_type = "F10"
                return query_type, stocks, indexs, details
            else:
                if is_question:
                    query_type = "诊股"
                    return query_type, stocks, indexs, details
                for need_w in ["怎么样", "如何", "买", "走势", "股票", "该不该", "怎样", "投资", "卖", "持有", "离场", "?", "还行",
                               "操作", "怎么", "是不是", "还是", "要不要", "哪些", "吗", "咋样", "咋说", "能否", "反弹", "可以", "跌",
                               "行不行", "成长性", "是吧", "？", "什么", "判断", "是否", "么"]:
                    if need_w in query:
                        query_type = "诊股"
                        return query_type, stocks, indexs, details
                else:
                    query_type = ""
                    return query_type, stocks, indexs, details
        else:
            #选股怎么判断 的股票 得股票 地股票
            details = self.process_sentence(query)
            if len(details) != 0:
                query_type = "选股"
            return query_type, stocks, indexs, details





# ex = Extractor()
# sentences = corpus_process.get_sentence()
# res = ex.analyze_query("600519的", True)
# print(res)
# #sentences = ["市值-100.7~300.6亿以内?市盈大于2小于3市净率在1-3之间，并且换手率小于5%"]
# #sentences = ["净利润增长率在5-10%之间"]
# for sentence in sentences:
#     print(sentence)
#     res = ex.analyze_query(sentence, True)
#     print(res)

























