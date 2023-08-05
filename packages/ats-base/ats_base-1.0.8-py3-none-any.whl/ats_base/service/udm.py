"""
    结果分析计算验证服务
"""
from ats_base.base import req, entrance
from ats_base.common import func
from ats_base.config.configure import CONFIG

udm = entrance.api(CONFIG.get(func.SERVICE, 'udm'))


def acv(module: str, function: str, data):
    """
    数据验证
    :param module:
    :param function:
    :param data:
    :return:
    """
    result = req.post('{}/{}/{}'.format('{}/{}'.format(udm, 'acv'), module, function), jsons=data)

    if result['code'] == 500:
        raise Exception(result['message'])

    return result['data']


def built_in(module: str, function: str, data):
    """
    数据验证
    :param module:
    :param function:
    :param data:
    :return:
    """
    result = req.post('{}/{}/{}'.format('{}/{}'.format(udm, 'built_in'), module, function), jsons=data)

    if result['code'] == 500:
        raise Exception(result['message'])

    return result['data']
