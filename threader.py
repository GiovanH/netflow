import threading


def map(task, pendingData, maxThreads=4):
    """Task: a function task(data) that operates on one piece
    of data and returns the result.
    PendingData: An array of data. Each will be processed
    and the result returned in an unsorted list.
    """
    threads = []
    expectedData = len(pendingData)
    results = []

    def taskwrapper():
        """thread worker function"""
        while(len(pendingData) > 0):
            data = pendingData.pop()
            results.append(task(data))

    for i in range(maxThreads):
        t = threading.Thread(target=taskwrapper)
        threads.append(t)
        t.start()

    while len(results) < expectedData:
        continue

    return results
