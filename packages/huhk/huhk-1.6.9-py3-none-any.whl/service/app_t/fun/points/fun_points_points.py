    @allure.step(title="查看积分明细- - 积分流水分页查询")
    @allure.step(title="查看积分明细- - 积分流水分页查询")
    def points_points_flowDetail(self, userId="$None$", _assert=True,  **kwargs):
        """
            url=/points/points/flowDetail
                params: headers : 请求头
        """
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_flowDetail(**_kwargs)

        self.input_value.userId = userId

        if _assert is True:
            self.assert_points_points_flowDetail(**_kwargs)
        elif _assert is not True:
            assert self.res.rsp.code == _assert or self.res.status_code == _assert, "校验code=%s不通过" % _assert
        return self.res


