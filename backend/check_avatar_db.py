from app.db.database import SessionLocal, engine
from app.models.models import User
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_test():
    db = SessionLocal()
    try:
        # 1. Check existing column names
        logger.info("Checking database schema for employees_table...")
        res = db.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'employees_table'")).fetchall()
        columns = [r[0] for r in res]
        logger.info(f"Available columns: {columns}")
        
        # 2. Try identifying Sooraj
        sooraj = db.query(User).filter(User.employee_id == '2026018').first()
        if sooraj:
            logger.info(f"Sooraj found. UUID: {sooraj.id}. Current Avatar: {sooraj.avatar}")
            
            # 3. Try manual update
            test_url = "https://res.cloudinary.com/dv1sih7vk/image/upload/v1741346387/sample.jpg"
            logger.info(f"Attempting manual update to: {test_url}")
            sooraj.avatar = test_url
            db.commit()
            db.refresh(sooraj)
            logger.info(f"Verification after commit: {sooraj.avatar}")
        else:
            logger.warning("Sooraj (2026018) not found in DB.")
            
    except Exception as e:
        logger.error(f"DB Test Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_test()
