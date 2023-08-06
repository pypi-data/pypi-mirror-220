import re
import Levenshtein


def _traverse_tree(root, li, current_path):
    if root is None:
        return
    li.append(current_path)
    for child in root.children:
        cp = current_path + "/" + child.val
        _traverse_tree(child, li, cp)


def check_tree_diff(tree1, tree2):
    all_catlog1 = []
    all_catlog2 = []
    _traverse_tree(tree1, all_catlog1, "")
    _traverse_tree(tree2, all_catlog2, "")
    mark1 = [True for i in range(len(all_catlog1))]
    mark2 = [True for i in range(len(all_catlog2))]
    for i, c1 in enumerate(all_catlog1):
        for j, c2 in enumerate(all_catlog2):
            if c2 == c1 and mark2[j]:
                mark1[i] = False
                mark2[j] = False
                break
    rest1, rest2 = [], []
    for m1, c1 in zip(mark1, all_catlog1):
        if m1:
            rest1.append(c1)
    for m2, c2 in zip(mark2, all_catlog2):
        if m2:
            rest2.append(c2)
    return rest1, rest2


def max_backward_match(word_list, vocab, max_k=10):
    res = []
    end = len(word_list)
    while end > 0:
        break_flag = False
        for i in range(max_k):
            start = end - max_k + i
            start = start if start >= 0 else 0
            temp = "".join(word_list[start:end])
            if temp in vocab:
                res.append([temp, start, end])
                end = start
                break_flag = True
                break
        if not break_flag:
            end -= 1
    res.reverse()
    return res


def similarity(s1, s2):
    return Levenshtein.ratio(s1, s2)


def read_words(filename):
    words = set()
    with open(filename, "r") as f:
        for line in f:
            words.add(line.strip())
    return words


def read_scope_words(filename):
    di = dict()
    words = read_words(filename)
    for word in words:
        parts = re.split("\s+", word.strip())
        if len(parts) != 2:
            continue
        if parts[1] not in di:
            di[parts[1]] = []
        di[parts[1]].append(parts[0])
    return di
























