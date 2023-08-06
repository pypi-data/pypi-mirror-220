from huhk import projects_path, admin_host
from huhk.unit_dict import Dict


class ProjectInIt:
    def __init__(self, name=None, app_key=None, yapi_url=None, yapi_token=None, yapi_json_file=None, swagger_url=None):
        """api_type: 0时，value是swagger的api，json的url
                     1时，value值为yapi项目token,
                     2时，value是yapi下载的json文件名，文件放在file目录下,
                     3时，value是yapi的yapi-swagger.json
           name:项目名称，空时默认当前py文件所在文件名上级目录
        """
        self.path = Dict()
        self.path.dir = projects_path
        self.app_key = app_key
        self.name = name
        self.yapi_url = yapi_url
        self.yapi_token = yapi_token
        self.yapi_json_file = yapi_json_file
        self.swagger_url = swagger_url
        self.url = admin_host
        self.yapi_file_str = None
        self.size_names = ("pagesize", "size", "limit")
        self.page_names = ("pageNum", "current", "currentpage")
        self.before = ("before", "start")
        self.end = ("end", )
        self.page_and_size = self.size_names + self.page_names


        self.api_testcase_list = []
        self.api_testcase_file_str = ""
        self.sql_fun_list = None
        self.name2 = None
        self.api_fun_fun_list = None
        self.api_fun_file_str = None
        self.assert_fun_list = None
        self.assert_file_str = None
        self.sql_file_str = None
        self.sql_file_str = None
        self.fun_init_list = None
        self.fun_init_str = None
        self.fun_file_str = None
        self.api_file_str = ""

        self.yapi_url = yapi_url
        self.api_type = None
        self.app_key = app_key
        self.name = name
        self.name2 = name
        self.api_list_old = []
        self.api_list = Dict()
        self.error = ""
        self.this_file_list = Dict({"api": [], "fun": [], "assert": [], "sql": []})
        self.this_fun_list = Dict()
        self.this_api_fun = Dict()
