import copy
import collections as col
import random


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


# calculate gamma
def cal_gamma(p, q, element):
    p_partition = partition(element, p)
    q_partition = partition(element, q)
    pos_n = 0
    for i in q_partition:
        temp = 0
        for j in p_partition:
            mark = True
            for k in range(len(j)):
                if j[k] in i:
                    continue
                else:
                    mark = False
                    break
            if mark:
                temp = temp + len(j)
        pos_n = pos_n + temp
    result = pos_n / len(element)
    return result


# attribute reduction using dependence method
def attribute_reduction(c, d, element):
    r = []
    gammaCD = cal_gamma(c, d, element)
    while True:
        t = copy.deepcopy(r)
        index = random.randint(0, len(c))
        x = c[index - 1]
        if x in r:
            continue
        r.append(x)
        if cal_gamma(r, d, element) > cal_gamma(t, d, element):
            t = copy.deepcopy(r)
        r = copy.deepcopy(t)
        gammaRD = cal_gamma(r, d, element)
        if gammaRD == gammaCD:
            break
    r = sorted(r)
    return r


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
    c = [0, 1, 2, 3]
    d = [4]
    index_result = attribute_reduction(c, d, data)
    result = [attribute[i] for i in index_result]
    print('the result of attribute reduction is', result)


if __name__ == '__main__':
    main()
