# coding=utf-8
import time
import re
import json
import unittest
from loguru import logger
from public.send_request import SendRequest
from config.basic_config import ConfigInit
# from testcase.test_login import Login
from public.data_info import finddata, write_res
class MyTest(unittest.TestCase):

    """
    The base class is for all testcase.
    """
    def setUp(self):
        self.url = ConfigInit.login_url
        self.headers = {}
        self.send_requests = SendRequest(self.url, self.headers)
        logger.info('############################### START ###############################')


    def tearDown(self):
        logger.info('###############################  End  ###############################')


class MyTokenTest(unittest.TestCase):
    """
    The base class is for all testcase.
    """

    @classmethod
    def login_func(cls, account='18175516432', pw='hb123456'):
        """封装登录函数"""
        send_data = {
            "account":account,
            "password":pw,
            "login_type":1 }
        url = ConfigInit.login_url + '/id_v2_5/user/login'
        headers = {'Content-Type': 'application/json'}
        r = SendRequest(url, headers).send_request("post", url=url, data=send_data, header=headers)
        token = r['data']['token']
        user_id = r['data']['basic']['id']
        return token,user_id

    @classmethod
    def setUpClass(cls):
        cls.token, cls.user_id = cls.login_func()

    def setUp(self):
        self.url = ConfigInit.url
        self.headers = {
                        'JK-TOKEN':self.token,
                        'JK-USER-ID': str(self.user_id)
                        }
        self.send_requests = SendRequest(self.url, self.headers)
        logger.info('############################### START ###############################')

    # def send_request(self, data, random_parameters=None):
    #     """
    #     :param data: 从data文件中读取到的对应接口数据
    #     :param random_parameters: 除了从依赖接口获取依赖参数替换外，需要随机生成参数替换时，从这里传
    #     :return: null
    #     """
    #     url = self.url + data['url']
    #     rownum = data['rownum']
    #     method = data['method']
    #     send_data = data['send_data']
    #     keys = data['update_data']  # 获取请求参数需要替换的参数标示列表
    #     if not random_parameters is None:
    #         send_data = self.update_data2(send_data, random_parameters)  # 替换发送的数据
    #     if "rely_num" not in data:
    #         r = SendRequest().send_request(method, url=url, data=send_data, header=self.headers)
    #     else:
    #         rely_num = data['rely_num']  # 依赖接口名称
    #         rely_parameter = data['rely_parameter']  # 依赖接口参数
    #         values = finddata(case_name=rely_num, rely_parameter=rely_parameter)  # 通过依赖接口名称和对应的依赖参数，提取依赖值
    #         if method == 'post':
    #             k_v_list = self.construct_dict(keys, values)  # 组成替换参数字典{"参数标示":"提取到的值"}
    #             send_data = self.update_data2(send_data, [k_v_list])  # 替换发送的数据
    #             r = SendRequest().send_request(method, url=url, data=send_data, header=self.headers)
    #         elif method == 'get':
    #             url = self.replace_str(url, keys[0], values)
    #             r = SendRequest().send_request(method, url=url, data=send_data, header=self.headers)
    #     write_res(rownum, json.dumps(r, indent=2, ensure_ascii=False))  # 写入返回值
    #     assert_info = data['assert_info']
    #     self.assertEqual(r['code'], assert_info['code'])
    #     self.assertEqual(r['msg'], assert_info['msg'])
    #     return r
    #
    # def post_send(self, data):
    #     url = self.url + data['url']
    #     rely_num = data['rely_num']  # 依赖接口名称
    #     rely_parameter = data['rely_parameter']  # 依赖接口参数
    #     keys = data['update_data']  # 获取请求参数需要替换的参数标示列表
    #     values = finddata(case_name=rely_num, rely_parameter=rely_parameter)   # 通过依赖接口名称和对应的依赖参数，提取依赖值
    #     k_v_list = self.construct_dict(keys, values)   #  组成替换参数字典{"参数标示":"提取到的值"}
    #     send_data = data['send_data']
    #     send_data = self.update_data2(send_data, [k_v_list])  # 替换发送的数据
    #     rownum = data['rownum']
    #     r = SendRequest().send_json_post(url=url, dict=send_data, header=self.headers)
    #     write_res(rownum, json.dumps(r, indent=2, ensure_ascii=False))  # 写入返回值
    #     assert_info = data['assert_info']
    #     self.assertEqual(r['code'], assert_info['code'])
    #     self.assertEqual(r['msg'], assert_info['msg'])
    #
    # def get_send(self, data):
    #     rely_num = data['rely_num']  # 依赖接口名称
    #     rely_parameter = data['rely_parameter']  # 依赖接口参数
    #     keys = data['update_data']  # 获取请求参数需要替换的参数标示列表
    #     values = finddata(case_name=rely_num, rely_parameter=rely_parameter)   # 通过依赖接口名称和对应的依赖参数，提取依赖值
    #     url = self.url + self.replace_str(data['url'], keys[0], values)
    #     rownum = data['rownum']
    #     method = data['method']
    #     send_data = data['send_data']
    #     r = SendRequest().send_request(method, url=url, data=send_data, header=self.headers)
    #     write_res(rownum, json.dumps(r, indent=2, ensure_ascii=False))  # 写入返回值
    #     assert_info = data['assert_info']
    #     self.assertEqual(r['code'], assert_info['code'])
    #     self.assertEqual(r['msg'], assert_info['msg'])

    def tearDown(self):
        time.sleep(1)
        logger.info('###############################  End  ###############################')

    # def replace_str(self, url, mark_str, parameters):
    #     """替换url中指定参数
    #     :param url: 替换前url；示例：'/product/list?page=1&size=10&keyword=&industryId=&categoryId=str1'
    #     :param mark_str: 需要替换的字符串标示；示例:url中需要被替换的值都标示为str1，那这个mark_str就是传"str1"，是别的就传别的
    #     :param parameters:  替换的值的集合，按替换顺序传参；示例：["1","12345"]
    #     :return: 结果 替换后真正的请求url
    #     """
    #     if type(url) != str:
    #         logger.debug('url格式错误：{}'.format(url))
    #         return None
    #     if type(parameters) != list:
    #         logger.debug('parameters格式错误：{}'.format(parameters))
    #         return None
    #     for parameter in parameters:
    #         url = url.replace(mark_str, parameter, 1)
    #     return url
    #
    # def replace_dict(self, d, parameter1, parameter2):
    #     #替换字典中指定value
    #     new = {}
    #     for k, v in d.items():
    #         if isinstance(v, dict):
    #             v = self.replace_dict(v, parameter1, parameter2)
    #         if v == parameter1:
    #             new[k] = parameter2
    #         else:
    #             new[k] = v
    #     return new
    #
    # # 精确提取：json.data.name
    # def json_exact_search(self, data, key):
    #     '''
    #     :param data: 嵌套字典、列表；dict、list；示例：{'code':0,'data':[{'name':'a'},{'name':'b'},{'name':'c'}]}
    #     :param key:  查找条件; str ； 示例：'json.data.0.name'
    #     :return: 结果 = a
    #     '''
    #     logger.info('————精确提取：json方式————')
    #     if type(data) != dict:
    #         try:
    #             data = eval(data)
    #         except:
    #             return None
    #     logger.debug('————json方法：精确查找提取-数据源：%s,%s' % (type(data), data))
    #     logger.debug('————json方法：精确查找提取-查找条件：%s,%s' % (type(key), key))
    #     k_list = key.split('.')
    #     k_list.pop(0)
    #     try:
    #         for i in k_list:
    #             try:
    #                 i = int(i)
    #             except:
    #                 i = i
    #             logger.debug('————json方法：精确查找提取-提取条件：%s,%s' % (type(i), i))
    #             logger.debug('————json方法：精确查找提取-提取后数据源：%s,%s' % (type(key), key))
    #             v = data[i]
    #             data = v
    #         logger.debug('————json方法：精确查找-提取值：————%s,%s' % (type(v), v))
    #         return v
    #     except Exception as e:
    #         logger.debug('————json方法：精确查找-错误：————%s' % e)
    #         return None
    #     finally:
    #         logger.debug('————json方法：精确查找-结束————')
    #
    #     # 精确提取：data[][][]
    # def data_exact_search(self, datas, key):
    #     '''
    #     :param data: 嵌套字典、列表；dict、list；示例：{'code':0,'data':[{'name':'a'},{'name':'b'},{'name':'c'}]}
    #     :param key:  查找条件；str；示例："data['data'][0][name]"
    #     :return: 结果 = a
    #     '''
    #     logger.info('————进入精确提取：data方式————')
    #     if type(datas) != dict:
    #         try:
    #             datas = eval(datas)
    #         except:
    #             return None
    #     data = datas
    #     logger.debug('data方法：精确查找提取-数据源：%s,%s' % (type(data), data))
    #     logger.debug('data方法：精确查找提取-查找条件：%s,%s' % (type(key), key))
    #     try:
    #         res = eval(key)
    #         logger.debug('————data方法：精确查找提取-开始查找————%s,%s' % (type(res), str(res)))
    #     except:
    #         res = None
    #         logger.debug('data方法：精确查找提取-查找失败:%s,%s' % (type(res), res))
    #     return res
    #
    # # 参数值替换
    # def update_data2(self, datas, k_v_list):
    #     '''
    #     :param datas:   接口请求数据：请求头、请求参数、请求主体 type = dict
    #     :param k_v_list: 接口替换条件：[{'要替换的参数' : '提取的值'}]
    #     :return: 替换后的接口请求数据，type = dict
    #     '''
    #
    #     if type(datas) != str:
    #         datas = str(datas)
    #     if type(k_v_list) != list:
    #         k_v_list = [k_v_list]
    #     for k_v in k_v_list:
    #
    #         if type(k_v) != dict:
    #             k_v = eval(k_v)
    #
    #         for k, v in k_v.items():
    #             v_type = type(v)
    #             u_k = k
    #             uk_values_len = re.compile("Values_(.*?)").findall(str(u_k))  # 获取关联参数的个数
    #             try:
    #                 k = eval(k)
    #
    #             except:
    #                 k = k
    #
    #             if type(k) in [dict, list]:
    #                 datas = eval(datas)
    #                 for k1, v2 in datas.items():
    #                     print('嵌套替换-K值：%s,%s' % (type(k1), k1))
    #                     print('嵌套替换-value值：%s,%s' % (type(v2), v2))
    #                     print('嵌套替换-替换条件：%s,%s' % (type(k), k))
    #                     print('嵌套替换-替换的值：%s,%s' % (type(v), v))
    #                     # values_len = re.compile("Values_(.*?)").findall(str(v2))  # 获取关联参数的个数
    #                     if type(v2) != type(k):
    #                         v = str(v)
    #                         try:
    #                             v2 = eval(v2)
    #                             v2 = eval(v2)
    #                         except Exception as e:
    #                             logger.error('嵌套替换数据转换失败：%s' % e)
    #
    #                     if (v2) == (k):
    #                         datas[k1] = v
    #
    #                         print('嵌套完成替换：%s,%s' % (type(datas), datas))
    #             else:
    #                 v2 = str(v)
    #                 if type(v) != str:
    #                     k = "'" + k + "'"
    #                 datas = re.sub("%s+(.*?)" % k, v2, datas)
    #
    #     return eval(datas)
    #
    # def construct_dict(self, keys, values):
    #     """传入两个列表，构建成字典"""
    #     dictionary = dict(zip(keys, values))
    #     return dictionary

    @classmethod
    def tearDownClass(cls):
        pass