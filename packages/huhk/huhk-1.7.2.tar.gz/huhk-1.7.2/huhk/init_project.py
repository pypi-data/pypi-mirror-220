import json
import os.path
import re
import sys
import requests
import time

from huhk.case_project.project_base import ProjectBase
from huhk.unit_fun import FunBase
from huhk import projects_path


class GetApi(ProjectBase):
    def __init__(self, name=None, app_key=None, yapi_url=None, yapi_token=None, yapi_json_file=None, swagger_url=None):
        """
        """
        super().__init__(name, app_key, yapi_url, yapi_token, yapi_json_file, swagger_url)
        self.get_project()

    def create_or_update_project(self, _update=False):
        """
        创建项目
        """
        # 创建项目目录
        self.set_file_path()
        # 获取已维护api方法接口列表
        self.get_this_fun_list()
        # 获取接口文档api接口列表
        self.get_api_list()
        # 添加api封装方法
        self.write_fun(_update=_update)

    def set_file_path(self):
        """创建项目框架"""
        FunBase.mkdir_file(self.path.values(), is_py=True)
        if not os.path.exists(os.path.join(self.path.service_dir, "__init__.py")):
            FunBase.write_file(os.path.join(self.path.service_dir, "__init__.py"), value=self.get_init_value())
        if not os.path.exists(os.path.join(self.path.service_dir, f"{self.name}_fun.py")):
            FunBase.write_file(os.path.join(self.path.service_dir, f"{self.name}_fun.py"), value=self.get_fun_value())

    def get_api_fun_list(self):
        """获取已维护方法列表，无则创建demo文件"""
        self.path.fun_file_path = os.path.join(self.path.service_dir, self.name + "_fun.py")
        if os.path.exists(self.path.fun_file_path):
            self.fun_file_str = FunBase.read_file(self.path.fun_file_path)
        else:
            self.fun_file_str = "import requests\n\nfrom huhk.unit_fun import FunBase\n" \
                                "from huhk import admin_host\n\n\nclass %sFun(FunBase):\n" \
                                "    def __init__(self):\n        super().__init__()\n        self.res = None\n\n" \
                                "    def run_mysql(self, sql_str):\n" \
                                "        # id是后台http://47.96.124.102/admin 项目数据库链接的id\n" \
                                '        out = requests.post(admin_host + "/sql/running_sql/", ' \
                                'json={"id": 1, "sql_str": sql_str}).json()\n' \
                                '        if out.get("code") == "0000":\n' \
                                '            return out.get("data")\n        else:\n' \
                                '            assert False, sql_str + str(out.get("msg"))\n\n\n' \
                                "if __name__ == '__main__':\n    f = %sFun()\n" \
                                '    out = f.run_mysql("SELECT * FROM `t_accept_log`  LIMIT 1;")\n' \
                                '    print(out)\n\n' % (self.name2, self.name2)
        self.fun_init_str = re.findall(r"(def +[\d\D]*?\n)\s*def", self.fun_file_str)[0]
        self.fun_init_list = [i.split('=')[0].strip()[5:] for i in self.fun_init_str.split('\n') if "=" in i]

        self.path.sql_file_path = os.path.join(self.path.service_dir, self.name + "_sql.py")
        if os.path.exists(self.path.sql_file_path):
            self.sql_file_str = FunBase.read_file(self.path.sql_file_path)
        else:
            self.sql_file_str = "from service.%s.%s_fun import %sFun\n\n\n" % (self.name, self.name, self.name2)
            self.sql_file_str += "class %sSql(%sFun):\n\n\n" \
                                 "if __name__ == '__main__':\n    s = %sSql()\n\n" % (
                                     self.name2, self.name2, self.name2)
        self.sql_fun_list = re.findall("    def +(.*)?\(", self.sql_file_str)

        self.path.assert_file_path = os.path.join(self.path.service_dir, self.name + "_assert.py")
        if os.path.exists(self.path.assert_file_path):
            self.assert_file_str = FunBase.read_file(self.path.assert_file_path)
        else:
            self.assert_file_str = "import allure\n\nfrom service.%s.%s_sql import %sSql\n\n\n" % (
            self.name, self.name, self.name2)
            self.assert_file_str += "class %sAssert(%sSql):\n\n\n" \
                                    "if __name__ == '__main__':\n    s = %sAssert()\n\n" % (
                                        self.name2, self.name2, self.name2)
        self.assert_fun_list = re.findall("    def +(.*)?\(", self.assert_file_str)

        self.path.api_fun_file_path = os.path.join(self.path.service_dir, self.name + "_api_fun.py")
        if os.path.exists(self.path.api_fun_file_path):
            self.api_fun_file_str = FunBase.read_file(self.path.api_fun_file_path)
        else:
            self.api_fun_file_str = "from service.%s.%s_assert import %sAssert\n" % (self.name, self.name, self.name2)
            self.api_fun_file_str += "from service.%s import %s_api\n\nimport allure\n" % (self.name, self.name)
            self.api_fun_file_str += "\n\nclass %sApiFun(%sAssert):\n\n" \
                                     "if __name__ == '__main__':\n    s = %sApiFun()\n\n" % (
                                         self.name2, self.name2, self.name2)
        self.api_fun_fun_list = re.findall("    def +(.*)?\(", self.api_fun_file_str)

        self.path.api_testcase_file_path = os.path.join(self.path.testcase_dir, "test_api.py")
        if os.path.exists(self.path.api_testcase_file_path):
            self.api_testcase_file_str = FunBase.read_file(self.path.api_testcase_file_path)
        else:
            self.api_testcase_file_str = "import pytest\nimport allure\n\n" \
                                         "from service.%s.%s_api_fun import %sApiFun\n\n\n" % (
                                             self.name, self.name, self.name2)
            self.api_testcase_file_str += '@allure.epic("针对单api的测试")\n@allure.feature("场景：")\nclass TestApi:\n' \
                                          '    def setup(self):\n        self.f = %sApiFun()\n\n' % self.name2
        self.api_testcase_list = re.findall("    def +test_(.*)?\(", self.api_testcase_file_str)

    def get_api_list(self):
        """根据api文档不同方式生成api文件"""
        if self.swagger_url:
            self.get_list_menu_swagger()
        elif self.yapi_url and self.yapi_token:
            self.get_list_menu()
        elif self.yapi_file_str or self.yapi_json_file:
            self.get_list_json()

    def write_fun(self, _update=False):
        if not self.this_fun_list.api and not self.api_list:
            self.api_list += [{'method': 'GET', 'title': '示例-get', 'path': '/demo/get', 'up_time': 1675665418},
                              {'method': 'POST', 'title': '示例-post', 'path': '/demo/post', 'up_time': 1675665418}]
        for row in self.api_list:
            self.write_api(row)
        for fun_name in self.this_fun_list.api.keys():
            self.write_sql(fun_name, _update=_update)
            self.write_assert(fun_name, _update=_update)
            self.write_api_fun(fun_name, _update=True)

    def write_api_fun2(self):
        for row in self.api_list:
            fun_name = self.get_fun_name(row.get('path'))
            if fun_name in self.api_list_old:
                ord_str = re.findall(r'(def %s\(.+\)[\w\W]*?)(def|$)' % fun_name, self.api_file_str)
                up_time = re.findall(r'up_time=(\d+)([\w\W]+)', ord_str[0][0])
                if up_time and int(up_time[0][0]) < row.get('up_time'):
                    new_str = self.get_api_fun_str(fun_name, row)
                    self.api_file_str = self.api_file_str.replace(ord_str[0][0], new_str)
            else:
                self.api_list_old.append(fun_name)
                self.api_file_str += self.get_api_fun_str(fun_name, row)
        if not self.api_list_old:
            self.api_list_old.append("demo")
            self.api_file_str += """@allure.step(title="调接口：/demo")\ndef demo(mobile=None, headers=None, **kwargs):
    \"""\n    发送手机验证码\n    up_time=1657087679\n\n    params: mobile :  : 用户电话号码
    params: headers : 请求\n    ====================返回======================
    params: code : number : \n    params: msg : string : \n    params: data : null : 
    \"""\n    _method = "GET"\n    _url = "/common/common/sendSmsCode"\n
    _headers = {\n        "Content-Type": "application/x-www-form-urlencoded",\n    }
    _headers.update({"headers": headers})\n\n    _data = {\n        "mobile": mobile,  # 用户电话号码\n    }\n
    _params = {\n    }\n
    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)\n\n"""
        for fun_name in self.api_list_old:
            if fun_name not in self.api_fun_fun_list:
                self.api_fun_fun_list.append(fun_name)
                self.get_api_fun_fun_str(fun_name)
        for fun_name in self.api_fun_fun_list:
            if "assert_" + fun_name not in self.assert_fun_list and "self.assert_" + fun_name + '(' in self.api_fun_file_str:
                self.assert_fun_list.append("assert_" + fun_name)
                self.get_assert_fun_str(fun_name)
        for fun_name in self.assert_fun_list:
            fun_name = fun_name[7:]
            if "sql_" + fun_name not in self.sql_fun_list and "self.sql_" + fun_name + '(' in self.assert_file_str:
                self.sql_fun_list.append("sql_" + fun_name)
                self.get_sql_fun_str(fun_name)
        for fun_name in self.api_fun_fun_list:
            if fun_name not in self.api_testcase_list:
                self.api_testcase_list.append("test_" + fun_name)
                self.get_api_testcase_str(fun_name)

        FunBase.write_file(self.path.api_file_path, self.api_file_str)
        FunBase.write_file(self.path.fun_file_path, self.fun_file_str)
        FunBase.write_file(self.path.sql_file_path, self.sql_file_str)
        FunBase.write_file(self.path.assert_file_path, self.assert_file_str)
        FunBase.write_file(self.path.api_fun_file_path, self.api_fun_file_str)
        FunBase.write_file(self.path.api_testcase_file_path, self.api_testcase_file_str)


    def get_api_testcase_str(self, fun_name):
        api_fun_str = re.findall(r'(def %s\(.+\)[\w\W]*?)(def |$)' % fun_name, self.api_file_str)
        if api_fun_str:
            api_fun_str = api_fun_str[0][0]
        else:
            return False
        desc = re.findall(r'"""([\w\W]*)"""', api_fun_str)
        api_testcase_str = '    @pytest.mark.skip("待维护")\n'
        if desc:
            desc = desc[0].split('====================返回======================')[0]
            desc_list = [" " * 8 + i.strip() for i in desc.split('\n') if "up_time=" not in i and i.strip()
                         and "params: headers" not in i]
            api_testcase_str += '    @allure.step(title="%s")\n' % (
                desc_list[0].strip() if desc_list else "")
        api_testcase_str += '    def test_%s(self):\n        self.f.%s()\n\n\n' % (fun_name, fun_name)
        self.api_testcase_file_str += api_testcase_str

    # def get_assert_fun_str(self, fun_name):
    #     data = re.findall(r'def %s\((.*)?\)' % fun_name, self.api_fun_file_str)[0]
    #     data_list = [i.split('=')[0].strip() for i in data.split(',') if len(i.split('=')) > 1
    #                  and i.strip()[0] != '_' and i.split('=')[0].strip() != "headers"]
    #     assert_fun_str = '    @allure.step(title="接口返回结果校验")\n    def assert_%s(self, **kwargs):\n' \
    #                      '        assert self.res.rsp.code in (0, 200), self.res.rsp.msg\n' \
    #                      '        # out = self.sql_%s(**kwargs)\n' % (fun_name, fun_name)
    #     assert_fun_str += '        # flag = self.compare_json_list(self.res, out, [%s])\n' % \
    #                       ', '.join(['"%s"' % i for i in data_list if i not in self.page_and_size])
    #     assert_fun_str += '        assert True, "数据比较不一致"\n\n'
    #     assert_file_str_tmp = re.split(r"(\nif __name__ == '__main__':)", self.assert_file_str)
    #     assert_file_str_tmp.insert(1, assert_fun_str)
    #     self.assert_file_str = "".join(assert_file_str_tmp)

    def sub_hz(self, _id, _str):
        if re.findall(r'[^\da-zA-Z_\ (=,*):]', re.findall(r"def .*?\):", _str)[0]):
            api = self.get_api(_id)
            tmp2 = api.get('data', {}).get('req_params', [])
            for tmp3 in tmp2:
                name = tmp3.get('name', "")
                desc = tmp3.get('desc', "")
                if re.findall(r'[^\da-zA-Z_\ (=,*):]', name) and not re.findall(r'\W', desc):
                    _str = _str.replace(name, desc)
        if re.findall(r'[( ]async[,=)]', _str):
            for tmp in re.findall(r'[( ]async[,=)]', _str):
                tmp1 = str(tmp).replace('async', 'async1')
                _str = _str.replace(tmp, tmp1)
        return _str



if __name__ == '__main__':
    ga = GetApi(app_key="a63ca17b-3cf3-46cb-b8b6-9ad20518e1e1")
    ga.set_file_path()