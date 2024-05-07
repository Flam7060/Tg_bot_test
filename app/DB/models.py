from sqlalchemy.ext.asyncio import create_async_engine,AsyncAttrs,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger



engine = create_async_engine(url="sqlite+aiosqlite:///mydatabase.db")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass



class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey("groups.id"))
    name = Column(String(155),nullable=False)
    description = Column(String(255),nullable=True)
    price = Column(Integer,nullable=False)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    name = Column(String(155),nullable=False)

class Purchase(Base):
    __tablename__ = "purchases"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger,nullable=False)
    service_id = Column(ForeignKey("services.id"))
    date = Column(DateTime,default=datetime.utcnow)


class Logs(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)
    message = Column(String(255))
    date = Column(DateTime,default=datetime.utcnow)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
