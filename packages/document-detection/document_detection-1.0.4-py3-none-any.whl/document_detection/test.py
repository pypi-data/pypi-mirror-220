from detection import Detection

det = Detection()

from node import Node
tree1 = Node("", [Node("A", [Node("A1"), Node("A2", [Node("C")])]), Node("B"), Node("C")])
tree2 = Node("", [Node("A"), Node("D", [Node("D1"), Node("D2", [Node("D3")])])])
res = det.catalog_check(tree1, tree2)
print(res)

cd = {"千分尺":["千分尺", "塞尺"], "反光镜":["活动光镜"]}
res = det.extract_standard_device("千分尺和塞尺还有反光镜的用处", cd)
print(res)

res = det.extract_standard_device("塞尺镜子", dict())
print(res)

res = det.invalid_reference_check("《关于处分》的")
print(res)
res = det.invalid_reference_check("《处分》说明书")
print(res)
res = det.invalid_reference_check("玩儿《erwer》为而为")
print(res)

res = det.similar_expression(sentences=[{"sentence":"反光镜的长度是1-5cm", "document_name":"反光镜", "position":(1,2)},
                                        {"sentence":"活动光镜的长度是1-4cm", "document_name":"反光镜", "position":(2,2)}], check_dict=cd)
print(res)
res = det.similar_expression(sentences=[{"sentence":"反光镜的长度是1-5cm", "document_name":"反光镜", "position":(1,2)},
                                        {"sentence":"活动光镜ewfrwerer的长度是1-4cm", "document_name":"反光镜", "position":(2,2)},
                                        {"sentence":"反光镜的长werkwekrk度是2-5cm", "document_name":"hde", "position":(1,2)}], check_dict=cd)
print(res)


res = det.abnormal_number_check("-0.7~3.5之间吧")
print(res)
res = det.abnormal_number_check("0..9月")
print(res)

res = det.detection_check("检查确保镜子有无渗透")
print(res)
res = det.detection_check("检查确保镜子有无我二位金融界")
print(res)