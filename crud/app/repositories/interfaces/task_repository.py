
from abc import ABC, abstractmethod
from typing import List
 import Task 

class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def all(self) -> List[Task]:
        pass

    @abstractmethod
    def show(self, id) -> Task:
        pass

    @abstractmethod
    def update(self, id, task:Task) -> Task:
        pass
    
    @abstractmethod
    def delete(self, id):
        pass