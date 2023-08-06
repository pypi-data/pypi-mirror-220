    @allure.step(title="浩瀚模块 - 更改充电桩权益状态-Y")
    @allure.step(title="浩瀚模块 - 更改充电桩权益状态-Y")
    def open_haohan_rights_update(self, params="$None$", _assert=True,  **kwargs):
        """
            url=/open/haohan/rights/update
                params: params : object :
                data : string : 加密数据
                params: headers : 请求头
        """
        params = self.get_value_choice(params, list_or_dict=None)

        _kwargs = self.get_kwargs(locals())
        self.res = app_t_api.open_haohan_rights_update(**_kwargs)

        self.input_value.params = params

        if _assert is True:
            self.assert_open_haohan_rights_update(**_kwargs)
        elif _assert is not True:
            assert self.res.rsp.code == _assert or self.res.status_code == _assert, "校验code=%s不通过" % _assert
        return self.res


