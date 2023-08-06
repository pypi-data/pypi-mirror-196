import document_detection.utils as utils
import re
import os


_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),
                                                 os.path.dirname(__file__), path))

class Detection:
    def __init__(self):
        self.device_dict = utils.read_device("device.txt")
        self.device_names = set(self.device_dict.keys())
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
    def extract_standard_device(self, sentence):
        #res = [{"device_name":"", "position":(0,10), "standard_device_name":""}]
        res = utils.max_backward_match(sentence, self.device_names, max_k=10)
        res = [{"device_name":elem[0], "position":(elem[1], elem[2]), "standard_device_name":self.device_dict[elem[0]]} for elem in res]
        return res


    #todo:test 两个逻辑能否合并
    def invalid_reference_check(self, sentence):
        #res = [{"reference":"", "position":(0,10)}]
        res = []
        iter = re.finditer("《.*》", sentence)
        for elem in iter:
            res.append((elem.group(0), elem.span()))
        iter = re.finditer("说明书|手册", sentence)
        for elem in iter:
            span = elem.span()
            end_pos = span[0]
            start_pos = 0 if end_pos < 10 else end_pos - 10
            res.append((sentence[start_pos:end_pos] + elem.group(0), (start_pos, span[1])))
        res = [{"reference":elem[0], "position": elem[1]} for elem in res]
        return res

    #todo: threshold read
    #sentences=[{"sentence":"", "document_name":"", "position":(1,2)}]
    def similar_expression(self, sentences):
        #res = [{"sentence":"", "document_name":"", "position":(1,2), "similar_sentences":[{"sentence":"", "document_name":"", "position":(2,3)}]}]
        res = []
        device_dict = dict()
        for i, sentence in enumerate(sentences):
            device_res = utils.max_backward_match(sentence["sentence"], self.device_names, 10)
            for device in device_res:
                standard_device_name = self.device_dict[device[0]]
                if standard_device_name not in device_dict:
                    device_dict[standard_device_name] = set()
                device_dict[standard_device_name].add(i)
        di = dict()
        for device in device_dict:
            pos_list = device_dict[device]
            for i in pos_list:
                di[i] = []
                for j in pos_list:
                    if i != j:
                        sim = utils.similarity(sentences[i]["sentence"], sentences[j]["sentence"])
                        if sim > 0.7:
                            di[i].append(j)
        for i in di:
            pos_list = di[i]
            if len(pos_list) > 0:
                elem_di = sentences[i].copy()
                elem_di["similar_sentences"] = [sentences[j] for j in pos_list]
                res.append(elem_di)
        return res


    #todo:
    def abnormal_number_check(self, sentence):
        scope_pos_list = []
        # pattern = self.scope_words1 + "([^,，。！!/?？；;~～]{1,10}的)?(-?[0-9]+(\.[0-9]+)?)"
        # for case in re.finditer(pattern, sentence):
        #     scope_pos_list.append(case.span())
        # pattern = "(-?[0-9]+(\.[0-9]+)?)" + self.scope_words2
        pattern = "(-?[0-9]+(\.[0-9]+)?)"
        for case in re.finditer(pattern, sentence):
            scope_pos_list.append(case.span())
        return {"positions": scope_pos_list}



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



# det = Detection()

# from node import Node
# tree1 = Node("")
# tree1.children = [Node("A", [Node("A1"), Node("A2")]), Node("B"), Node("C")]
# tree2 = Node("")
# tree2.children = [Node("A"), Node("D", [Node("D1"), Node("D2")])]
# res = det.catalog_check(tree1, tree2)
# print(res)
#
# res = det.extract_standard_device("千分尺和塞尺还有反光镜的用处")
# print(res)
# res = det.extract_standard_device("")
# print(res)
#
# res = det.invalid_reference_check("《关于处分》的")
# print(res)
# res = det.invalid_reference_check("《关于处分》说明书")
# print(res)
#
# res = det.similar_expression(sentences=[{"sentence":"反光镜的长度是1-5cm", "document_name":"反光镜", "position":(1,2)},
#                                         {"sentence":"活动光镜的长度是1-4cm", "document_name":"反光镜", "position":(2,2)}])
# print(res)
# res = det.similar_expression(sentences=[{"sentence":"反光镜的长度是1-5cm", "document_name":"反光镜", "position":(1,2)},
#                                         {"sentence":"活动光镜ewfrwerer的长度是1-4cm", "document_name":"反光镜", "position":(2,2)},
#                                         {"sentence":"反光镜的长werkwekrk度是2-5cm", "document_name":"hde", "position":(1,2)}])
# print(res)
#
# res = det.abnormal_number_check("-0.7~3.5之间吧")
# print(res)
# res = det.abnormal_number_check("0..9")
# print(res)
#
# res = det.detection_check("检查确保镜子有无渗透")
# print(res)
# res = det.detection_check("检查确保镜子有无我二位金融界")
# print(res)
























