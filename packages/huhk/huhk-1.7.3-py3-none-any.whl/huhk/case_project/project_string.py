import json
import os
import re

import requests

from huhk.case_project.project_init import ProjectInIt
from huhk.unit_dict import Dict


class ProjectString(ProjectInIt):
    def _get_description(self, req_body_other):
        try:
            if not req_body_other:
                return []
            elif isinstance(req_body_other, str):
                properties = json.loads(req_body_other).get('properties') or {}
            elif isinstance(req_body_other, list):
                return req_body_other
            else:
                properties = req_body_other.get('properties') if req_body_other.get('properties') else req_body_other
            _list = []
            for k, v in properties.items():
                if type(v) == dict:
                    _properties = self._get_description(v.get('properties')) if v.get('properties') else None
                    _items = self._get_description(v.get('items')) if v.get('items') else None
                    _row = {"name": k,
                            "desc": v.get('description', ""),
                            "type": v.get('type', ""),
                            "properties": _properties,
                            "items": _items}
                else:
                    _row = {"name": k,
                            "desc": None,
                            "type": v,
                            "properties": None,
                            "items": None}
                _list.append(_row)
            return _list
        except Exception as e:
            print(e)

    def get_init_value(self):
        """
            生成项目__init__.py文件
        """
        value = 'from huhk.init_project import GetApi\n'
        value += 'from huhk.unit_request import UnitRequest\n\n\n'
        value += 'class Request(UnitRequest):\n    pass\n\n\n'
        value += f'APP_KEY = "{self.app_key}"\n\n\n' if self.app_key else ""
        value += 'unit_request = Request("SIT", APP_KEY)\n'
        value += '# 环境变量\nvariable = unit_request.variable\n'
        value += 'http_requester = unit_request.http_requester\n\n\n'
        value += 'if __name__ == "__main__":\n'
        value += f"    GetApi(name='{self.name}'"
        if self.app_key:
            value += f", app_key=APP_KEY"
        elif self.yapi_url and self.yapi_token:
            value += f", yapi_url='{self.yapi_url}', yapi_token='{self.yapi_token}'"
        elif self.yapi_json_file:
            value += f", yapi_json_file='{self.yapi_json_file}'"
        elif self.swagger_url:
            value += f", swagger_url='{self.swagger_url}'"
        value += ").create_or_update_project()\n"
        return value

    def get_fun_value(self):
        """生成项目基础方法"""
        value = "import requests\n\nfrom huhk.unit_fun import FunBase\n"
        value += "from huhk.unit_dict import Dict\n"
        value += f"from huhk import admin_host\n\n\nclass {self.name2.replace('_', '')}Fun(FunBase):\n"
        value += "    def __init__(self):\n        super().__init__()\n        self.res = None\n"
        value += "        self.output_list = Dict()\n        self.input_value = Dict()\n"
        value += "    @staticmethod\n    def run_mysql( sql_str, db_id=1):\n"
        value += "        # 根据后台数据库配置id查询\n"
        value += '        out = requests.post(admin_host + "/sql/running_sql/", '
        value += 'json={"id": db_id, "sql_str": sql_str}).json()\n'
        value += '        if out.get("code") == "0000":\n'
        value += '            return out.get("data")\n        else:\n'
        value += '            assert False, sql_str + str(out.get("msg"))\n\n\n'
        value += f"if __name__ == '__main__':\n    f = {self.name2.replace('_', '')}Fun()\n"
        value += '    out = f.faker().name()\n'
        value += '    print(out)\n\n'
        return value

    @staticmethod
    def get_params_string(req_all, res_body):
        """方法描述生成"""
        def get_str(l):
            _str = ""
            for p in l:
                _str += f'    params: {p.get("name", "")} : {p.get("type", "")} : {p.get("desc", "")}\n'
                if p.get('properties') or p.get('items'):
                    for p2 in p.get('properties') or p.get('items'):
                        _str += f'              {p2.get("name", "")} : {p2.get("type", "")} : {p2.get("desc", "")}\n'
            return _str

        try:
            api_str = get_str(req_all)
            api_str += "    params: headers : 请求头\n    ====================返回======================\n"
            api_str += get_str(res_body)
            return api_str
        except Exception as e:
            print(e)

    @staticmethod
    def list_add(_list):
        """列表变量叠加"""
        _list3 = []
        _list4 = ["Content-Type"]
        for i in _list:
            name = i.get("name").split("[")[0]
            if name not in _list4:
                _list4.append(name)
                i["name"] = name
                _list3.append(i)
        return _list3

    @staticmethod
    def get_req_json(_list, value=False):
        """"""
        json_str = '{\n'
        for p in _list:
            json_str += f'        "{p.get("name", "")}": ' + (
                '"%s"' % p.get("value", "") if value else p.get("name", "")) + ","
            json_str += ("  # " + p.get("desc").replace('\n', ' ') if p.get("desc") else "") + '\n'
        json_str += '    }'
        return json_str

    @staticmethod
    def get_fun_name(name):
        name = re.sub(r'\W', '_', name.split('{')[0]).strip().lstrip('_')
        return name

    def get_path(self, name, fun_type="apis"):
        name_l = [i for i in name.split('_') if i]
        out = Dict()
        if fun_type == "api" and self.this_fun_list.api[name]:
            filename = self.this_fun_list.api[name].path
            out.path = filename
            out.class_name = None
            out.import_path = ".".join(filename.replace(self.path.dir, "").split(os.sep)[1:])[:-3]
        else:
            filename = f"{fun_type}_{'_'.join(name_l[:-1]) if name_l[:-2] else self.name}.py".replace('__', "_")
            out.path = os.path.join(self.path.service_dir, fun_type, os.path.sep.join(name_l[:-2]), filename)
            out.class_name = filename.split(".")[0].title().replace('_', '')
            out.import_path = ".".join(["service", self.name, fun_type] + name_l[:-2] + [filename.split('.py')[0]])
        return out

    def get_api_header_str(self):
        api_header_str = f"import allure\n\nfrom service.{self.name} import http_requester\n" \
                         f"from huhk.unit_request import get_url\n\n\n"
        return api_header_str

    def get_api_fun_str(self, name, row):
        if self.api_type == 1:
            data = {"token": self.yapi_token, "id": row.get('_id')}
            res = requests.get(self.yapi_url + "/api/interface/get", data=data)
            row = Dict(json.loads(res.text)).get('data')
        api_str = '@allure.step(title="调接口：%s")\n' % row.get("path").split('{')[0]
        api_str += "def " + name + "("
        req_params = row.get('req_params', [])
        req_query = row.get('req_query', [])
        req_body_form = row.get('req_body_form', [])
        req_headers = row.get('req_headers', [])
        req_body = self._get_description(row.get('req_body_other'))
        res_body = self._get_description(row.get('res_body'))
        req_all = self.list_add(req_params + req_query + req_body_form + req_body)
        req_all_data = self.list_add(req_query + req_body_form + req_body)

        api_str += " ".join(set([i.get('name') + '=None,' for i in req_all])) + " headers=None, **kwargs):\n"
        api_str += f'    """\n    {row["title"]}\n    up_time={row["up_time"]}\n\n'
        api_str += self.get_params_string(req_all, res_body)
        api_str += f'    """\n    _method = "{row.get("method")}"\n    _url = "{row.get("path")}"\n'
        if '/{' in row.get("path"):
            api_str += f'    _url = get_url(_url, locals())\n'
        api_str += '\n    _headers = ' + self.get_req_json(req_headers, True)
        api_str += '\n    _headers.update({"headers": headers})\n\n'
        api_str += '    _data = ' + self.get_req_json(req_all_data)
        api_str += '\n\n    _params = ' + self.get_req_json(req_params)
        api_str += '\n\n    return http_requester(_method, _url, params=_params, data=_data, ' \
                   'headers=_headers, **kwargs)\n\n\n'
        return api_str

    def get_sql_header_str(self, class_name):
        header_str = f"from service.{self.name}.{self.name}_fun import {self.name2.replace('_', '')}Fun\n\n\n"
        header_str += f"class {class_name}({self.name2.replace('_', '')}Fun):\n"
        return header_str

    @staticmethod
    def get_sql_fun_str(fun_name):
        sql_fun_str = "    def sql_%s(self, **kwargs):\n" % fun_name
        sql_fun_str += "        # name = self.kwargs_pop(kwargs, 'name')  # 单独处理字段\n"
        sql_fun_str += "        # self.kwargs_replace(kwargs, likes=[], ins=[], before_end=[])  "
        sql_fun_str += "# 模糊查询字段，数组包含查询字段，区间字段处理\n"
        sql_fun_str += '        # kwargs["order_by"] = None  # 排序\n'
        sql_fun_str += '        sql_str = self.get_sql_str("table_name", **kwargs)  # 生成sql语句\n'
        sql_fun_str += '        # out = self.run_mysql(sql_str)  # 执行sql语句\n' \
                       '        # return out\n\n'
        return sql_fun_str

    def get_assert_header_str(self, class_name, sql_path):
        header_str = f"import allure\n\n"
        header_str += f"from service.{self.name} import unit_request\n"
        header_str += f"from {sql_path.import_path} import {sql_path.class_name}\n\n\n"
        header_str += f"class {class_name}({sql_path.class_name}):\n"
        return header_str

    def get_assert_fun_str(self, fun_name):
        assert_fun_str = '    @allure.step(title="接口返回结果校验")\n    def assert_%s(self, _assert=True, **kwargs):\n' \
                         '        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"\n' \
                         '        # out = self.sql_%s(**kwargs)\n' % (fun_name, fun_name)
        assert_fun_str += '        # flag = self.compare_json_list(self.res, out, [%s])\n' % \
                          ', '.join(['"%s"' % i for i in self.this_fun_list.api[fun_name].input
                                     if str(i).lower() not in self.page_and_size])
        assert_fun_str += '        assert True, "数据比较不一致"\n\n'
        return assert_fun_str

    def get_api_fun_header_str(self, fun_name):
        assert_path = self.get_path(fun_name, fun_type='asserts')
        fun_path = self.get_path(fun_name, fun_type='funs')
        api_path = self.get_path(fun_name, fun_type='apis')
        header_str = "import allure\n\n"
        header_str += f"from {assert_path.import_path} import {assert_path.class_name}\n"
        header_str += f"from {api_path.import_path.rsplit('.', 1)[0]} import {api_path.import_path.rsplit('.', 1)[1]}\n\n\n"
        header_str += f"class {fun_path.class_name}({assert_path.class_name}):\n"
        return header_str

    def get_api_fun_fun_str(self, fun_name):
        api_path = self.get_path(fun_name, fun_type='apis')
        api = self.this_fun_list.api[fun_name]
        data_list_tmp = []
        for n in api.input:
            if n in self.size_names:
                data_list_tmp.append(n.strip() + '=10')
            elif n in self.page_names:
                data_list_tmp.append(n.strip() + '=1')
            else:
                data_list_tmp.append(n.strip() + '="$None$"')
        api_fun_fun_str = f"    @allure.step(title=\"{api.title or api.url}\")\n"
        api_fun_fun_str += "    def %s(self, %s, _assert=True, " % (fun_name, ", ".join(data_list_tmp))
        data_list = [n for n in api.input if n not in self.page_and_size and n != 'headers']
        if str(api.method).lower() == "post" and len(data_list) > 2 and not (set(api.input) & set(self.page_and_size)):
            api_fun_fun_str += "_all_is_None=False, "
        api_fun_fun_str += " **kwargs):\n"
        api_fun_fun_str += f"        \"\"\"\n            url={api.url}\n"
        api_fun_fun_str += "".join([" " * 16 + i.strip() + "\n" for i in api.params.split('\n')
                                    if i.strip() and "params: userId" not in i])
        api_fun_fun_str += "        \"\"\"\n"
        if set(api.input) & set(self.page_and_size):
            for n in data_list:
                api_fun_fun_str += "        %s = self.get_list_choice(%s, list_or_dict=None, key=\"%s\")\n" % (n, n, n)
        else:
            for n in data_list:
                api_fun_fun_str += "        %s = self.get_value_choice(%s, list_or_dict=None, key=None" % (n, n)
                api_fun_fun_str += ", _all_is_None=_all_is_None)" if len(data_list) > 2 else ")"
        api_fun_fun_str += '\n' if data_list else ''
        api_fun_fun_str += "        _kwargs = self.get_kwargs(locals())\n"
        api_fun_fun_str += f"        self.res = {api_path.import_path.rsplit('.', 1)[1]}.{fun_name}(**_kwargs)\n\n"
        api_fun_fun_str += "        self.assert_%s(_assert, **_kwargs)\n" % fun_name
        if set(api.input) & set(self.page_and_size):
            api_fun_fun_str += "        self.set_output_value(_kwargs)\n"
        api_fun_fun_str += "        self.set_value(_kwargs)\n\n\n"

        return api_fun_fun_str

