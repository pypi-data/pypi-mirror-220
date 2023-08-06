from pyspark import daemon, worker


def remote_debug_wrapped(*args, **kwargs):
    # ======================Copy and paste from the previous dialog===========================
    import pydevd_pycharm
    pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)
    # ========================================================================================
    worker.main(*args, **kwargs)


daemon.worker_main = remote_debug_wrapped
if __name__ == '__main__':
    daemon.manager()
