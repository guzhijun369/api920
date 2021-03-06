# coding=utf-8
import json
from public import mytest
from ddt import ddt, data, unpack
from loguru import logger
from public.send_request import SendRequest
from public.data_info import get_test_case_data, data_info, write_res, get_specific_num, finddata
from faker import Faker
import random

fake = Faker("zh_CN")
fake_en = Faker("en_US")


# import json


@ddt
class Project(mytest.MyTokenTest):
    """项目管理模块的接口"""

    @data(*get_test_case_data(data_info, 'add_curriculum'))
    def test_001_add_curriculum(self, data):
        label = fake.word()  # 生成随机课程名称
        name = "脚本修改" + fake.word() + str(random.randint(1, 1000)) + "课程"  # 生成随机Name  # 生成随机课程标签
        objector = fake.word()  # 生成随机目标学员
        income = fake.sentence(nb_words=6, variable_nb_words=True)  # 生成随机学习目标
        intro = fake.sentence(nb_words=6, variable_nb_words=True)  # 生成随机课程综述
        keys = ["num1","num2", "num3", "num4", "num5"]
        values = [label, name, objector, income, intro]

        k_v_list = [self.send_requests.construct_dict(keys, values)]
        r = self.send_requests.send_request_all(data, random_parameters=k_v_list)
        assert_info = data['assert_info']
        self.assertEqual(r['code'], assert_info['code'])
        self.assertEqual(r['msg'], assert_info['msg'])

    @data(*get_test_case_data(data_info, 'get_curriculum_all'))
    def test_002_get_curriculum_all(self, data):
        r = self.send_requests.send_request_all(data)
        assert_info = data['assert_info']
        self.assertEqual(r['code'], assert_info['code'])
        self.assertEqual(r['msg'], assert_info['msg'])

    @data(*get_test_case_data(data_info, 'rm_curriculum'))
    def test_003_rm_curriculum(self, data):
        r = self.send_requests.send_request_all(data)
        assert_info = data['assert_info']
        self.assertEqual(r['code'], assert_info['code'])
        self.assertEqual(r['msg'], assert_info['msg'])

    @data(*get_test_case_data(data_info, 'delete_curriculum'))
    def test_004_delete_curriculum(self, data):
        r = self.send_requests.send_request_all(data)
        assert_info = data['assert_info']
        self.assertEqual(r['code'], assert_info['code'])
        self.assertEqual(r['msg'], assert_info['msg'])

    @data(*get_test_case_data(data_info, 'upload'))
    def test_005_upload(self, data):
        self.headers = None
        url = data['url']
        rely_num = data['rely_num']  # 依赖接口名称
        rely_parameter = data['rely_parameter']  # 依赖接口参数
        keys = data['update_data']
        values = finddata(case_name=rely_num, rely_parameter=rely_parameter)
        k_v_list = self.send_requests.construct_dict(keys, values)
        send_data = data['send_data']
        send_data = self.send_requests.update_data2(send_data, [k_v_list])
        rownum = data['rownum']
        r = self.send_requests.send_file_data(url=url, dict=send_data,
                                         file_name={"file": ("img", open(r"D:/6.png", "rb"), "img/png")})
        write_res(rownum, json.dumps(r, indent=2, ensure_ascii=False))  # 写入返回值
        self.assertTrue('hash' in json.dumps(r, indent=2, ensure_ascii=False))
        self.assertTrue('key' in json.dumps(r, indent=2, ensure_ascii=False))

    @data(*get_test_case_data(data_info, 'form_data_login'))
    def test_006_upload(self, data):
        r = self.send_requests.send_request_all(data)

    @data(*get_test_case_data(data_info, 'application_login'))
    def test_007_application_login(self, data):
        r = self.send_requests.send_request_all(data)
