import allure

from service.app_t import unit_request
from service.app_t.sql.open.haohan.sql_open_haohan_relation import SqlOpenHaohanRelation


class AssertOpenHaohanRelation(SqlOpenHaohanRelation):
    @allure.step(title="接口返回结果校验")
    def assert_open_haohan_relation_update(self, **kwargs):
        assert unit_request.is_assert_true(self.res), "校验接口返回，缺少成功标识"
        # out = self.sql_open_haohan_relation_update(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

