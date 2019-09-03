from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime


class Post:

    @staticmethod
    async def create_post_with_photo(db: AsyncIOMotorDatabase, user_id: str, author: str, title: str, message: str, photo: str):
        data = {
            'user_id': ObjectId(user_id),
            'author': author,
            'title': title,
            'message': message,
            'photo': photo,
            'date_created': datetime.utcnow(),
        }

        await db.posts.insert_one(data)

    @staticmethod
    async def create_post(db: AsyncIOMotorDatabase, user_id: str, author: str, title: str, message: str):
        data = {
            'user_id': ObjectId(user_id),
            'author': author,
            'title': title,
            'message': message,
            'date_created': datetime.utcnow(),
        }

        await db.posts.insert_one(data)

    @staticmethod
    async def get_post(db: AsyncIOMotorDatabase, limit=20):
        posts = await db.posts.find().to_list(limit)
        return posts

    @staticmethod
    async def get_post_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        posts = await db.posts.find({'user_id': ObjectId(user_id)}).to_list(limit)
        return posts



    @staticmethod
    async def delete_post_by_id(db: AsyncIOMotorDatabase, post_id: str):
        if post_id:
            db.posts.delete_one({'_id': ObjectId(post_id)})
