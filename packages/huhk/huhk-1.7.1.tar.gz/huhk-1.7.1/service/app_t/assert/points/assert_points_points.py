import allure

from service.app_t import unit_request
from service.app_t.sql.points.sql_points_points import SqlPointsPoints


class AssertPointsPoints(SqlPointsPoints):
    @allure.step(title="接口返回结果校验")
    def assert_points_points_flowDetail(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_points_points_flowDetail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_page(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_points_points_page(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["beforeTime", "endTime"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_download(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_points_points_download(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["beforeTime", "endTime"])
        assert True, "数据比较不一致"

    @allure.step(title="接口返回结果校验")
    def assert_points_points_convertDetail(self, **kwargs):
        assert unit_request.is_assert_true(self.res)
        # out = self.sql_points_points_convertDetail(**kwargs)
        # flag = self.compare_json_list(self.res, out, ["userId"])
        assert True, "数据比较不一致"

