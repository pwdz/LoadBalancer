import sys
import time
def getNums(fileData):
    numbers = []
    for num in fileData:
        numbers.append(int(num))
    return numbers


def minCalculator(fileData):
    numbers = getNums(fileData)
    return min(numbers)

def maxCalculator(fileData):
    numbers = getNums(fileData)
    return max(numbers)

def averageCalculator(fileData):
    numbers = getNums(fileData)
    return sum(numbers)/len(numbers)

def sortNum(fileData):
    numbers = getNums(fileData)
    return sorted(numbers,reverse=True)

def wordCount(fileData):
    dictionay = {}
    for line in fileData:
        words = line.split()
        for word in words:
            if word not in dictionay.keys():
                dictionay[word] = 1
            else:
                dictionay[word]+=1

    return {k: v for k, v in sorted(dictionay.items(), key=lambda item: item[1], reverse=True)}


def main():
    func = sys.argv[1]
    inputPath = sys.argv[2]
    time.sleep(6)
    fileData = open(inputPath, 'r')
    if func == 'min':
        result = minCalculator(fileData)
        print(result)
    if func == 'max':
        result =  maxCalculator(fileData)
        print(result)
    if func =='average':
        result = averageCalculator(fileData)
        print(result)
    if func =='sort':
        result = sortNum(fileData)
        for i in result:
            print(str(i))

    if func =='wordcount':
        result = wordCount(fileData)
        for key in result.keys():
            print(str(key)+'    '+str(result[key]))


if __name__ == '__main__':
    main()