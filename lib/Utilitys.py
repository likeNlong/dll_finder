import ctypes
import platform
import re
import shutil
import subprocess
import time
import progress
import psutil
import win32gui
from tqdm import tqdm
import os
from lib.config_read import *


def start_print():
    print(r'''
             ___    ___ ___    ___ ________  _________   
            |\  \  /  /|\  \  /  /|\   ____\|\___   ___\ 
            \ \  \/  / | \  \/  / | \  \___|\|___ \  \_| 
             \ \    / / \ \    / / \ \_____  \   \ \  \  
              /     \/   /     \/   \|____|\  \   \ \  \ 
             /  /\   \  /  /\   \     ____\_\  \   \ \  \ 
            /__/ /\ __\/__/ /\ __\   |\_________\   \|__|
            |__|/ \|__||__|/ \|__|   \|_________|        

            Project: dll_finder 
            Author：微信公众号-->小惜渗透，欢迎师傅们关注（回复：`彩蛋`有惊喜）                                 
        ''')

def path_check():
    # 启动前自查
    if not(dll_names_paths  and destination_dir and exe_name):
        my_print('config值错误（存在空值），请检查','error')
        exit()
    if not os.path.exists(dll_names_paths):
        my_print('DLL目录文本文件不存在，请检查config.yaml配置','error')
        exit()
    if not os.path.exists(dll_names_paths):
        my_print('白程序所在路径配置错误，请检查config.yaml配置','error')
        exit()

def get_exe_is_architecture64(exe_path):
    # 获取exe文件的位数信息
    arch = platform.architecture(exe_path)
    if arch[0] == '64bit':
        print('[INFO]: 判断目目标白文件为64位，正在选择对应DLL')
        return './static/Dllx64.dll'
    else:
        print('[INFO]: 判断目目标白文件为32位，正在选择对应DLL')
        return './static/Dllx86.dll'

def get_dll_names(dll_names_paths):
    '''
    该函数用来从对应txt文件中查询出所有DLL名字
    参数:
        dll_names_paths: str，存放DLL路径的EXE文本
    返回值:
        matches，存放正则匹配过后获得的所有DLL名字的数组
    '''
    pattern = '[A-Za-z0-9\\-_\\. @]+\\.(?:DLL|dll)'

    with open(dll_names_paths, "r", encoding="utf-8") as file:
        text = file.read()

    matches = re.findall(pattern, text)
    return matches



#创建startupinfo并为其设置隐藏属性
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = progress.HIDE_CURSOR
def execute_exe(exe_path):
    '''
        单独封装出来的使用subprocess库执行程序的函数，方便用于线程执行函数的对象赋值，将被启动的程序的输出重定向到一个空管道避免干扰主程序运行
        参数: None
        返回值: None
    '''
    process = subprocess.Popen(exe_path,startupinfo=startupinfo,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return process




def copy_file(source_file, destination_dir):
    '''
            文件复制函数
            参数:
                source_file: str，源文件路径
                destination_dir: str，目标文件路径
            返回值: None
    '''
    try:
        shutil.copy(source_file, destination_dir)
    except Exception as e:
        my_print(f"文件复制失败: {e}，请检查权限是否正确，建议使用管理员权限运行。",'error')
        exit()

#检测文件是否被删除
def is_process_kill(process_name):
    for proc in psutil.process_iter():
        try:
            try:
                process = psutil.Process(proc.pid)
            except:
                process_con(process_name)
                break
            if process_name.lower() in process.name().lower():
                return True
        except:
            pass
    return False

def process_con(process_name):
    '''
            该函数用来统计是计算机进程列表中否存在计算器进程以及待测试的白程序进程，并将其关闭
            参数:
                process_name: str，待测试的白程序进程名称
            返回值:
                log，进程标记，当log为1表示只存在计算器进程，证明对应测试的DLL文件可以达到劫持操作，但白程序无法正确运行
                             当log为2表示DllMain的函数没正常执行
                             当log为3表示两个进程均存在，判断该DLL极大可能性为可劫持的DLL
    '''
    calc_log = 0
    exe_log = 0
    for proc in psutil.process_iter():
        try:
            try:
                process = psutil.Process(proc.pid)
            except:
                return process_con(process_name)
            if "calc.exe".lower() in process.name().lower():
                calc_log = 1
                process.kill()
            if process_name.lower() in process.name().lower():
                exe_log = 2
                process.kill()
                time.sleep(0.1)
                #保险起见
                try:
                    subprocess.check_output(["taskkill", "/F", "/IM", process_name], stderr=subprocess.STDOUT)
                except:
                    pass
                #解决小图标仍然存在的bug
                refresh_ico()

        except:
            #my_print('进程查询失败，请检测','error')
            return process_con(process_name)

    return calc_log + exe_log

# 获取任务栏窗口句柄
hShellTrayWnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
#计算偏移
skew = win32gui.GetWindowRect(hShellTrayWnd)[3] - win32gui.GetWindowRect(hShellTrayWnd)[1]
notify = ctypes.windll.user32.FindWindowExW(0, 0, "NotifyIconOverflowWindow", None)
notify_son = ctypes.windll.user32.FindWindowExW(notify, 0, "ToolbarWindow32", None)
def refresh_ico():
    '''
    鼠标位置是针对于任务栏整体的
    托盘溢出区的子窗口也就是图标隐藏区
    托盘溢出区以及子窗口，显示位置为任务栏上方，实际坐标为下方，所以发送鼠标信号消息要加上偏移
    '''
    rect = win32gui.GetWindowRect(notify_son)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    step = 50
    for x in range(1,  width + step, step):
        for y in range(1, height + skew + step, step):
            ctypes.windll.user32.SendMessageW(notify_son, 0x0200, 0, x | (y // 2 << 16))

def my_print(text,log=None):
    '''
            该函数封装了tqdm.write函数，能够在不影响进度条正常显示的情况下，根据不同情况输出不同的颜色和状态的内容
            参数:
                text: str，要输出的文字
                log: str，状态标志，默认为None
            返回值:None
    '''
    if log == 'success':
        tqdm.write(f"\033[92m[SUCCESS]: {text}\033[0m")
    elif log == 'error':
        tqdm.write(f"\033[91m[ERROR]: {text}\033[0m")
    elif log == 'warning':
        tqdm.write(f"\033[93m[WARNING]: {text}\033[0m")
    else:
        tqdm.write(text)

def end_print(true_dlls,defective_dlls):
    print("\n")
    print('----------------XXST-测试最终结果为---------------------')
    print()
    print(f'\033[1m可劫持的DLL文件：\033[0m  {true_dlls}')
    print(f'\033[1m有缺陷的可劫持的DLL文件：\033[0m  {defective_dlls}')
    print()
    print('-----------------------------------------------------')
