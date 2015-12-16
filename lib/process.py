import multiprocessing

__all__ = [
    'create_process',
    'destory_processes',
]

def create_process(process_dic, func_name = None, args = ()):
    p = multiprocessing.Process(target = func_name, args = args)
    p.start()
    process_dic[ p.pid ] = p

def destory_processes(process_dic):
    destory_process_list = []
    for pid, process in process_dic.items():
        process.join(1)

        if not process.is_alive():
            destory_process_list.append(pid)

    for pid in destory_process_list:
        del process_dic[ pid ]