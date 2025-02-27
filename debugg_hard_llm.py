# Description: This program implements a simple task scheduler
# It allows adding tasks with priorities and deadlines
# Tasks are sorted by priority and executed if deadline not exceeded
# Includes basic task statistics tracking

import datetime
import random

class Task:
    def __init__(self, name, priority, days_until_deadline):
        self.name = name
        self.priority = priority  # 1-10, higher is more urgent
        self.deadline = datetime.datetime.now() + datetime.timedelta(days_until_deadline)
        self.completed = False

class Scheduler:
    def __init__(self):
        self.tasks = []
        self.stats = {"completed": 0, "failed": 0}

    def add_task(self, name, priority, days):
        task = Task(name, priority, days)
        self.tasks.append(task)
        return task

    def sort_tasks(self):
        self.tasks.sort(key=lambda x: x.priority, reverse=True)

    def execute_tasks(self):
        current_time = datetime.datetime.now()
        for task in self.tasks:
            if task.deadline < current_time:
                if not task.completed:
                    print(f"Task '{task.name}' failed - deadline passed")
                    self.stats["failed"] += 1
            else:
                execution_time = random.randint(1, 5)
                print(f"Executing '{task.name}' (Priority: {task.priority}) "
                      f"- takes {execution_time} seconds")
                task.completed = True
                self.stats["completed"] += 1

    def display_stats(self):
        print(self.stats)
        completion_rate = self.stats["completed"] / (self.stats["completed"] + self.stats["failed"])
        print(f"\nTask Statistics:")
        print(f"Completed: {self.stats["completed"]}")
        print(f"Failed: {self.stats["failed"]}")
        print(f"Completion Rate: {completion_rate:.2%}")

def main():
    scheduler = Scheduler()
    
    # Add some sample tasks
    scheduler.add_task("Fix bugs", 8, 2)
    scheduler.add_task("Write documentation", 3, 5)
    scheduler.add_task("Team meeting", 5, 1)
    scheduler.add_task("Code review", 7, 3)
    
    print("Initial task list:")
    for task in scheduler.tasks:
        print(f"- {task.name} (Priority: {task.priority}, "
              f"Deadline: {task.deadline.strftime('%Y-%m-%d')})")
    
    # Execute tasks
    scheduler.sort_tasks()
    scheduler.execute_tasks()
    
    # Show results
    scheduler.display_stats()

if __name__ == "__main__":
    main()
