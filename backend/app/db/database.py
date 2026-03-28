import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from app.core.config import settings

# Setup basic logging to monitor DB issues
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the SQLAlchemy engine for SQL Server
# fast_executemany=True is highly recommended when using pyodbc for batch performance
# pool_pre_ping=True verifies the connection before executing allowing recovery from dropped connections
try:
    engine = create_engine(
        settings.get_database_url,
        fast_executemany=True, 
        pool_pre_ping=True,
        pool_recycle=3600
    )
    logger.info("Successfully configured the SQL Server SQLAlchemy engine.")
except Exception as e:
    logger.error(f"Error configuring database engine setup: {e}")
    # We do not strictly fail here to allow the process to boot and fail gracefully during health checks.

# Create Customized Session Object
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for mapping Pydantic schema later down the road
Base = declarative_base()

# FastAPI Dependency for injecting database sessions securely into endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() # Always close to release resources back to pool

def test_database_connection():
    """Utility function to forcefully verify the backend can reach the SQL Server instance"""
    try:
        with engine.connect() as connection:
            logger.info("Successfully verified connection to the SQL Server Database instance.")
            return True
    except OperationalError as e:
        logger.error(f"SQL Server connection failed due to OperationalError: {e}")
        return False
    except Exception as e:
        logger.error(f"An unexpected Python exception during Database initialization: {e}")
        return False
