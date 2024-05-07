from sqlalchemy import select

from app.DB.models import async_session, Group, Service


from sqlalchemy import select



 

async def get_groups():
    async with async_session() as session:
        query = select(Group)
        result = await session.execute(query)
        return result.scalars().all()

async def get_services_by_group(group_id):
    async with async_session() as session:
        query = select(Service).filter(Service.group_id == group_id)
        result = await session.execute(query)
        
        return result.scalars().all()