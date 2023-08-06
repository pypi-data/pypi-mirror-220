import document_detection.utils as utils
import re
import os
import sys


_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__), path))

class Detection:
    def __init__(self):
        # self.device_dict = utils.read_device(_get_module_path("device.txt"))
        # self.device_names = set(self.device_dict.keys())
        self.state_words = utils.read_words(_get_module_path("state_word.txt"))
        self.scope_words = utils.read_scope_words(_get_module_path("scope_table"))
        self.scope_words1 = "|".join(self.scope_words.get("case1", []))
        self.scope_words2 = "|".join(self.scope_words.get("case2", []))


    #todo:test 记住root一定是""或者无意义，但是不能是None
    def catalog_check(self, tree1, tree2):
        #res = {"less":["cat1/cat2/cat3"], "more":["cat1"]}
        less, more = utils.check_tree_diff(tree1, tree2)
        res = {"less":less, "more":more}
        return res


    #todo:test
    #check_dict   {"标准词":["非标准词1", "非标准词2"]}
    def extract_standard_device(self, sentence, check_dict):
        #res = [{"device_name":"", "position":(0,10), "standard_device_name":""}]
        device_dict = dict()
        for standard_word, words in check_dict.items():
            for word in words:
                device_dict[word] = standard_word
            device_dict[standard_word] = standard_word
        res = utils.max_backward_match(sentence, device_dict.keys(), max_k=10)
        res = [{"device_name":elem[0], "position":(elem[1], elem[2]), "standard_device_name":device_dict[elem[0]]} for elem in res]
        return res


    #todo:test
    def invalid_reference_check(self, sentence):
        #res = [{"reference":"", "position":(0,10)}]
        res = []
        iter = re.finditer("《.*》", sentence)
        for elem in iter:
            res.append((elem.group(0), elem.span()))
        iter = re.finditer("[^,，。！!/?？；;~～]{0,10}说明书|手册", sentence)
        for elem in iter:
            res.append((elem.group(0), elem.span()))
        res = [{"reference": elem[0], "position": elem[1]} for elem in res]
        return res


    #sentences=[{"sentence":"", "document_name":"", "position":(1,2)}]
    def similar_expression(self, sentences, check_dict, threshold=0.7):
        #res = [{"sentence":"", "document_name":"", "position":(1,2), "similar_sentences":[{"sentence":"", "document_name":"", "position":(2,3)}]}]
        res = []
        device_dict = dict()
        device_dict_res = dict()
        for standard_word, words in check_dict.items():
            for word in words:
                device_dict[word] = standard_word
            device_dict[standard_word] = standard_word
        for i, sentence in enumerate(sentences):
            device_res = utils.max_backward_match(sentence["sentence"], device_dict.keys(), 10)
            for device in device_res:
                standard_device_name = device_dict[device[0]]
                if standard_device_name not in device_dict_res:
                    device_dict_res[standard_device_name] = set()
                device_dict_res[standard_device_name].add(i)
        di = dict()
        for device in device_dict_res:
            pos_list = device_dict_res[device]
            for i in pos_list:
                di[i] = []
                for j in pos_list:
                    if i != j:
                        sim = utils.similarity(sentences[i]["sentence"], sentences[j]["sentence"])
                        if sim > threshold:
                            di[i].append(j)
        for i in di:
            pos_list = di[i]
            if len(pos_list) > 0:
                elem_di = sentences[i].copy()
                elem_di["similar_sentences"] = [sentences[j] for j in pos_list]
                res.append(elem_di)
        return res


    def abnormal_number_check(self, sentence):
        res = []
        scope_pos_list = []
        number_list = []
        pattern = self.scope_words1 + "([^,，。！!/?？；;~～]{1,10}的)?(-?[0-9]+(\.[0-9]+)?)"
        for case in re.finditer(pattern, sentence):
            scope_pos_list.append(case.span())
        pattern = "(-?[0-9]+(\.[0-9]+)?)" + self.scope_words2
        for case in re.finditer(pattern, sentence):
            scope_pos_list.append(case.span())
        pattern = "(-?[0-9]+(\.[0-9]+)?)[^,，。！!/?？；;~～]{0,4}[\-—~～到至±](-?[0-9]+(\.[0-9]+)?)($|[^0-9\-~～到至]+)"
        for case in re.finditer(pattern, sentence):
            scope_pos_list.append(case.span())
        pattern = "([0-9]+(月|日|年))"
        for case in re.finditer(pattern, sentence):
            scope_pos_list.append(case.span())
        pattern = "(-?[0-9]+(\.[0-9]+)?)"
        for case in re.finditer(pattern, sentence):
            number_list.append(case.span())
        for number in number_list:
            flag = True
            for scope_pos in scope_pos_list:
                if number[0] >= scope_pos[0] and number[1] <= scope_pos[1]:
                    flag = False
            if flag:
                res.append(number)
        return {"positions": res}


    #todo:无状态词典
    def detection_check(self, sentence):
        #res = {"position":[(1,2), (4,7)]}
        pos = []
        res = re.finditer("检查.*(确保|是否|有无)([^,，。！？!、/?]*)", sentence)
        for elem in res:
            elem_state = elem.group(2)
            flag = True
            for sw in self.state_words:
                if sw in elem_state:
                    flag = False
            if flag:
                pos.append(elem.span())
        res = {"position": pos}
        return res


