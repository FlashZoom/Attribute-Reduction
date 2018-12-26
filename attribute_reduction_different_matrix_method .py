import copy
import collections as col
import numpy as np


# use relationship to generate partition
def partition(element, attribute):
    x = copy.deepcopy(element)
    result = []
    for i in range(len(element)):
        if element[i] not in x:
            continue
        temp = [element[i]]
        x.remove(element[i])
        x_temp = copy.deepcopy(x)
        for other in x_temp:
            mark = True
            for j in range(len(attribute)):
                if other[attribute[j]] == element[i][attribute[j]]:
                    continue
                else:
                    mark = False
            if mark:
                temp.append(other)
                x.remove(other)
        result.append(temp)

    return result


# calculate pos
def cal_pos(p, q, element):
    p_partition = partition(element, p)
    q_partition = partition(element, q)
    pos_n = []
    for i in q_partition:
        temp = []
        for j in p_partition:
            mark = True
            for k in range(len(j)):
                if j[k] in i:
                    continue
                else:
                    mark = False
                    break
            if mark:
                temp.extend(j)
        pos_n = pos_n + temp
    index = []
    for i in pos_n:
        index.append(element.index(i))
    index.sort()
    return index


# calculate core
def core(c, d, element):
    result = []
    for i in c:
        b = copy.deepcopy(c)
        b.remove(i)
        if cal_pos(b, d, element) != cal_pos(c, d, element):
            result.append(i)
    return result


def different_matrix(element, c, d):
    result = []
    for i in element:
        for j in element:
            temp = []
            if i[d[0]] != j[d[0]]:
                for k in c:
                    if i[k] != j[k]:
                        temp.append(k)
            if temp:
                result.append(temp)
    result = list(np.unique(result))
    return result


# attribute reduction using different matrix method
def attribute_reduction(c, d, element):
    r = core(c, d, element)
    m = different_matrix(element, c, d)
    while True:
        q = []
        for i in m:
            mark = False
            for j in r:
                if j in i:
                    mark = True
                    break
            if mark:
                q.append(i)
        m = [i for i in m if i not in q]
        SGF = list(np.zeros(len(c), dtype=int))
        for i in m:
            for j in i:
                SGF[j] = SGF[j] + 1
        r.append(SGF.index(max(SGF)))
        if not m:
            break
    r.sort()
    return r


# use equivalence matching method
def rule_extract(attribute, c_reduction, d, element):
    rule = []
    E = partition(element, c_reduction)
    D = partition(element, d)
    for i in E:
        for j in D:
            EY = [k for k in i if k in j]
            cf = len(EY) / len(i)
            if cf >= 1:
                temp = {}
                temp['CF'] = cf
                temp['rule'] = ''
                for k in range(len(c_reduction)):
                    temp['rule'] = temp['rule'] + attribute[c_reduction[k]] + '=' + i[0][c_reduction[k]] + ' '
                temp['rule'] += '-> '
                for k in range(len(d)):
                    temp['rule'] = temp['rule'] + attribute[d[k]] + '=' + i[0][d[k]] + ' '
                rule.append(temp)
    return rule


def main():
    attribute = ['a', 'b', 'c', 'd', 'e']
    element = col.namedtuple('element', attribute)
    x1 = element(a='S', b='R', c='T', d='T', e='R')
    x2 = element(a='R', b='S', c='S', d='S', e='T')
    x3 = element(a='T', b='R', c='R', d='S', e='S')
    x4 = element(a='S', b='S', c='R', d='T', e='T')
    x5 = element(a='S', b='R', c='T', d='R', e='S')
    x6 = element(a='T', b='T', c='R', d='S', e='S')
    x7 = element(a='T', b='S', c='S', d='S', e='T')
    x8 = element(a='R', b='S', c='S', d='R', e='S')
    data = [x1, x2, x3, x4, x5, x6, x7, x8]
    condition_attribute = [0]
    # result = partition(data, condition_attribute)
    test = [0, 1]
    c = [0, 1, 2, 3]
    d = [4]
    index = attribute_reduction(c, d, data)
    result = [attribute[i] for i in index]
    print('The result of attribute reduction is', result)
    rule = rule_extract(attribute, index, d, data)
    print('The decision rule is')
    print(rule)


if __name__ == '__main__':
    main()
