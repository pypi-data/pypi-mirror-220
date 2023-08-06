import ctypes
import os
import sys
import threading
from ctypes import *


dll_dir = os.path.dirname(os.path.abspath(__file__))
os.add_dll_directory(dll_dir)
N_dll = CDLL("N.dll")

Run_ID = 0
lock_ID = threading.Lock()  # 创建一个锁对象


def GetRun_ID():
    """获取运行的ID"""
    global Run_ID
    with lock_ID:  # 使用锁来保证 Run_ID 的线程安全
        Run_ID = Run_ID + 1
        if Run_ID > 200:
            Run_ID = 1
        return Run_ID


def on_callback(Msg=None):
    """回调函数"""
    print("callback:", Msg.decode("gbk"))
    return 42


def callback_Add():
    # 建立一个全局的回调函数
    # 将 Python 函数转换为 C 可调用的函数指针
    callback_type = WINFUNCTYPE(c_int, c_char_p)
    callback_func = callback_type(on_callback)
    # 打印函数指针的整数表示
    callback_int = cast(callback_func, c_void_p).value
    return callback_int


def initialize(callback=True):
    """初始化"""

    callback_int = callback_Add() if callback else 0
    # 建立回调函数

    N_initialize = N_dll.N_initialize
    r = N_initialize(callback_int)

    return string_at(r).decode("gbk")


def login(ID, Uin, Password, Guid=None):
    """常规登录"""
    Guid = Guid or ""

    N_Login = N_dll.N_Login
    N_Login.argtypes = [c_int, c_char_p, c_char_p, c_char_p]
    result = string_at(
        N_Login(ID, Uin.encode("gbk"), Password.encode("gbk"), Guid.encode("gbk"))
    )
    return result.decode("gbk")


def login_tailless(ID, TokenA):
    """无尾模式"""
    N_login_tailless = N_dll.N_login_tailless
    r = N_login_tailless(c_int(ID), c_char_p(TokenA.encode("gbk")))
    return string_at(r).decode("gbk")


def login_Submit_slider(ID, Ticket):
    """提交滑块"""
    N_login_Submit_slider = N_dll.N_login_Submit_slider
    print(N_login_Submit_slider)
    r = N_login_Submit_slider(ID, c_char_p(Ticket.encode("gbk")))
    return string_at(r).decode("gbk")


def login_Send_verification_to_the_phone(ID):
    """发送验证码到手机"""
    N_login_Send_verification_to_the_phone = (
        N_dll.N_login_Send_verification_to_the_phone
    )
    r = N_login_Send_verification_to_the_phone(ID)
    return string_at(r).decode("gbk")


def login_Submit_verificationcode(ID, code):
    """设备锁提交验证码"""
    N_login_Submit_verificationcode = N_dll.N_login_Submit_verificationcode
    r = N_login_Submit_verificationcode(ID, c_char_p(code.encode("gbk")))
    return string_at(r).decode("gbk")


def Scan_code_authorization(ID, k):
    """扫码授权"""
    N_Scan_code_authorization = N_dll.N_Scan_code_authorization
    r = N_Scan_code_authorization(ID, c_char_p(k.encode("gbk")))
    return string_at(r).decode("gbk")


def Scan_code_assist(ID, str_url):
    """扫码——辅助验证"""
    N_Scan_code_assist = N_dll.N_Scan_code_assist
    r = N_Scan_code_assist(ID, c_char_p(str_url.encode("gbk")))
    return string_at(r).decode("gbk")


def Refresh_token(ID):
    """
    刷新令牌,刷新成功后将返回新的解登录包,也可以通过GetTokenA获取新的TokenA
    """
    N_login_Refresh_token = N_dll.N_login_Refresh_token
    r = N_login_Refresh_token(ID)
    return string_at(r).decode("gbk")


def GetTokenA(ID):
    """获取当前运行ID的TokenA"""
    N_GetTokenA = N_dll.N_GetTokenA
    r = N_GetTokenA(ID)
    return string_at(r).decode("gbk")


def Group_Get_condition(ID, Group):
    """获取群条件"""
    N_Group_Get_condition = N_dll.N_Group_Get_condition
    r = N_Group_Get_condition(ID, c_int64(Group))
    return string_at(r).decode("gbk")


def N_subscribe_unfollow(ID, Target):
    """
    取消订阅号关注
    2720152058 QQ团队
    1770946116 安全中心
    """
    N_subscribe_unfollow = N_dll.N_subscribe_unfollow
    r = N_subscribe_unfollow(ID, c_int64(Target))
    return string_at(r).decode("gbk")


def AS_Get_login_infor(ID, type_):
    """
    账号安全_获取登陆信息
    1 在线设备 2 历史设备 3 在线和历史不区分
    """

    N_AS_Get_login_infor = N_dll.N_AS_Get_login_infor
    r = N_AS_Get_login_infor(ID, c_int(type_))
    return string_at(r).decode("gbk")


def AS_Del_login_Infor(ID, target):
    """
    账号安全_删除设备信息
    target为获取设备信息里面的j7
    """

    N_AS_Del_login_Infor = N_dll.N_AS_Del_login_Infor
    r = N_AS_Del_login_Infor(ID, c_char_p(target))
    return string_at(r).decode("gbk")


def auth_get_list(ID, num):
    """授权获取授权列表"""
    N_auth_get_list = N_dll.N_auth_get_list
    r = N_auth_get_list(ID, c_int(num))
    return string_at(r).decode("gbk")


def Get_Phone(ID):
    """授权获取授权列表"""
    N_Get_Phone = N_dll.N_Get_Phone
    r = N_Get_Phone(ID)
    return string_at(r).decode("gbk")


def TCP_Send(ID, data, wait, ssoseq):
    """TCP发送数据"""
    N_TCP_Send = N_dll.N_TCP_Send
    r = N_TCP_Send(ID, c_char_p(data, wait, ssoseq))
    return string_at(r).decode("gbk")


def Get_version():
    """获取版本号"""
    r = N_dll.Get_Version_infor()
    return string_at(r).decode("gbk")


# 默认就初始化
print(initialize())
