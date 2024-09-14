from sqlalchemy import (
    CHAR,
    Boolean,
    Column,
    DateTime,
    Float,
    JSON,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
metadata = Base.metadata


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



class Rolemaster(Base):
    __tablename__ = "rolemaster"

    id = Column(Integer, primary_key=True)
    rolename = Column(String(20))
    createdate = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey("usermaster.id"))
    last_updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    last_updated_by = Column(ForeignKey("usermaster.id"))
    permission = Column(String(4000))

    usermaster = relationship(
        "Usermaster", primaryjoin="Rolemaster.created_by == Usermaster.id"
    )
    usermaster1 = relationship(
        "Usermaster", primaryjoin="Rolemaster.last_updated_by == Usermaster.id"
    )


class Userrole(Base):
    __tablename__ = "userroles"

    id = Column(Integer, primary_key=True)
    usermasterid = Column(Integer)
    rolemasterid = Column(Integer)
    createdate = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    created_by = Column(ForeignKey("usermaster.id"))
    last_updated = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    last_updated_by = Column(ForeignKey("usermaster.id"))

    usermaster = relationship(
        "Usermaster", primaryjoin="Userrole.created_by == Usermaster.id"
    )
    usermaster1 = relationship(
        "Usermaster", primaryjoin="Userrole.last_updated_by == Usermaster.id"
    )
