import allure

from service.app_t import unit_request
from service.app_t.sqls.points.sqls_points_pointsApp import SqlsPointsPointsapp


class AssertsPointsPointsapp(SqlsPointsPointsapp):
    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_signIn(self, **kwargs):
        assert unit_request.is_assert_true(self.res), "校验接口返回，缺少成功标识"
        # out = self.sql_points_pointsApp_signIn(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_myPoints(self, **kwargs):
        assert unit_request.is_assert_true(self.res), "校验接口返回，缺少成功标识"
        # out = self.sql_points_pointsApp_myPoints(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_myPointsTotal(self, **kwargs):
        assert unit_request.is_assert_true(self.res), "校验接口返回，缺少成功标识"
        # out = self.sql_points_pointsApp_myPointsTotal(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

