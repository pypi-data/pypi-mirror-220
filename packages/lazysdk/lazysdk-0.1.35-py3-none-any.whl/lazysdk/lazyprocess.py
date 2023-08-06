#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from multiprocessing import Process
from multiprocessing import Queue
import showlog
import time
import copy
import os
os_cpu_count = os.cpu_count()  # CPU核心数


def run(
        task_list: list,
        task_function,
        subprocess_keep: bool = False,
        subprocess_limit: int = None,
        master_process_delay: int = 1,
        return_data: bool = False,
        silence: bool = False
):
    """
    多进程 进程控制
    :param task_list: 任务列表，list格式，会将list中的每个元素传入给task_function中的task_info，作为任务的详细信息；
    :param task_function: 子任务的function，需提前写好，入参为：(task_index, task_info)，例如：task_function(task_index, task_info)
    :param subprocess_keep: 是否保持子进程，True为保持进程，死掉会自动重启；False为不保持，自然退出
    :param subprocess_limit: 进程数限制，0为无限制，否则按照设定的数量限制并行的子进程数量
    :param master_process_delay: 主进程循环延时，单位为秒，默认为1秒
    :param return_data: 是否返回数据，True返回，False不返回
    :param silence: 静默模式，为True是不产生任何提示

    demo:
    def task_function(
            task_index,
            task_info
    ):
        # 进程详细的内容
        print(task_index, task_info)
    """
    inner_task_list = copy.deepcopy(task_list)  # 深度拷贝，防止篡改
    if subprocess_limit:
        # 存在自定义的子进程数量限制，将采用
        pass
    else:
        # 不存在自定义的子进程数量限制，将使用默认计算方式
        if os_cpu_count > 1:
            # 如果cpu核心数大于1个
            subprocess_limit = os_cpu_count - 1  # 子进程数设置为cpu核心数减1
        else:
            # 如果cpu核心数等于1个
            subprocess_limit = 1
    active_process = dict()  # 存放活跃进程进程，以task_index为key，进程信息为value的dict
    total_task_num = len(inner_task_list)  # 总任务数量
    task_index_start = 0  # 用来计算启动的累计进程数
    if return_data:
        q = Queue()  # 生成一个队列对象，以实现进程通信
    else:
        pass

    if silence:
        pass
    else:
        showlog.info(f'正在准备多进程执行任务，总任务数为：{total_task_num}，进程数限制为：{subprocess_limit}...')
    # 创建并启动进程
    while True:
        this_time_start = copy.deepcopy(task_index_start)  # 深度拷贝累积启动的进程数，以确定本次循环的起点任务序号，假设subprocess_keep为False
        for task_index in range(this_time_start, total_task_num):  # 按照任务量遍历
            # 判断是否需要创建新的子进程
            if len(active_process.keys()) >= subprocess_limit:
                # 当前活跃进程数量达到子进程数限制，本次循环不再新增进程，跳出
                if silence is False:
                    showlog.warning(f'达到子进程数限制：{subprocess_limit}')
                break
            else:
                # 未达到进程数限制
                if task_index in active_process.keys():
                    # 进程已存在，不重复创建，跳过
                    continue
                else:
                    # 进程不存在，待定
                    # 不存在子进程限制规则/当前活跃进程数量未达到进程数限制，将开启一个新进程
                    if silence is False:
                        showlog.info(f'发现需要开启的子进程：{task_index}/{total_task_num}')
                    task_info = inner_task_list[task_index]  # 提取将开启的进程的任务内容
                    # ---------- 开启进程 ----------
                    if return_data is True:
                        p = Process(
                            target=task_function,
                            args=(task_index, task_info, q)
                        )
                    else:
                        p = Process(
                            target=task_function,
                            args=(task_index, task_info)
                        )
                    p.start()
                    # ---------- 开启进程 ----------
                    active_process[task_index] = {
                        'task_index': task_index,  # 任务序号
                        'task_info': task_info,  # 任务详情
                        'process': p,  # 进程对象
                    }  # 记录开启的进程
                    if silence is False:
                        showlog.info(f'子进程：{task_index}/{total_task_num} 已开启')
                    task_index_start += 1  # 记录累计开启进程数

        # 检测非活跃进程，并从active_process中剔除非活跃进程，以便开启新的进程
        inactive_process_temp = list()  # 非活跃进程
        for process_index, process_info in active_process.items():
            # print(q.qsize())
            # print(q.get())
            # print(q.get_nowait())
            if process_info['process'].is_alive() is True:
                # 该子进程仍然运行
                continue
            else:
                # 该子进程停止运行
                if silence is False:
                    showlog.warning(f'进程 {process_index} 不活跃，将被剔除...')
                inactive_process_temp.append(process_index)
                # 尝试终止进程
                # process_info['process'].terminate()
                # process_info['process'].join()

        if inactive_process_temp:
            # 存在需要剔除的子进程
            for each_dead_process in inactive_process_temp:
                # 尝试终止进程
                active_process[each_dead_process]['process'].terminate()
                active_process[each_dead_process]['process'].join()
                active_process.pop(each_dead_process)
        else:
            # 不存在需要剔除的子进程
            pass
        if silence is False:
            showlog.info(f'>> 当前活跃进程数：{len(active_process.keys())}')
        else:
            pass

        if task_index_start >= len(inner_task_list) and len(active_process.keys()) == 0:
            if silence is False:
                showlog.info('全部任务执行完成')
            else:
                pass
            if subprocess_keep is True:
                task_index_start = 0  # 将累计启动进程数重置为0
            else:
                return
        else:
            pass
        time.sleep(master_process_delay)


def task_function_demo(
        task_index,
        task_info,
        q=None
):
    print(task_index, task_info)
    time.sleep(1)
    q.put(task_index)


if __name__ == '__main__':
    task_list_demo = [
        {'task_id': 1},
        {'task_id': 2},
        {'task_id': 3},
        {'task_id': 4},
        {'task_id': 5},
        {'task_id': 6},
        {'task_id': 7},
        {'task_id': 8},
        {'task_id': 9},
        {'task_id': 10},
        {'task_id': 11},
    ]
    run(
        task_list=task_list_demo,
        task_function=task_function_demo,
        return_data=True,
        # silence=True
    )
