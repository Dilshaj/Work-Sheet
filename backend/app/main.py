import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.config import settings
from app.db.database import get_db, test_database_connection, engine, Base
from app.routes import auth, employees, projects, tasks, attendance, dashboard, profile, offer_letter, employee_leaves

import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Database...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database schemas verified.")

        from app.db.database import SessionLocal
        from app.models.models import User
        from app.utils.security import get_password_hash

        db = SessionLocal()
        try:
            admin_eid = "ADMIN-001"

            admin_user = db.query(User).filter(User.role == "admin").first()

            if admin_user:
                logger.info("Found existing admin user, verifying configuration...")
                admin_user.employee_id = admin_eid
                db.commit()
                logger.info("Admin user verified.")
            else:
                logger.info("Creating default admin user...")
                new_admin = User(
                    name="Admin",
                    employee_id=admin_eid,
                    email="dilshajceo@dilshajinfotech.tech",
                    password_hash=get_password_hash("admin@123"),
                    role="admin",
                    is_first_login=False
                )
                db.add(new_admin)
                db.commit()
                logger.info("Default admin user created.")
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error executing schema verification: {e}")
    yield
    logger.info("Shutting down API Service...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for EduProva task and employee management system.",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ✅ STATIC FOLDER
if not os.path.exists("static"):
    os.makedirs("static")

app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔥🔥 NEW: UPLOADS FOLDER (IMPORTANT)
if not os.path.exists("uploads"):
    os.makedirs("uploads")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ ROUTES
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(employees.router, prefix="/api", tags=["Employees"])
app.include_router(projects.router, prefix="/api", tags=["Projects"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(attendance.router, prefix="/api", tags=["Attendance"])
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(profile.router, prefix="/api", tags=["User/Employee Profile"])
app.include_router(offer_letter.router, prefix="/api", tags=["Offer Letter"])
app.include_router(employee_leaves.router, prefix="/api", tags=["Employee Leaves"])

# ✅ ROOT
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the EduProva API. Server is running.", "version": "1.0.0"}

# ✅ HEALTH
@app.get("/api/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

# ✅ DB HEALTH
@app.get("/api/health/db", tags=["Health"])
def health_check_db(db: Session = Depends(get_db)):
    is_connected = test_database_connection()
    if is_connected:
        try:
            db.execute(text("SELECT 1"))
            return {
                "status": "success",
                "message": "Successfully connected to SQL Server Database."
            }
        except Exception as e:
            logger.error(f"Database query execution failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Query execution failed."
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection failed."
        )
