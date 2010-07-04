import time, sys

def bench(procs, n=None):
    if n is None:
        if len(sys.argv) == 2:
            n = int(sys.argv[1])
        else:
            n = 20

    results = []
    max_label_len = 0
    for label, func in procs:
        t0 = time.time()
        for i in range(n):
          func()
        tf = time.time()
        results.append((label, tf-t0))
        max_label_len = max(max_label_len, len(label))

    print "%s\ttotal\teach (%d)" % (' ' * max_label_len, n)
    for label, t in results:
        print "%*s\t%.3f\t%.3f" % (max_label_len, label, t, t/n)
