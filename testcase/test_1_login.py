#coding=utf-8
import ast
import json
from pprint import pprint
from public import mytest
from ddt import ddt,data,unpack
from loguru import logger
from public.send_request import SendRequest
from public.data_info import get_test_case_data, data_info, write_res

@ddt
class Login(mytest.MyTest):
    """登录模块"""

    @data(*get_test_case_data(data_info, 'login'))
    def test_login(self, data):
        "登录接口"
        r = self.send_requests.send_request_all(data)
        assert_info = data['assert_info']
        self.assertEqual(r['code'], assert_info['code'])
        self.assertEqual(r['msg'], assert_info['msg'])







