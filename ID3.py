#利用决策树，预测隐形眼镜类型
import math
# 打开数据集
def dataset(filename):
    fr = open(filename)
    num = len(fr.readline().split('\t'))
    dataMat = []
    for line in fr.readlines():
        lineArr = []
        for i in range(num):
            curArr = line.strip().split('\t')
            lineArr.append(curArr[i])
        dataMat.append(lineArr)
    return dataMat

#计算香农熵
def shannonEnt(dataSet):
    lineNum = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        curlabel = featVec[-1]
        if curlabel not in labelCounts.keys():
            labelCounts[curlabel] = 1
        else:
            labelCounts[curlabel] += 1
    shannonEnt = 0
    for key in labelCounts:
        prob = labelCounts[key]/lineNum
        shannonEnt -= prob * math.log(prob,2)
    return shannonEnt

print(shannonEnt(dataSet))

#按照特征划分数据集, axis是按照第几个属性划分，value是要返回的子集对应的属性值
def splitDataSet(dataSet,axis,value):
    featVec = []
    newDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeat = featVec[: axis]
            reducedFeat.extend(featVec[axis+1 :])
            newDataSet.append(reducedFeat)
    return newDataSet

#选择最佳的划分特征量

def bestSplit(dataSet):
    numFeat = len(dataSet[0]) - 1
    baseEnt = shannonEnt(dataSet)
    bestinfoEnt = 0
    bestFeat = -2
    for i in range(numFeat):
        featList = []
        for j in range(len(dataSet)):
            featList.append(dataSet[j][i])
        uniqueList = set(featList)
        newEnt = 0
        for value in uniqueList:
            newData = splitDataSet(dataSet, i, value)
            prob = float(len(newData))/float(len(dataSet))
            newEnt += prob * shannonEnt(newData)
        infoEnt = baseEnt - newEnt
        if infoEnt > bestinfoEnt :
            bestinfoEnt = infoEnt
            bestFeat = i
    return bestFeat


def majorityCnt(classList):
    classCounts = {}
    for vote in classList:
        if vote not in classCounts.keys():
            classCounts[vote] = 0
            classCounts[vote] += 1
    sortedClassCount = sorted(classCounts.iteritems(),key = operator.itemgetter(1),reverse = True)
    return sortedClassCount[0][0]

# 利用递归构建决策树

def createTree(dataSet,labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet) == 1:
        return majorityCnt(classList)
    bestFeat = bestSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = { bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[beatFeat] for example in dataSet]
    uniqueValues = set(featValues)
    for values in uniqueValues :
        subLabels = labels[:]
        myTree[bestFeatLabel][values] = creatTree(splitDataSet(dataSet,bestFeat,values),subLabels)
    return myTree










