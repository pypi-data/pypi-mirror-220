import re
import os
import pandas as pd
import json

_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__), path))

def _read_sentences(filename):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            lines.append(line.strip().lower())
    return lines


def _read_table(filename):
    res = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            line = re.split("\s+", line.strip().lower())
            res.append(line)
    di = dict()
    if len(res) > 0:
        for i, line in enumerate(res):
            if i == 0:
                for name in res[0]:
                    di[name] = []
            else:
                for j, name in enumerate(res[0]):
                    if j >= len(line):
                        break
                    di[name].append(line[j])
    return di


def get_stock_dict(filename):
    di = dict()
    json_dict = json.load(open(filename))
    for key in json_dict:
        elems = json_dict[key]
        for code in elems:
            if elems[code]["stock_tags"] in ("深A", "沪A", "京A"):
                res = re.search("^([a-zA-Z]{2})([0-9a-zA-Z]+)$", code)
                if not res:
                    continue
                letter_res = res.group(1).lower()
                number_res = res.group(2)
                di[number_res+"."+letter_res] = code
                stock_name = elems[code]["stock_name"].replace(" ", "")
                code_lower = code.lower()
                di[code_lower] = code
                di[stock_name] = code
                di[number_res] = code
    return di


def get_index_dict(filename):
    di = dict()
    with open(filename, "r") as f:
        for line in f:
            words = line.strip().split("\t")
            for word in words[1:]:
                di[word] = words[0]
    return di


def _process_table(index_table, scope_table, enum_table, unit_table, match_words):
    index_alias = dict()
    index_unit = dict()
    scope_word_alias = dict()
    scope_word_order = dict()
    all_unit = set()

    match_words_dict = dict()
    for id, word in zip(match_words["id"], match_words["word"]):
        if not isinstance(word, float):
            match_words_dict[word.lower().strip()] = (id.strip(), word)


    for name, alias, default_unit, possible_unit in zip(index_table["name"], index_table["alias"], index_table["default_unit"], index_table["possible_unit"]):
        name = name.strip().lower()
        alias = re.split("[,，]", alias)
        alias.append(name)
        alias = [elem.strip().lower() for elem in alias]
        for elem in alias:
            index_alias[elem] = name
        default_unit = default_unit.strip().lower()
        possible_unit = re.split("[,，]", possible_unit)
        possible_unit = [elem.strip().lower() for elem in possible_unit]
        possible_unit.append(default_unit)
        all_unit = all_unit.union(set(possible_unit))
        possible_unit = list(set(possible_unit))
        index_unit[name] = {"default_unit": default_unit, "possible_unit": possible_unit}

    for word, norm_name, allowed_order in zip(scope_table["word"], scope_table["norm_name"], scope_table["allowed_order"]):
        word = word.strip().lower()
        norm_name = norm_name.strip()
        allowed_order = re.split("[,，]", allowed_order)
        allowed_order = [elem.strip() for elem in allowed_order]
        scope_word_alias[word] = norm_name
        scope_word_order[word] = allowed_order

    #指标对应枚举
    enum_value = dict()
    direct_enum_value = dict()
    for alias, name, result in zip(enum_table["alias"], enum_table["name"], enum_table["result"]):
        name = name.strip().lower()
        result = result.strip().lower()
        alias = re.split("[,，]", alias)
        if name not in enum_value:
            enum_value[name] = set()
        enum_value[name].add(result)
        for d_name in alias:
            direct_enum_value[d_name.strip().lower()] = name + result
        direct_enum_value[name + result] = name + result

    #单位转换
    unit_transform = dict()
    for base_unit, unit, times in zip(unit_table["base_unit"], unit_table["unit"], unit_table["times"]):
        base_unit, unit, times = base_unit.strip().lower(), unit.strip().lower(), float(times.strip().lower())
        if base_unit not in unit_transform:
            unit_transform[base_unit] = dict()
        unit_transform[base_unit][unit] = times

    stock_dict = get_stock_dict(_get_module_path("stock.json"))
    index_dict = get_index_dict(_get_module_path("f10.txt"))
    return index_alias, enum_value, direct_enum_value, scope_word_alias, scope_word_order, index_unit, unit_transform, match_words_dict, all_unit, stock_dict, index_dict


def get_corpus():
    index_table = {elem[0]:elem[1].values() for elem in pd.read_csv(_get_module_path("index_table.csv")).fillna("null").to_dict().items()}
    scope_table = _read_table(_get_module_path("scope_table"))
    enum_table = _read_table(_get_module_path("enum_table"))
    unit_table = _read_table(_get_module_path("unit_table"))
    match_words = pd.read_csv(_get_module_path("match_words.csv"))
    return _process_table(index_table, scope_table, enum_table, unit_table, match_words)


def get_sentence():
    return _read_sentences("sentences.txt")

# index_alias, enum_value, direct_enum_value = get_corpus()
# print(index_alias)
# print(enum_value)
# print(direct_enum_value)