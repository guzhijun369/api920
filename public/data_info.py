#coding=utf-8
import xlrd,sys
import os
import ast
from config.basic_config import ConfigInit
from config import globalparam
# from pprint import pprint
from xlutils.copy import copy
from loguru import logger
import json
import pandas as pd
from pprint import pprint


# PATH = os.path.join(globalparam.data_path, ConfigInit.data_filename)  # 运行配置
# PATH = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), 'data\\testdata', ConfigInit.data_filename)  # 调试路径
# write_path = os.path.join(globalparam.project_path,'data\\testdata', ConfigInit.data_filename)
# write_path = 'D:\\workhome\\project\\apitest\\public\\data\\testdata\\data.xlsx'
PATH = os.path.join(globalparam.data_path, ConfigInit.data_filename)

# print(PATH)
def get_excel_dict(path, index=0):
    paralList=[]
    workbook=xlrd.open_workbook(path) # 打开文件
    sheet=workbook.sheets()[index]  # sheet索引从0开始
    firstRowDataList=sheet.row_values(0)#第一行数据
    #print firstRowDataList
    for rownum in range(1, sheet.nrows):#循环每一行数据
        list = sheet.row_values(rownum)
        dict={}
        dictTestCaseName={}

        for caseData in list:
            dict['rownum'] = rownum  # 存储当前行数，以便返回数据写入
            dict[firstRowDataList[list.index(caseData)]] =caseData #每一行数据与第一行数据对应转为字典
            #json.dumps(json.loads(caseData), ensure_ascii=False)
        dictTestCaseName[list[0]]=dict#转为字典后与用例名字对应转为字典
        paralList.append(dictTestCaseName)#将处理后的数据放入列表里
    return (paralList)

def get_test_case_data(data_info,testCaseName):
    testData = data_info
    getTestCaseDataList = []
    for data in testData:
        if (list(data.keys())[0]) == testCaseName:
            getTestCaseDatadict = {}
            if 'send_data' in data[testCaseName]:
                if '{' in data[testCaseName]['send_data'] and '}' in data[testCaseName]['send_data']:
                    getTestCaseDatadict['send_data'] = ast.literal_eval(data[testCaseName]['send_data']) # 获取表中的send_data，即接口发送数据
                else:
                    getTestCaseDatadict['send_data'] = data[testCaseName]['send_data']
            else:
                getTestCaseDatadict['send_data'] = None
            getTestCaseDatadict['assert_info'] = ast.literal_eval(data[testCaseName]['assert_info']) # 获取表中的assert_info，即断言数据
            getTestCaseDatadict['method'] = data[testCaseName]['method'] # 获取表中method，即请求方式
            getTestCaseDatadict['url'] = data[testCaseName]['url'].replace('\n', '').replace('\r', '').strip() #  获取表中url
            getTestCaseDatadict['case_name'] = data[testCaseName]['case_name'].replace('\n', '').replace('\r', '').strip() # 获取表中case_name，即用例名称
            getTestCaseDatadict['rownum'] = data[testCaseName]['rownum'] # 获取当前数据行数，以便写入返回值
            if data[testCaseName]['update_data'] != "null":
                update_data = eval(data[testCaseName]['update_data'])
                # for i in eval(data[testCaseName]['update_data']):
                #     update_data.append(i)
                getTestCaseDatadict['update_data'] = update_data
            else:
                getTestCaseDatadict['update_data'] = None
            if data[testCaseName]['rely'].replace('\n', '').replace('\r', '').strip() == 'yes':
                #获取依赖接口的名称
                num_str = data[testCaseName]['num'].split(',')
                getTestCaseDatadict['rely_num'] = num_str
                rely_parameter = eval(data[testCaseName]['rely_parameter'])
                getTestCaseDatadict['rely_parameter'] = rely_parameter
            if 'Content-Type' in data[testCaseName]:
                getTestCaseDatadict['Content-Type'] = data[testCaseName]['Content-Type'].replace('\n', '').replace('\r', '').strip()
            else:
                getTestCaseDatadict['Content-Type'] = None
            getTestCaseDataList.append(getTestCaseDatadict)
    return getTestCaseDataList

def write_res(rownum,data):
    #将接口返回值写入文件，res_data
    oldwb = xlrd.open_workbook(PATH, formatting_info=True)
    newwb = copy(oldwb)
    sheet = newwb.get_sheet(0)
    sheet.write(rownum, 11, data)
    newwb.save(PATH)

def get_specific_num(path=PATH, index=0, num=1):
    #获取文件指定行的res_data(获取返回接口数据)
    workbook = xlrd.open_workbook(path)  # 打开文件
    sheet = workbook.sheets()[index]
    list = sheet.row_values(num)
    data = json.loads(list[11])
    return data

def json_exact_search(data, key):
    '''
    :param data: 嵌套字典、列表；dict、list；示例：{'code':0,'data':[{'name':'a'},{'name':'b'},{'name':'c'}]}
    :param key:  查找条件; str ； 示例：'json.data.0.name'
    :return: 结果 = a
    '''
    logger.info('————精确提取：json方式————')
    if type(data) != dict:
        try:
            data = eval(data)
        except:
            return None
    logger.debug('————json方法：精确查找提取-数据源：%s,%s' % (type(data), data))
    logger.debug('————json方法：精确查找提取-查找条件：%s,%s' % (type(key), key))
    k_list = key.split('.')
    k_list.pop(0)
    try:
        for i in k_list:
            try:
                i = int(i)
            except:
                i = i
            logger.debug('————json方法：精确查找提取-提取条件：%s,%s' % (type(i), i))
            logger.debug('————json方法：精确查找提取-提取后数据源：%s,%s' % (type(key), key))
            v = data[i]
            data = v
        logger.debug('————json方法：精确查找-提取值：————%s,%s' % (type(v), v))
        return v
    except Exception as e:
        logger.debug('————json方法：精确查找-错误：————%s' % e)
        return None
    finally:
        logger.debug('————json方法：精确查找-结束————')

def finddata(path=PATH, case_name=None, rely_parameter=None):
    # 获取文件指定行的res_data(获取返回接口数据),case_name是列表，多个接口返回列表
    '''
    :param path: 文件路径，例如：“D:\\workhome\\project\\apitest\\public\\data\\testdata\\data.xlsx”
    :param case_name: 依赖的接口列表，从文件中的num列读出
    :param rely_parameter: 依赖接口指定参数表达式列表，从文件中rely_parameter列读出
    :return: resdata，列表，按顺序输出取到的所有依赖参数
    '''
    res_data = []
    demo_df=pd.read_excel(path) ##文件路径
    for i in case_name:
        for indexs in demo_df.index:
            if (demo_df.loc[indexs].values[6] == i):  # 表中case_name 列在第七行，固定查找第七行用例名进行匹配，后期优化改成不写死列数
                data = json.loads(demo_df.loc[indexs].values[11])  # 表中res_data 列在第12行，固定查找第12行返回数据进行匹配，后期优化改成不写死列数
                rely_parameter_data = rely_parameter[i].split(',')
                for parameter in rely_parameter_data:
                    v = json_exact_search(data, parameter)
                    # print("key--{} 查找到值为{}".format(parameter,v))
                    res_data.append(v)
    return res_data
# b = {'新建课程': 'json.data.id'}
# c = finddata(case_name=["新建课程"], rely_parameter=b)
# print(c)
data_info = get_excel_dict(PATH)
# a = get_test_case_data(data_info, 'application_login')
# pprint(a)
# get_specific_num(PATH)

