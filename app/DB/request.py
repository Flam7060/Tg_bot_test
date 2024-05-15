from sqlalchemy import select

from app.DB.models import async_session, Group, Service, Appeals


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
    
async def get_service_by_id(service_id, group_id):
    services = await get_services_by_group(group_id)
    for service in services:
        if service.id == service_id:
            return service
    return None

async def save_appeal_to_database(data):
    # Создаем экземпляр объекта Appeals
    appeal = Appeals(
        tg_id=data.get('tg_id'),
        service_id=data.get('service_id'),
        name=data.get('name'),
        phone=data.get('phone'),
        message=data.get('message')
    )

    # Добавляем объект Appeals в базу данных
    async with async_session() as session:
        session.add(appeal)
        await session.commit()