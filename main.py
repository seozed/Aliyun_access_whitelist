# coding=utf-8

import requests
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526.RevokeSecurityGroupRequest import RevokeSecurityGroupRequest
from aliyunsdkecs.request.v20140526.AuthorizeSecurityGroupRequest import AuthorizeSecurityGroupRequest
from retry import retry
import ipaddress
import settings

# 此处分别填写创建的RAM子账号的AccessKeyId，子账号的AccessKeySecret，以及要管理的大区
client = AcsClient(settings.ak, settings.secret, settings.region_id)

def validate_ipaddress(ip: str):
    return ipaddress.ip_address(ip)


# 获取当前公网ip
@retry(tries=3)
def get_current_ip():
    url = 'http://checkip.amazonaws.com/'
    response = requests.get(url)
    ip = response.text.strip()
    return ip if validate_ipaddress(ip) else None


# 获取历史公网ip
def GetCompanyOldIp():
    try:
        f = open('ip.txt', 'r')
        oldIP = f.read().strip()
        return oldIP
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    else:
        f.close()


# 写入新的ip到本地
def IputCompanyNewIp(ip):
    try:
        f = open('ip.txt', 'w')
        f.write(ip)
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    else:
        print("写入NewIp成功")
        f.close()




# 删除规则
def DelGroup(SourceCidrIp):
    request = RevokeSecurityGroupRequest()
    request.set_accept_format('json')
    request.set_SecurityGroupId(settings.SecurityGroupId)
    request.set_PortRange("-1/-1")
    request.set_IpProtocol("all")
    request.set_Policy('accept')
    request.set_SourceCidrIp(SourceCidrIp)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


# 添加规则
def AddGroup(SourceCidrIp):
    request = AuthorizeSecurityGroupRequest()
    request.set_accept_format('json')
    request.set_SecurityGroupId(settings.SecurityGroupId)  # 安全组ID
    request.set_IpProtocol("all")
    request.set_PortRange("-1/-1")
    request.set_Description("Added by Python")
    request.set_SourceCidrIp(SourceCidrIp)
    response = client.do_action_with_exception(request)
    print(str(response, encoding='utf-8'))


def main():
    """
    入口
    :return:
    """
    NewIp = get_current_ip()
    if not NewIp:
        exit('获取IP地址失败')
    OldIp = GetCompanyOldIp()
    if NewIp == OldIp:
        print('出口ip没有发生变化')
    else:
        print('出口ip发生变化：', NewIp)
        DelGroup(NewIp)
        AddGroup(NewIp)
        IputCompanyNewIp(NewIp)


if __name__ == '__main__':
    main()
