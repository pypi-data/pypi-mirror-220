import time


class Task:
    def __init__(self, name, priority, next_run_time):
        self.name = name
        self.priority = priority
        self.next_run_time = next_run_time

    def run(self):
        # The specific implementation of running the task
        pass

    def update_next_run_time(self, delay):
        self.next_run_time = time.time() + delay

    def __lt__(self, other):
        # Compare tasks based on their next_run_time
        # In case of a tie, compare their priority
        return (self.next_run_time, self.priority) < (other.next_run_time, other.priority)
