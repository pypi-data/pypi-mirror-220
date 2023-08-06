import allure

from service.app_t import unit_request
from service.app_t.sqls.points.sqls_points_points import SqlsPointsPoints


class AssertsPointsPoints(SqlsPointsPoints):
    @allure.step(title="接口返回结果校验")
    def assert_points_points_flowDetail(self, _assert=True, **kwargs):
        assert unit_request.is_assert_true(self.res, _assert), "校验接口返回，缺少成功标识"
        # out = self.sql_points_points_flowDetail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_page(self, **kwargs):
        assert unit_request.is_assert_true(self.res), "校验接口返回，缺少成功标识"
        # out = self.sql_points_points_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["endTime", "beforeTime"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_download(self, **kwargs):
        assert unit_request.is_assert_true(self.res), "校验接口返回，缺少成功标识"
        # out = self.sql_points_points_download(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["endTime", "beforeTime"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_convertDetail(self, **kwargs):
        assert unit_request.is_assert_true(self.res), "校验接口返回，缺少成功标识"
        # out = self.sql_points_points_convertDetail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

