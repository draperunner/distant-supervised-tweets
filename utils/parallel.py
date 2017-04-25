# http://stackoverflow.com/a/5792404
from multiprocessing import Process, Pipe


def spawn(f):
    def fun(pipe, x):
        pipe.send(f(x))
        pipe.close()

    return fun


def parmap(func, listlike):
    pipe = [Pipe() for x in listlike]
    proc = [Process(target=spawn(func), args=(c, x)) for x, (p, c) in zip(listlike, pipe)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [p.recv() for (p, c) in pipe]
