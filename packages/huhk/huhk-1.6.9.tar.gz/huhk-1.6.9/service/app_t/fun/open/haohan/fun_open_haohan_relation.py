    @allure.step(title="浩瀚模块-关联关系-Y")
    @allure.step(title="浩瀚模块-关联关系-Y")
    def open_haohan_relation_update(self, userId="$None$", _assert=True,  **kwargs):
        """
            url=/open/haohan/relation/update
                params: headers : 请求头
        """
        userId = self.get_value_choice(userId, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.open_haohan_relation_update(**_kwargs)

        self.input_value.userId = userId

        if _assert is True:
            self.assert_open_haohan_relation_update(**_kwargs)
        elif _assert is not True:
            assert self.res.rsp.code == _assert or self.res.status_code == _assert, "校验code=%s不通过" % _assert
        return self.res


