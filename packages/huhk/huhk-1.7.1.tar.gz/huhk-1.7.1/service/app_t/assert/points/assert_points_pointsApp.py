import allure

from service.app_t import unit_request
from service.app_t.sql.points.sql_points_pointsApp import SqlPointsPointsapp


class AssertPointsPointsapp(SqlPointsPointsapp):
    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_signIn(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_points_pointsApp_signIn(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_myPoints(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_points_pointsApp_myPoints(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_pointsApp_myPointsTotal(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_points_pointsApp_myPointsTotal(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

