class Task:
    def _init_(self, id, duration):
        self.id = id
        self.duration = duration
        self.dependencies = []
        self.EST = float('inf')  # Earliest Start Time
        self.EFT = 0             # Earliest Finish Time
        self.LST = float('inf')  # Latest Start Time
        self.LFT = 0             # Latest Finish Time

    def add_dependency(self, task):
        self.dependencies.append(task)

class Project:
    def _init_(self):
        self.tasks = {}

    def add_task(self, id, duration):
        self.tasks[id] = Task(id, duration)

    def add_dependency(self, from_id, to_id):
        self.tasks[to_id].add_dependency(self.tasks[from_id])

    def calculate_earliest_times(self):
        # Topological Sort using Kahn's Algorithm to handle tasks in order
        from collections import deque
        in_degree = {id: 0 for id in self.tasks}
        for task in self.tasks.values():
            for dep in task.dependencies:
                in_degree[task.id] += 1
        queue = deque([id for id in self.tasks if in_degree[id] == 0])
        while queue:
            current_id = queue.popleft()
            current_task = self.tasks[current_id]
            if not current_task.dependencies:
                current_task.EST = 0  # start at time 0 if no dependencies
            current_task.EFT = current_task.EST + current_task.duration
            for neighbor in self.tasks.values():
                if current_task in neighbor.dependencies:
                    neighbor.EST = max(neighbor.EST, current_task.EFT)
                    in_degree[neighbor.id] -= 1
                    if in_degree[neighbor.id] == 0:
                        queue.append(neighbor.id)

    def calculate_latest_times(self, project_end_time):
        # Initialize LFT for all terminal tasks
        for task in self.tasks.values():
            if not any(task in t.dependencies for t in self.tasks.values()):
                task.LFT = project_end_time
                task.LST = task.LFT - task.duration
        # Process tasks in reverse topological order
        for task in reversed(list(self.tasks.values())):
            for dep in task.dependencies:
                dep.LFT = min(dep.LFT, task.LST)
                dep.LST = dep.LFT - dep.duration

    def find_project_completion_time(self):
        self.calculate_earliest_times()
        max_eft = max(task.EFT for task in self.tasks.values())
        self.calculate_latest_times(max_eft)
        return max_eft, max(task.LFT for task in self.tasks.values())

# Example usage
proj = Project()
proj.add_task('A', 5)
proj.add_task('B', 3)
proj.add_task('C', 2)
proj.add_dependency('A', 'B')
proj.add_dependency('A', 'C')
earliest_completion, latest_completion = proj.find_project_completion_time()
print(f"Earliest Completion Time: {earliest_completion}")
print(f"Latest Completion Time: {latest_completion}")