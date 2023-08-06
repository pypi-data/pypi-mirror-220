import ctypes
import threading
import time
from funboost.utils.time_util import DatetimeConverter
import requests


class ThreadKillAble(threading.Thread):
    task_id = None
    killed = False
    event_kill = threading.Event()


def kill_thread(thread_id):
    ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_id), ctypes.py_object(SystemExit))


class ThreadHasKilled(Exception):
    pass


def kill_fun_deco(task_id):
    def _inner(f):
        def __inner(*args, **kwargs):
            def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
                result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))
                threading.current_thread().event_kill.set()  # noqa

            result = []
            new_kwargs = {
                'oldfunc': f,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }

            thd = ThreadKillAble(target=_new_func, args=(), kwargs=new_kwargs)
            thd.task_id = task_id
            thd.event_kill = threading.Event()
            thd.start()
            thd.event_kill.wait()
            if not result and thd.killed is True:
                raise ThreadHasKilled(f'{DatetimeConverter()} 线程已被杀死 {thd.task_id}')
            return result[0]

        return __inner

    return _inner


def kill_thread_by_task_id(task_id):
    for t in threading.enumerate():
        if isinstance(t, ThreadKillAble):
            thread_task_id = getattr(t, 'task_id', None)
            if thread_task_id == task_id:
                t.killed = True
                t.event_kill.set()
                kill_thread(t.ident)


if __name__ == '__main__':
    import nb_log

    test_lock = threading.Lock()


    def my_fun(x):
        """
        使用lock.acquire(),强行杀死会一直无法释放锁
        """
        test_lock.acquire()
        print(f'start {x}')
        # resp = requests.get('http://127.0.0.1:5000')  # flask接口里面sleep30秒，
        # print(resp.text)
        for i in range(10):
            time.sleep(2)
        test_lock.release()
        print(f'over {x}')
        return 666


    def my_fun2(x):
        """
        使用with lock,强行杀死会不会出现一直无法释放锁
        """
        with test_lock:
            print(f'start {x}')
            # resp = requests.get('http://127.0.0.1:5000')  # flask接口里面sleep30秒，
            # print(resp.text)
            for i in range(10):
                time.sleep(2)
            print(f'over {x}')
            return 666


    threading.Thread(target=kill_fun_deco(task_id='task1234')(my_fun2), args=(777,)).start()
    threading.Thread(target=kill_fun_deco(task_id='task5678')(my_fun2), args=(888,)).start()
    time.sleep(5)
    kill_thread_by_task_id('task1234')

    """
    第一种代码：
    test_lock.acquire()
    执行io耗时代码
    test_lock.release()
    如果使用lock.acquire()获得锁以后，执行耗时代码时候，还没有执行lock.release() 强行杀死线程，会导致锁一直不能释放
    
    第二种代码
    with test_lock:
        执行io耗时代码
    使用with lock 获得锁以后，执行耗时代码时候，强行杀死线程，则不会导致锁一直不能释放
    
    """
