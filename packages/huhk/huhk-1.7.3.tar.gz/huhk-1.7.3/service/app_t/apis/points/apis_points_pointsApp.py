import allure

from service.app_t import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/myPoints")
def points_pointsApp_myPoints(userId=None, headers=None, **kwargs):
    """
    APP - 查看我的积分
    up_time=1676254812

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : object : 
              records : array : 
              size : number : 每页大小
              current : number : 当前页
              total : number : 总页数
    """
    _method = "GET"
    _url = "/points/pointsApp/myPoints"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/myPointsTotal")
def points_pointsApp_myPointsTotal(userId=None, headers=None, **kwargs):
    """
    APP - 总积分查询
    up_time=1676255216

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 
    params: msg : string : 
    params: data : number : 当前用户积分
    """
    _method = "GET"
    _url = "/points/pointsApp/myPointsTotal"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/pointsApp/signIn")
def points_pointsApp_signIn(userId=None, headers=None, **kwargs):
    """
    APP-用户签到
    up_time=1676254515

    params: userId :  : 用户ID
    params: headers : 请求头
    ====================返回======================
    params: code : number : 0成功;1失败
    params: msg : string : 
    params: data : boolean : true/false 签到成功/失败
    """
    _method = "GET"
    _url = "/points/pointsApp/signIn"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


