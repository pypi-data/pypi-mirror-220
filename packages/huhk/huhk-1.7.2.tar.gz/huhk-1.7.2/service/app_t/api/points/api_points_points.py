import allure

from service.app_t import http_requester
from huhk.unit_request import get_url


@allure.step(title="调接口：/points/points/flowDetail")
def points_points_flowDetail(userId=None, headers=None, **kwargs):
    """
    查看积分明细- - 积分流水分页查询
    up_time=1676254506

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
    _url = "/points/points/flowDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/page")
def points_points_page(current=None, beforeTime=None, size=None, endTime=None, headers=None, **kwargs):
    """
    积分统计-分页查询积分
    up_time=1676269112

    params: current :  : 
    params: size :  : 
    params: beforeTime :  : 
    params: endTime :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              records : object : 日期
              size : string : 
              current : string : 
              total : string : 
    """
    _method = "GET"
    _url = "/points/points/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "beforeTime": beforeTime,
        "endTime": endTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/download")
def points_points_download(current=None, beforeTime=None, size=None, endTime=None, headers=None, **kwargs):
    """
    积分统计 - 导出
    up_time=1676266332

    params: current :  : 
    params: size :  : 
    params: endTime :  : 
    params: beforeTime :  : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/points/points/download"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "endTime": endTime,
        "beforeTime": beforeTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/convertDetail")
def points_points_convertDetail(userId=None, headers=None, **kwargs):
    """
    用户中心-兑换明细 - 分页查询
    up_time=1676267280

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
    _url = "/points/points/convertDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/flowDetail")
def points_points_flowDetail(userId=None, headers=None, **kwargs):
    """
    查看积分明细- - 积分流水分页查询
    up_time=1676254506

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
    _url = "/points/points/flowDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/page")
def points_points_page(endTime=None, size=None, current=None, beforeTime=None, headers=None, **kwargs):
    """
    积分统计-分页查询积分
    up_time=1676269112

    params: current :  : 
    params: size :  : 
    params: beforeTime :  : 
    params: endTime :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              records : object : 日期
              size : string : 
              current : string : 
              total : string : 
    """
    _method = "GET"
    _url = "/points/points/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "beforeTime": beforeTime,
        "endTime": endTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/download")
def points_points_download(endTime=None, size=None, current=None, beforeTime=None, headers=None, **kwargs):
    """
    积分统计 - 导出
    up_time=1676266332

    params: current :  : 
    params: size :  : 
    params: endTime :  : 
    params: beforeTime :  : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/points/points/download"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "endTime": endTime,
        "beforeTime": beforeTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/convertDetail")
def points_points_convertDetail(userId=None, headers=None, **kwargs):
    """
    用户中心-兑换明细 - 分页查询
    up_time=1676267280

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
    _url = "/points/points/convertDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/flowDetail")
def points_points_flowDetail(userId=None, headers=None, **kwargs):
    """
    查看积分明细- - 积分流水分页查询
    up_time=1676254506

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
    _url = "/points/points/flowDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/page")
def points_points_page(size=None, current=None, endTime=None, beforeTime=None, headers=None, **kwargs):
    """
    积分统计-分页查询积分
    up_time=1676269112

    params: current :  : 
    params: size :  : 
    params: beforeTime :  : 
    params: endTime :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              records : object : 日期
              size : string : 
              current : string : 
              total : string : 
    """
    _method = "GET"
    _url = "/points/points/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "beforeTime": beforeTime,
        "endTime": endTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/download")
def points_points_download(size=None, current=None, endTime=None, beforeTime=None, headers=None, **kwargs):
    """
    积分统计 - 导出
    up_time=1676266332

    params: current :  : 
    params: size :  : 
    params: endTime :  : 
    params: beforeTime :  : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/points/points/download"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "endTime": endTime,
        "beforeTime": beforeTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/convertDetail")
def points_points_convertDetail(userId=None, headers=None, **kwargs):
    """
    用户中心-兑换明细 - 分页查询
    up_time=1676267280

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
    _url = "/points/points/convertDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/flowDetail")
def points_points_flowDetail(userId=None, headers=None, **kwargs):
    """
    查看积分明细- - 积分流水分页查询
    up_time=1676254506

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
    _url = "/points/points/flowDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/page")
def points_points_page(current=None, endTime=None, beforeTime=None, size=None, headers=None, **kwargs):
    """
    积分统计-分页查询积分
    up_time=1676269112

    params: current :  : 
    params: size :  : 
    params: beforeTime :  : 
    params: endTime :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              records : object : 日期
              size : string : 
              current : string : 
              total : string : 
    """
    _method = "GET"
    _url = "/points/points/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "beforeTime": beforeTime,
        "endTime": endTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/download")
def points_points_download(beforeTime=None, current=None, endTime=None, size=None, headers=None, **kwargs):
    """
    积分统计 - 导出
    up_time=1676266332

    params: current :  : 
    params: size :  : 
    params: endTime :  : 
    params: beforeTime :  : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/points/points/download"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "endTime": endTime,
        "beforeTime": beforeTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/convertDetail")
def points_points_convertDetail(userId=None, headers=None, **kwargs):
    """
    用户中心-兑换明细 - 分页查询
    up_time=1676267280

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
    _url = "/points/points/convertDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/flowDetail")
def points_points_flowDetail(userId=None, headers=None, **kwargs):
    """
    查看积分明细- - 积分流水分页查询
    up_time=1676254506

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
    _url = "/points/points/flowDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/page")
def points_points_page(beforeTime=None, endTime=None, current=None, size=None, headers=None, **kwargs):
    """
    积分统计-分页查询积分
    up_time=1676269112

    params: current :  : 
    params: size :  : 
    params: beforeTime :  : 
    params: endTime :  : 
    params: headers : 请求头
    ====================返回======================
    params: code : string : 
    params: msg : string : 
    params: data : object : 
              records : object : 日期
              size : string : 
              current : string : 
              total : string : 
    """
    _method = "GET"
    _url = "/points/points/page"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "beforeTime": beforeTime,
        "endTime": endTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/download")
def points_points_download(beforeTime=None, endTime=None, current=None, size=None, headers=None, **kwargs):
    """
    积分统计 - 导出
    up_time=1676266332

    params: current :  : 
    params: size :  : 
    params: endTime :  : 
    params: beforeTime :  : 
    params: headers : 请求头
    ====================返回======================
    """
    _method = "GET"
    _url = "/points/points/download"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "current": current,
        "size": size,
        "endTime": endTime,
        "beforeTime": beforeTime,
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


@allure.step(title="调接口：/points/points/convertDetail")
def points_points_convertDetail(userId=None, headers=None, **kwargs):
    """
    用户中心-兑换明细 - 分页查询
    up_time=1676267280

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
    _url = "/points/points/convertDetail"

    _headers = {
    }
    _headers.update({"headers": headers})

    _data = {
        "userId": userId,  # 用户ID
    }

    _params = {
    }

    return http_requester(_method, _url, params=_params, data=_data, headers=_headers, **kwargs)


