from sqlalchemy import func, text
from sqlalchemy.orm import Session
from app.models.models import Project, Task, User, Attendance

def get_admin_dashboard_metrics(db: Session, project_id: str = None):
    """
    Revised aggregate metrics for Admin Dashboard using SQLAlchemy ORM 
    to handle project_id filtering robustly.
    """
    try:
        # Handle cases where project_id might be a string literal "null", "undefined", or empty
        is_filtered = project_id and project_id not in ["null", "undefined", "None", ""]
        
        if is_filtered:
            # Metrics for a specific project
            active_projects = 1
            active_employees = db.query(User).filter(
                User.role == 'user',
                User.project_id == project_id
            ).count()
            total_tasks = db.query(Task).filter(Task.project_id == project_id).count()
            completed_tasks = db.query(Task).filter(
                Task.project_id == project_id,
                Task.status == 'Completed'
            ).count()
        else:
            # Global Metrics
            active_projects = db.query(Project).count()
            active_employees = db.query(User).filter(User.role == 'user').count()
            total_tasks = db.query(Task).count()
            completed_tasks = db.query(Task).filter(Task.status == 'Completed').count()

        return {
            "activeProjects": int(active_projects),
            "activeEmployees": int(active_employees),
            "totalTasks": int(total_tasks),
            "completedTasks": int(completed_tasks)
        }
    except Exception as e:
        print(f"CRITICAL Error calculating dashboard metrics: {e}")
        # Log more info
        import traceback
        traceback.print_exc()
        return {
            "activeProjects": 0, "activeEmployees": 0, "totalTasks": 0, "completedTasks": 0
        }

def get_user_dashboard_metrics(db: Session, user_id: str):
    """
    Optimized aggregate queries specifically for the User Dashboard overview.
    """
    try:
        total_tasks = db.query(Task).filter(Task.assigned_to == user_id).count()
        completed_tasks = db.query(Task).filter(
            Task.assigned_to == user_id,
            Task.status == 'Completed'
        ).count()
        
        return {
            "totalTasks": total_tasks,
            "completedTasks": completed_tasks,
            "pendingTasks": total_tasks - completed_tasks
        }
    except Exception as e:
        print(f"Error calculating user metrics: {e}")
        return {
            "totalTasks": 0, "completedTasks": 0, "pendingTasks": 0
        }
