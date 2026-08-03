"""Task Manager - Sarrafa Ayyuka Daga Kowane Wuri"""
import json
import uuid
from datetime import datetime

class TaskManager:
    """Yana sarrafa dukkan ayyukan da agent za ta yi"""
    
    def __init__(self, agent):
        self.agent = agent
        self.tasks = []
        self.task_history = []
        self.task_queue = []
    
    def add_task(self, description, priority=1, context=None, deadline=None):
        """Ƙara sabon aiki"""
        task = {
            'id': str(uuid.uuid4()),
            'description': description,
            'priority': priority,
            'context': context or {},
            'deadline': deadline,
            'status': 'pending',
            'created': datetime.now().isoformat(),
            'completed': None,
            'result': None
        }
        
        self.tasks.append(task)
        self.task_queue.append(task)
        
        # Sort by priority
        self.task_queue.sort(key=lambda x: x['priority'], reverse=True)
        
        return task['id']
    
    def get_pending_tasks(self):
        """Samo dukkan ayyukan da ba a yi ba"""
        pending = [t for t in self.task_queue if t['status'] == 'pending']
        return pending
    
    def mark_completed(self, task_id, result):
        """Alamar cewa an gama aiki"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['status'] = 'completed'
                task['completed'] = datetime.now().isoformat()
                task['result'] = result
                self.task_history.append(task)
                
                # Remove from queue
                self.task_queue = [t for t in self.task_queue if t['id'] != task_id]
                return True
        return False
    
    def get_task_by_id(self, task_id):
        """Samo aiki ta ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def get_all_tasks(self):
        """Samo dukkan ayyuka"""
        return self.tasks
    
    def get_task_history(self):
        """Samo tarihin ayyukan da aka gama"""
        return self.task_history
    
    def clear_completed(self):
        """Share ayyukan da aka gama"""
        self.tasks = [t for t in self.tasks if t['status'] != 'completed']
        self.task_queue = [t for t in self.task_queue if t['status'] != 'completed']