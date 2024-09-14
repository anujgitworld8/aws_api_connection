from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    JSON,
    LargeBinary,
    text
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class AuditTable(Base):
    __tablename__ = "audit_table"

    id = Column(Integer, primary_key=True)
    request_type = Column(String(200))
    requested_by = Column(String(200))
    request_body = Column(JSON)
    requested_datetime = Column(DateTime)
    response_body = Column(JSON)


class Usermaster(Base):
    __tablename__ = "usermaster"

    id = Column(Integer, primary_key=True)
    username = Column(String(110), nullable=False, unique=True)
    psswrd = Column(String(128))
    useremail = Column(String(320))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey("usermaster.id"))
    last_updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    last_updated_by = Column(ForeignKey("usermaster.id"))
    last_login = Column(DateTime)
    active = Column(String(20))
    fullname = Column(String(1000))
    salt = Column(LargeBinary)
    psswrd_exp_date = Column(DateTime)
    wrong_psswrd_cnt = Column(Integer)

    parent = relationship(
        "Usermaster",
        remote_side=[id],
        primaryjoin="Usermaster.created_by == Usermaster.id",
    )
    parent1 = relationship(
        "Usermaster",
        remote_side=[id],
        primaryjoin="Usermaster.last_updated_by == Usermaster.id",
    )
    roles = relationship("UserRole", back_populates="user")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), unique=True, nullable=False)
    users = relationship("UserRole", back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    permission_name = Column(String(50), unique=True, nullable=False)


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("usermaster.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    user = relationship("Usermaster", back_populates="roles")
    role = relationship("Role", back_populates="users")
