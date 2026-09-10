# To-Do List Application with AI Bot

A smart task management application with AI-powered suggestions, local storage persistence, and Unix-style file permissions (r, w, rwx).

## Features

### 📝 Core Functionality
- **Create Tasks** - Add tasks with title, description, priority, due date, and tags
- **Local Storage** - All data persists in browser localStorage or JSON file
- **Task Management** - Mark complete, edit, delete, search, filter
- **Priority Levels** - 5-level priority system (1=Low to 5=Urgent)
- **Tagging System** - Organize tasks with custom tags

### 🤖 AI Features
- **Smart Suggestions** - AI recommendations based on task content and priority
- **Task Prioritization** - Algorithm-based task ranking
- **Productivity Analytics** - Real-time statistics and insights
- **Pattern Recognition** - Learns from task patterns (work, health, personal)
- **Auto-Categorization** - Suggests improvements based on task details

### 🔐 Permission System (Unix-style)
- **r (Read)** - View tasks and data
- **w (Write)** - Create and modify tasks
- **rwx (Full)** - Complete access (default)
- Dynamic permission checking and enforcement

## Project Structure

```
├── todo_app.py           # Backend with AI bot and permissions
├── todo_app.html         # Interactive web dashboard
├── todos.json            # Local storage file (auto-created)
└── README.md             # Documentation
```

## Installation

### Backend (Python)

```bash
# No additional dependencies required beyond Python 3.7+
python todo_app.py
```

### Frontend (Browser)

```bash
# Simply open the HTML file
open todo_app.html
# Or start a local server
python -m http.server 8000
# Visit http://localhost:8000/todo_app.html
```

## Usage

### Python API

```python
from todo_app import ToDoListApp, Permission

# Initialize with full permissions
app = ToDoListApp(permission=Permission.FULL)

# Add task
task = app.add_task(
    title='Review data quality',
    description='Analyze metrics and identify issues',
    priority=5,
    tags=['work', 'urgent']
)

# Get AI recommendations
recommendations = app.get_ai_recommendations()

# Change permissions
app.set_permission(Permission.READ)  # Read-only
app.set_permission(Permission.READ_WRITE)  # Can read and write

# Get pending tasks
pending = app.get_pending_tasks()

# Generate report
print(app.generate_report())
```

### Web Interface

1. **Add Tasks**: Fill in task details and click "Add Task"
2. **Manage Tasks**: Check to complete, delete to remove
3. **Filter**: View All, Pending, Completed, or High Priority
4. **Search**: Find tasks by keyword
5. **AI Insights**: View productivity metrics and recommendations

## Permission Levels

| Permission | Read | Write | Execute | Use Case |
|-----------|------|-------|---------|----------|
| r         | ✓    | ✗     | ✗       | View-only mode |
| w         | ✗    | ✓     | ✗       | Write-only mode |
| rw        | ✓    | ✓     | ✗       | Normal mode |
| rwx       | ✓    | ✓     | ✓       | Full access |

## AI Suggestions Categories

### Work Tasks
- Set a specific deadline
- Break into smaller subtasks
- Identify dependencies
- Review past similar tasks

### Personal Tasks
- Schedule time for this task
- Identify blockers
- Consider energy levels
- Plan resources needed

### Urgent Tasks (Priority 4-5)
- Break into immediate actions
- Identify critical path
- Request help if needed
- Remove non-essential tasks

### Health Tasks
- Set regular reminders
- Track progress over time
- Consider recovery time
- Plan with accountability partner

## Data Storage

### Browser (Default)
- Uses localStorage API
- Persists across browser sessions
- No server required
- ~5-10MB limit

### Local File (Optional)
- Uses `todos.json` in project directory
- Direct file access with permission checks
- Manual backup capability

## Example Task Structure

```json
{
  "id": "1",
  "title": "Review dataset quality",
  "description": "Analyze metrics and issues",
  "completed": false,
  "priority": 5,
  "created_at": "2024-01-10T14:30:00",
  "due_date": "2024-01-15",
  "tags": ["work", "urgent"],
  "ai_suggestions": [
    "Break into immediate actions",
    "Identify critical path",
    "Set a specific deadline"
  ]
}
```

## Keyboard Shortcuts (Web)

- `Ctrl+Enter` - Add task from input
- `Click checkbox` - Toggle task completion
- `Delete button` - Remove task
- `Search bar` - Filter tasks in real-time

## Performance

- Handles 1000+ tasks efficiently
- Real-time filtering and search
- Instant localStorage sync
- Lightweight AI algorithms (no external API needed)

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- IE11: Partial support

## Future Enhancements

- [ ] Cloud sync (Google Drive, Dropbox)
- [ ] Recurring tasks
- [ ] Time tracking
- [ ] Collaboration features
- [ ] Export to PDF/Excel
- [ ] Mobile app
- [ ] Advanced AI with NLP
- [ ] Voice input

## License

MIT
