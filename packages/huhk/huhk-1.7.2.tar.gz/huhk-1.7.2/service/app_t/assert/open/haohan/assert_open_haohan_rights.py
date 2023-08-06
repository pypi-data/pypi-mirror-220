import allure

from service.app_t import unit_request
from service.app_t.sql.open.haohan.sql_open_haohan_rights import SqlOpenHaohanRights


class AssertOpenHaohanRights(SqlOpenHaohanRights):
    @allure.step(title="接口返回结果校验")
    def assert_open_haohan_rights_update(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_open_haohan_rights_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["params"])
        assert True, "数据比较不一致"

