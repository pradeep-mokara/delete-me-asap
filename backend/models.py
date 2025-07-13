from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from .db import Base
import uuid
from datetime import datetime
from backend.config import MAX_RETRIES


class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_id = Column(String, nullable=False)
    app_version_id = Column(String, nullable=False)
    test_path = Column(String, nullable=False)
    target = Column(String, nullable=False)
    priority = Column(Integer, default=0)
    status = Column(String, default="queued")
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=MAX_RETRIES)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

