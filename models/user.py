import hashlib
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class User:

    def __init__(self):
        pass

    @staticmethod
    async def get_user_by_email(db: AsyncIOMotorDatabase, email: str):
        user = await db.users.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
            return user
        else:
            return dict(error='User with email {} not found'.format(email))

    @staticmethod
    async def get_user_by_id(db: AsyncIOMotorDatabase, user_id: str):
        user = await db.users.find_one({'_id': ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
            return user
        else:
            return dict(error='User with id {} not found'.format(user_id))

    @staticmethod
    async def get_user(db: AsyncIOMotorDatabase, limit=20):
        user = await db.users.find().to_list(limit)
        return user

    @staticmethod
    async def create_new_user(db: AsyncIOMotorDatabase, data):
        email = data['email']
        first_name = data['first_name']

        user = await db.users.find_one({'email': email})
        if user:
            return dict(error='user with email {} exist'.format(email))

        user_first_name = await db.users.find_one({'first_name': first_name})
        if user_first_name:
            return dict(error='admin already created')

        if data['first_name'] == 'admin' and data['last_name'] and data['password']:
            data = dict(data)
            data['password'] = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
            data['privilege'] = 'admin'
            data['banned'] = 'False'
            result = await db.users.insert_one(data)
            return result

        elif data['first_name'] and data['last_name'] and data['password']:
            data = dict(data)
            data['password'] = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
            data['privilege'] = 'user'
            data['banned'] = 'False'
            result = await db.users.insert_one(data)
            return result
        else:
            return dict(error='Missing user data parameters')


    @staticmethod
    async def ban_user(db: AsyncIOMotorDatabase, user_id: str):
        if user_id:
            db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'banned': 'True'}})

    @staticmethod
    async def unban_user(db: AsyncIOMotorDatabase, user_id: str):
        if user_id:
            db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'banned': 'False'}})

    @staticmethod
    async def delete_user(db: AsyncIOMotorDatabase, user_id: str):
        if user_id:
            db.users.delete_one({'_id': ObjectId(user_id)})

    @staticmethod
    async def save_avatar_url(db: AsyncIOMotorDatabase, user_id: str, url: str):
        if url and user_id:
            db.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'avatar_url': url}})
