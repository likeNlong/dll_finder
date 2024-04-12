from lib.Utilitys import *
from lib.config_read import *
import os
import sys
from tqdm import tqdm
import time

if __name__ == "__main__":

    start_print()

    true_dlls = []
    defective_dlls = []

    #根据目标文件位数选择DLL
    source_file = get_exe_is_architecture64(destination_dir+'\\'+exe_name)
    #获取所有DLL的名称
    path_check()
    matches = get_dll_names(dll_names_paths)


    #删除所有干扰DLL
    print('[INFO]: 正在寻找并清除干扰DLL...')
    process_con(exe_name)
    for i in matches:
        if os.path.exists(destination_dir + '\\' + i):
            os.remove(destination_dir + '\\' + i)
    print('[INFO]: 清除干扰DLL成功,开始判断...')

    matches_len = len(matches)

    for index,i in tqdm(enumerate(matches, start=1), file=sys.stdout ,total=matches_len, desc='Processing'):
        #复制执行
        copy_file(source_file,destination_dir+'\\'+i)


        #为确保不受影响，在启动进程前确保白程序进程和计算器进程被成功关闭
        process_con(exe_name)


        #执行程序
        process = execute_exe(destination_dir+'\\'+exe_name)
        time.sleep(delay)

        #判断DLL是否合格
        log = process_con(exe_name)
        process.kill()
        if log == 1:
            if i not in defective_dlls:
                defective_dlls.append(i)
                my_print(f'{i}--->判断可能为有缺陷的DLL文件','warning')
        elif log == 3:
            if i not in true_dlls:
                true_dlls.append(i)
                my_print(f'{i}--->判断可能为可劫持的DLL文件','success')
        #删除文件
        while  is_process_kill(exe_name):
            pass
        os.remove(destination_dir+'\\'+i)

    #输出去重后的最终结果
    end_print(true_dlls,defective_dlls)


