# from redis.asyncio import asyncio

# async def create_redis_connection():
#     return await asyncio.Redis(host='localhost', port=6379, db=1)
# # Функция для получения групп товаров из базы данных
# async def get_groups_cached(redis):
#     cached_data = await redis.get('groups')
#     if cached_data:
#         return json.loads(cached_data)
#     else:
#         groups = await get_groups()
#         await redis.set('groups', json.dumps(groups))
#         return groups

# # Функция для получения услуг по ID группы из кэша Redis
# async def get_services_by_group_cached(redis, group_id):
#     cache_key = f'services_{group_id}'
#     cached_data = await redis.get(cache_key)
#     if cached_data:
#         return json.loads(cached_data)
#     else:
#         services = await get_services_by_group(group_id)
#         await redis.setex(cache_key, 3600, json.dumps(services))
#         return services

# # Создание подключения к Redis и вызов функций с использованием этого подключения
# async def main_redis():
#     redis = await create_redis_connection()
#     groups = await get_groups_cached(redis)
#     services = await get_services_by_group_cached(redis, group_id)
#     print(groups)
#     print(services)
#     redis.close()
#     await redis.wait_closed()

