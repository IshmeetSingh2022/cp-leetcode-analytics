from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    rating = Column(Integer, default=1200)
 # ✅ NAYA: Codeforces handle store karo taki bar bar type na karna pade
    cf_handle = Column(String, nullable=True)
    
    submissions = relationship(
        "Submission",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    topic_stats = relationship(
        "UserTopicStats",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    daily_stats = relationship(
        "DailyStats",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    rating_record = relationship(
        "UserRating",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
