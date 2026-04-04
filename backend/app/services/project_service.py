from sqlalchemy.orm import Session
from app.models.models import Project
from app.schemas.schemas import ProjectCreate, ProjectUpdate
<<<<<<< HEAD
from app.utils.cloudinary_utils import upload_base64_image
=======
>>>>>>> 803770a4512ea25f36e8e70d89c573a2e84035d2

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all projects."""
    return db.query(Project).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
def get_project(db: Session, project_id: str):
    """Retrieve a single project by ID."""
    return db.query(Project).filter(Project.id == project_id).first()

def create_project(db: Session, project: ProjectCreate):
    # 🔍 check duplicate
<<<<<<< HEAD
    # 🔥 Handle Image -> Cloudinary
    final_image = project.image
    if final_image and final_image.startswith("data:image"):
        cloudinary_url = upload_base64_image(final_image, folder="projects")
        if cloudinary_url:
            final_image = cloudinary_url

    db_project = Project(
        name=project.name,
        image=final_image
=======
    existing = db.query(Project).filter(Project.name == project.name).first()
    if existing:
        raise Exception("Project already exists")

    db_project = Project(
        name=project.name,
        image=project.image
>>>>>>> 803770a4512ea25f36e8e70d89c573a2e84035d2
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project

def update_project(db: Session, project_id: str, project_update: ProjectUpdate):
    """Update an existing project."""
    db_project = get_project(db, project_id)
    if db_project:
        if project_update.name is not None:
            db_project.name = project_update.name
        if project_update.image is not None:
<<<<<<< HEAD
            final_image = project_update.image
            if final_image and final_image.startswith("data:image"):
                cloudinary_url = upload_base64_image(final_image, folder="projects")
                if cloudinary_url:
                    final_image = cloudinary_url
            db_project.image = final_image
=======
            db_project.image = project_update.image
>>>>>>> 803770a4512ea25f36e8e70d89c573a2e84035d2
            
        db.commit()
        db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: str):
    """Delete a project. This cascades and nullifies dependencies based on the DB model setup."""
    db_project = get_project(db, project_id)
    if db_project:
        db.delete(db_project)
        db.commit()
        return True
    return False
