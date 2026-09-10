"""
To-Do List Application with AI Bot
Features:
- Local storage persistence
- File permissions (r, w, rwx)
- AI-powered task recommendations
- Priority management
"""

import json
import os
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict


class Permission(Enum):
    """File permission levels"""
    READ = 'r'      # Read-only
    WRITE = 'w'     # Write-only
    READ_WRITE = 'rw'  # Read and write
    EXECUTE = 'x'   # Execute
    FULL = 'rwx'    # Full permissions


@dataclass
class Task:
    """Task data structure"""
    id: str
    title: str
    description: str
    completed: bool = False
    priority: int = 1  # 1-5 scale
    created_at: str = None
    due_date: Optional[str] = None
    tags: List[str] = None
    ai_suggestions: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.tags is None:
            self.tags = []
        if self.ai_suggestions is None:
            self.ai_suggestions = []


class FilePermissionManager:
    """Manage file permissions (Unix-style)"""
    
    def __init__(self, filepath: str, permission: Permission = Permission.READ_WRITE):
        self.filepath = filepath
        self.permission = permission
        self.owner_perms = permission.value
    
    def can_read(self) -> bool:
        """Check if file can be read"""
        return 'r' in self.owner_perms
    
    def can_write(self) -> bool:
        """Check if file can be written"""
        return 'w' in self.owner_perms
    
    def can_execute(self) -> bool:
        """Check if file can be executed"""
        return 'x' in self.owner_perms
    
    def set_permission(self, permission: Permission):
        """Set new permission level"""
        self.permission = permission
        self.owner_perms = permission.value
    
    def get_permission_string(self) -> str:
        """Get permission as string (e.g., 'rwx')"""
        return self.owner_perms
    
    def verify_operation(self, operation: str) -> bool:
        """Verify if operation is allowed"""
        if operation == 'read':
            return self.can_read()
        elif operation == 'write':
            return self.can_write()
        elif operation == 'execute':
            return self.can_execute()
        return False


class AITaskBot:
    """AI-powered task suggestions and analysis"""
    
    def __init__(self):
        self.suggestions_db = self._load_suggestions_db()
    
    def _load_suggestions_db(self) -> Dict:
        """Load suggestion database"""
        return {
            'work': [
                'Set a specific deadline',
                'Break into smaller subtasks',
                'Identify dependencies',
                'Review past similar tasks'
            ],
            'personal': [
                'Schedule time for this task',
                'Identify blockers',
                'Consider energy levels',
                'Plan resources needed'
            ],
            'health': [
                'Set regular reminders',
                'Track progress over time',
                'Consider recovery time',
                'Plan with accountability partner'
            ],
            'urgent': [
                'Break into immediate actions',
                'Identify critical path',
                'Request help if needed',
                'Remove non-essential tasks'
            ]
        }
    
    def suggest_improvements(self, task: Task) -> List[str]:
        """Generate AI suggestions for task"""
        suggestions = []
        
        # Analyze task priority
        if task.priority >= 4:
            suggestions.extend(self.suggestions_db['urgent'])
        
        # Analyze task title for keywords
        title_lower = task.title.lower()
        for keyword, keyword_suggestions in self.suggestions_db.items():
            if keyword in title_lower:
                suggestions.extend(keyword_suggestions)
        
        # If no due date, suggest adding one
        if not task.due_date:
            suggestions.append('Add a due date to stay on track')
        
        # If description is short, suggest more details
        if len(task.description) < 20:
            suggestions.append('Add more details to task description')
        
        # Remove duplicates
        return list(dict.fromkeys(suggestions))[:5]  # Top 5 suggestions
    
    def prioritize_tasks(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority and AI recommendations"""
        scored_tasks = []
        for task in tasks:
            if not task.completed:
                score = task.priority * 10
                # Boost score if has AI suggestions
                if task.ai_suggestions:
                    score += len(task.ai_suggestions) * 2
                scored_tasks.append((score, task))
        
        # Sort by score descending
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        return [task for _, task in scored_tasks]
    
    def analyze_productivity(self, tasks: List[Task]) -> Dict:
        """Analyze productivity metrics"""
        total = len(tasks)
        completed = len([t for t in tasks if t.completed])
        high_priority = len([t for t in tasks if t.priority >= 4])
        overdue = len([t for t in tasks if t.due_date and not t.completed])
        
        return {
            'total_tasks': total,
            'completed': completed,
            'completion_rate': (completed / total * 100) if total > 0 else 0,
            'high_priority_tasks': high_priority,
            'overdue_tasks': overdue,
            'efficiency_score': (completed / total * 100) if total > 0 else 0
        }


class ToDoListApp:
    """Main To-Do List Application with local storage"""
    
    def __init__(self, storage_file: str = 'todos.json', permission: Permission = Permission.FULL):
        self.storage_file = storage_file
        self.permission_manager = FilePermissionManager(storage_file, permission)
        self.ai_bot = AITaskBot()
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self) -> bool:
        """Load tasks from local storage"""
        if not self.permission_manager.verify_operation('read'):
            raise PermissionError(f"Read permission denied. Current: {self.permission_manager.get_permission_string()}")
        
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.tasks = [
                        Task(**task) for task in data
                    ]
                return True
        except Exception as e:
            print(f"Error loading tasks: {e}")
        
        self.tasks = []
        return False
    
    def save_tasks(self) -> bool:
        """Save tasks to local storage"""
        if not self.permission_manager.verify_operation('write'):
            raise PermissionError(f"Write permission denied. Current: {self.permission_manager.get_permission_string()}")
        
        try:
            with open(self.storage_file, 'w') as f:
                json.dump([asdict(task) for task in self.tasks], f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def add_task(self, title: str, description: str, priority: int = 1, due_date: Optional[str] = None, tags: List[str] = None) -> Task:
        """Add a new task"""
        task_id = str(len(self.tasks) + 1)
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tags=tags or []
        )
        
        # Get AI suggestions
        task.ai_suggestions = self.ai_bot.suggest_improvements(task)
        
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def update_task(self, task_id: str, **kwargs) -> Optional[Task]:
        """Update an existing task"""
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                
                # Regenerate AI suggestions
                task.ai_suggestions = self.ai_bot.suggest_improvements(task)
                self.save_tasks()
                return task
        return None
    
    def mark_complete(self, task_id: str) -> bool:
        """Mark task as completed"""
        task = self.update_task(task_id, completed=True)
        return task is not None
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        self.tasks = [t for t in self.tasks if t.id != task_id]
        self.save_tasks()
        return True
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks
    
    def get_pending_tasks(self) -> List[Task]:
        """Get incomplete tasks"""
        return [t for t in self.tasks if not t.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get completed tasks"""
        return [t for t in self.tasks if t.completed]
    
    def get_high_priority_tasks(self, priority_level: int = 3) -> List[Task]:
        """Get tasks with priority >= level"""
        return [t for t in self.tasks if t.priority >= priority_level and not t.completed]
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        query_lower = query.lower()
        return [
            t for t in self.tasks 
            if query_lower in t.title.lower() or query_lower in t.description.lower()
        ]
    
    def filter_by_tag(self, tag: str) -> List[Task]:
        """Filter tasks by tag"""
        return [t for t in self.tasks if tag in t.tags]
    
    def get_ai_recommendations(self) -> Dict:
        """Get AI analysis and recommendations"""
        return {
            'productivity': self.ai_bot.analyze_productivity(self.tasks),
            'prioritized_tasks': [
                asdict(t) for t in self.ai_bot.prioritize_tasks(self.tasks)[:5]
            ],
            'suggestions': self.ai_bot.suggest_improvements(self.tasks[0]) if self.tasks else []
        }
    
    def set_permission(self, permission: Permission):
        """Change file access permissions"""
        self.permission_manager.set_permission(permission)
    
    def get_permission(self) -> str:
        """Get current file permissions"""
        return self.permission_manager.get_permission_string()
    
    def generate_report(self) -> str:
        """Generate a text report"""
        pending = self.get_pending_tasks()
        completed = self.get_completed_tasks()
        
        report = f"""
╔════════════════════════════════════════╗
║     TO-DO LIST APPLICATION REPORT      ║
╚════════════════════════════════════════╝

TASK SUMMARY:
────────────────────────────────────────
Total Tasks:          {len(self.tasks)}
Completed:            {len(completed)}
Pending:              {len(pending)}
Completion Rate:      {(len(completed)/len(self.tasks)*100 if self.tasks else 0):.1f}%

FILE PERMISSIONS:     {self.get_permission()}

AI INSIGHTS:
────────────────────────────────────────
"""
        
        ai_data = self.ai_bot.analyze_productivity(self.tasks)
        report += f"Efficiency Score:     {ai_data['efficiency_score']:.1f}%\n"
        report += f"High Priority Tasks:  {ai_data['high_priority_tasks']}\n"
        
        if pending:
            report += f"\nTOP PENDING TASKS:\n────────────────────────────────────────\n"
            for i, task in enumerate(self.ai_bot.prioritize_tasks(pending)[:3], 1):
                report += f"{i}. [{task.priority}/5] {task.title}\n"
        
        return report


if __name__ == '__main__':
    # Example usage
    app = ToDoListApp(permission=Permission.FULL)
    
    # Add some sample tasks
    app.add_task(
        title='Review dataset quality report',
        description='Analyze the data quality metrics and identify issues',
        priority=5,
        tags=['work', 'data']
    )
    
    app.add_task(
        title='Fix inconsistent column naming',
        description='Standardize all column names to snake_case format',
        priority=4,
        tags=['work', 'technical']
    )
    
    # Print report
    print(app.generate_report())
