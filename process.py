import multiprocessing
import json
import sys

from context import difference
from parser import Ontology


class Worker(multiprocessing.Process):

    def __init__(self, folder_a, folder_b, tasks, results):
        self.ontology_a = Ontology(folder_a)
        self.ontology_b = Ontology(folder_b)
        self.tasks = tasks
        self.results = results
        super(Worker, self).__init__()

    def run(self):
        print("Starting worker {0}".format(self.name))
        while True:
            task = self.tasks.get()
            if task is None:
                self.tasks.task_done()
                break
            results = None
            try:
                results = task(self.ontology_a, self.ontology_b)
            except Exception as err:
                print("Error on worker {0}:\n\t{1}".format(self.name, err))
                break
            self.tasks.task_done()
            self.results.put(results)


class Task:

    def __init__(self, idv_a, idv_b):
        self.idv_a = idv_a
        self.idv_b = idv_b

    def __call__(self, ontology_a, ontology_b):
        idv_a = ontology_a.select(self.idv_a)
        idv_b = ontology_b.select(self.idv_b)
        result = {
            "idv_a": self.idv_a,
            "idv_b": self.idv_b,
            "graph": difference(idv_a, idv_b)
        }
        return result


def process(folder_id, max_iter=None, n_jobs=None):
    if n_jobs is None:
        n_jobs = max(1, multiprocessing.cpu_count() - 1)

    queue_tasks = multiprocessing.JoinableQueue()
    queue_results = multiprocessing.Queue()

    print("Instanciating workers...")
    jobs = [Worker("000", folder_id, queue_tasks, queue_results)
            for _ in range(n_jobs)]

    source = Ontology("000")
    target = Ontology(folder_id)

    print("Starting jobs...")
    for job in jobs:
        job.start()

    print("Sending tasks...")
    n_tasks = 0
    for idv_a in source.individuals():
        for idv_b in target.individuals():
            n_tasks += 1
            queue_tasks.put(Task(idv_a.name, idv_b.name))
            if n_tasks >= max_iter:
                break
        if n_tasks >= max_iter:
            break

    print("Sending poison pills...")
    for _ in range(n_jobs):
        queue_tasks.put(None)

    results = []
    n_completed = 0
    while True:
        results.append(queue_results.get())
        n_completed += 1
        print("\rComputing tasks {0}/{1}".format(n_completed, n_tasks), end="")
        sys.stdout.flush()
        if n_completed == n_tasks:
            break

    with open(folder_id + ".json", "w") as output_file:
        json.dump({"items": results}, output_file)


if __name__ == "__main__":
    process("001", max_iter=1000)
