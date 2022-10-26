import pandas as pd
import inspect
import json
import os
import re
import shutil
from collections import defaultdict


def get__function_name():
    '''获取正在运行函数(或方法)名称'''
    return inspect.stack()[1][3]


def get__lineno():
    '''获取运行代码行数'''
    return inspect.stack()[1][2]


def generateItemPaths(itemPaths_dir):
    paths = {}

    def travesalDir(rootdir, paths):
        pattern = re.compile(r'\d+\.\w+')
        for item in os.listdir(rootdir):
            if not pattern.match(item):
                # print(get__lineno(), False, item)
                continue

            print(get__lineno(), True, item)
            num, name = re.split(r'\.', item, maxsplit=1)
            itemLink = os.path.join(rootdir, item)
            # print(get__lineno(), itemLink)

            # 将后缀.md去掉,作为字典键使用
            name = name.replace('.md', '')

            mdLink = itemLink[6:]
            # 转换os.path.join的路径拼接斜线
            mdLink = mdLink.replace('\\', '/')
            # 转换为md的链接格式[]()
            mdLink = f'[{name}]({mdLink})'

            paths[name] = mdLink
            print(get__lineno(), mdLink)

            if os.path.isdir(itemLink):
                print(get__lineno(), itemLink)
                travesalDir(itemLink, paths)
    travesalDir('./docs/', paths)

    with open(itemPaths_dir, 'w', encoding='utf-8') as f:
        json.dump(paths, f, ensure_ascii=False)


def readInfoData(filePath, sheetName, outPath):
    '''
        读取补充知识点清单,转化为json格式记录,每个知识点一个记录,key值是[名称],[说明]
    '''

    infoData1 = pd.read_excel(filePath, sheet_name=sheetName,
                              header=1, usecols=[1, 2])

    # TODO: 筛选方式待完善 把名称列的非空数据筛选出来
    # infoData2 = infoData1[infoData1['名称'].isna() * 1 == 0]
    infoData2 = infoData1.dropna()

    infoDict1 = infoData2.to_dict(orient='split')
    infoList1 = infoDict1['data']
    infoD = {x[0]: x[1] for x in infoList1}
    with open(outPath, mode='w', encoding='utf-8') as f:
        json.dump(infoD, f, ensure_ascii=False)


def readGuochengData(filePath, sheetName, outPath):
    '''
        读取过程域数据
    '''

    if 1:
        infoData1 = pd.read_excel(filePath, sheet_name=sheetName,
                                  header=1)

    # TODO: 筛选方式待完善 把名称列的非空数据筛选出来
    # infoData2 = infoData1[infoData1['名称'].isna() * 1 == 0]
    infoData2 = infoData1.fillna('')

    # 读出记录列表,列表中是一个个字典,后续可直接转化为json对象.此处也可以pandas.to_json直接转化为json
    infoDict1 = infoData2.to_dict(orient='records')
    # infoList1 = infoDict1['data']
    # infoD = {x[0]: x[1] for x in infoList1}
    with open(outPath, mode='w', encoding='utf-8') as f:
        json.dump(infoDict1, f, ensure_ascii=False)


def createTipsMD(jsonFile, outPath):
    pass


def generateMD1(jsonFile, outPath):
    with open(jsonFile, 'r', encoding='utf-8') as f:
        infoDict = json.load(f)

    shutil.rmtree(outPath)
    os.mkdir(outPath)
    index = 1
    for key, val in infoDict.items():
        print(key, val)
        # count -= 1
        with open(f'{outPath}{index:03d}.{key}.md', 'w', encoding='utf-8') as f:
            content = '## ' + key + '\n- '
            val = val.replace('\n', '\n- ')
            content += val
            print(content)
            f.write(content)
        index += 1


def generateInfoDataMDFile():

    # 生成补充知识点信息json
    if 1:
        filePath = './十大领域笔记（ITTO反向查询+论文框架+临考清单）20220901.xlsx'
        sheetName = '补充知识点清单'
        outPath = './docs/.vuepress/public/data/infoData.json'
        readInfoData(filePath, sheetName, outPath)

    # 生成补充知识点md文件
    if 1:
        jsonFile = './docs/.vuepress/public/data/infoData.json'
        outPath = './docs/02.ITTO点/03.其他/'

        generateMD1(jsonFile, outPath)


def generateToolsMDFile():
    pass

    # 生成工具信息toolsData.json
    if 1:
        filePath = './十大领域笔记（ITTO反向查询+论文框架+临考清单）20220901.xlsx'
        sheetName = '工具清单'
        outPath = './docs/.vuepress/public/data/toolsData.json'
        readInfoData(filePath, sheetName, outPath)

    # 生成工具知识点md文件
    if 1:
        jsonFile = './docs/.vuepress/public/data/toolsData.json'
        outPath = './docs/02.ITTO点/02.TT/'

        generateMD1(jsonFile, outPath)


def generateIOMDFile():

    # 生产io信息ioData.json
    if 1:
        filePath = './十大领域笔记（ITTO反向查询+论文框架+临考清单）20220901.xlsx'
        sheetName = '输入输出清单'
        outPath = './docs/.vuepress/public/data/ioData.json'
        readInfoData(filePath, sheetName, outPath)

    # 生成io知识点md文件
    if 1:
        jsonFile = './docs/.vuepress/public/data/ioData.json'
        outPath = './docs/02.ITTO点/01.IO/'
        generateMD1(jsonFile, outPath)


def createGuochengMDString(item, itemPaths):

    guochengField = item['过程']

    def transformToMDList(item输入):
        '''
            生成ITTO的清单,以及跳转链接
        '''
        print(get__lineno(), ':\n', item输入)
        stringList = item输入.split()
        stringList1 = [
            f'- {item}: {itemPaths.get(item, "")}' for item in stringList]
        resultAddString = '\n'.join(stringList1)
        return resultAddString

    resultString = f'''
## {guochengField}
### 过程定义:
- {item['过程定义']}
### 过程作用:
{transformToMDList(item['过程作用'])}
### 输入:
{transformToMDList(item['输入'])}
### 输出:
{transformToMDList(item['输出'])}
### 工具:
{transformToMDList(item['工具'])}
### 补充知识点
{transformToMDList(item['补充知识点'])}

'''
    return resultString


def generateGuochengMDFile():

    # 生成guochengData.json
    # 调用函数与ITTO的不一样,主表内容比较复杂
    if 0:
        filePath = './十大领域笔记（ITTO反向查询+论文框架+临考清单）20220901.xlsx'
        sheetName = '总表'
        outPath = './docs/.vuepress/public/data/guochengData.json'
        readGuochengData(filePath, sheetName, outPath)

    # 生产过程域md文件
    if 1:
        jsonFile = './docs/.vuepress/public/data/guochengData.json'
        outPath = './docs/01.过程域/'
        with open(jsonFile, 'r', encoding='utf-8') as f:
            infoData = json.load(f)

        itemPaths_dir = './docs/.vuepress/public/data/itemPaths.json'
        if not os.path.exists(itemPaths_dir):
            generateItemPaths(itemPaths_dir)
        with open(itemPaths_dir, 'r', encoding='utf-8') as fp:
            itemPaths = json.loads(fp.read())

        countDict = defaultdict(int)
        lingyuList = []

        shutil.rmtree(outPath)
        os.mkdir(outPath)
        for item in infoData:
            # print(item['十大领域'])

            # 十大子过程文件夹命名增加序号
            lingyu = item['十大领域']
            if lingyu not in lingyuList:
                lingyuList.append(lingyu)
            guochengOfTen = f'{len(lingyuList):02d}.{item["十大领域"]}'
            countDict[guochengOfTen] += 1
            if not os.path.exists(os.path.join(outPath, guochengOfTen)):
                os.mkdir(os.path.join(outPath, guochengOfTen))

            guochengField = item['过程']
            guochengFieldFileName = f'{countDict[guochengOfTen]:02d}.{guochengField}.md'
            # print(guochengFieldFileName)
            guochengFieldPath = os.path.join(
                outPath, guochengOfTen, guochengFieldFileName)
            # print(guochengFieldPath)
            with open(guochengFieldPath, 'w', encoding='utf-8') as f:
                contentString = createGuochengMDString(
                    item, itemPaths)
                f.write(contentString)

        print(countDict)


if __name__ == '__main__':
    # 读取excel文件,并生成补充知识点md文件
    # generateInfoDataMDFile()

    # 读取excel文件,并生成工具知识点md文件
    # generateToolsMDFile()

    # 读取excel文件,并生成IO知识点md文件
    # generateIOMDFile()

    generateGuochengMDFile()
