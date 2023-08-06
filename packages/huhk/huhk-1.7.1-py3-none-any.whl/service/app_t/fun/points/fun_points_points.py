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


    @allure.step(title="积分统计-分页查询积分")
    def points_points_page(self, beforeTime="$None$", endTime="$None$", current=1, size=10, _assert=True,  **kwargs):
        """
            url=/points/points/page
                params: current :  :
                params: size :  :
                params: beforeTime :  :
                params: endTime :  :
                params: headers : 请求头
        """
        if self.has_true(locals()) and not self._list_beforeTime:
            self.points_points_page(_assert=False)

        beforeTime = self.get_list_choice(beforeTime, self._list_beforeTime)
        endTime = self.get_list_choice(endTime, self._list_endTime)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_page(**_kwargs)

        self.output_list.beforeTime = self.get_res_value_list('beforeTime')
        self.output_list.endTime = self.get_res_value_list('endTime')
        self.input_value.beforeTime = beforeTime
        self.input_value.endTime = endTime

        if _assert is True:
            self.assert_points_points_page(**_kwargs)
        elif _assert is not True:
            assert self.res.rsp.code == _assert or self.res.status_code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="积分统计 - 导出")
    def points_points_download(self, beforeTime="$None$", endTime="$None$", current=1, size=10, _assert=True,  **kwargs):
        """
            url=/points/points/download
                params: current :  :
                params: size :  :
                params: endTime :  :
                params: beforeTime :  :
                params: headers : 请求头
        """
        if self.has_true(locals()) and not self._list_beforeTime:
            self.points_points_download(_assert=False)

        beforeTime = self.get_list_choice(beforeTime, self._list_beforeTime)
        endTime = self.get_list_choice(endTime, self._list_endTime)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_download(**_kwargs)

        self.output_list.beforeTime = self.get_res_value_list('beforeTime')
        self.output_list.endTime = self.get_res_value_list('endTime')
        self.input_value.beforeTime = beforeTime
        self.input_value.endTime = endTime

        if _assert is True:
            self.assert_points_points_download(**_kwargs)
        elif _assert is not True:
            assert self.res.rsp.code == _assert or self.res.status_code == _assert, "校验code=%s不通过" % _assert
        return self.res

    @allure.step(title="用户中心-兑换明细 - 分页查询")
    def points_points_convertDetail(self, userId="$None$", _assert=True,  **kwargs):
        """
            url=/points/points/convertDetail
                params: headers : 请求头
        """
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.points_points_convertDetail(**_kwargs)

        self.input_value.userId = userId

        if _assert is True:
            self.assert_points_points_convertDetail(**_kwargs)
        elif _assert is not True:
            assert self.res.rsp.code == _assert or self.res.status_code == _assert, "校验code=%s不通过" % _assert
        return self.res

