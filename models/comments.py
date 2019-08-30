from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime


class Comments:

    @staticmethod
    async def create_comment(db: AsyncIOMotorDatabase, from_user: str, author: str, to_post: str, message: str):
        data = {
            'from_user': ObjectId(from_user),
            'author': author,
            'to_post': ObjectId(to_post),
            'message': message,
            'data_created': datetime.now().strftime("%d-%m-%Y %H:%M")
        }
        await db.comments.insert_one(data)

    @staticmethod
    async def get_inbox_comments_by_post(db: AsyncIOMotorDatabase, post_id: str, limit=20):
        comments = await db.comments.find({'to_post': ObjectId(post_id)}).to_list(limit)
        return comments

    @staticmethod
    async def get_send_comments_by_user(db: AsyncIOMotorDatabase, user_id: str, limit=20):
        comments = await db.comments.find({'from_user': ObjectId(user_id)}).to_list(limit)
        return comments

    @staticmethod
    async def get_send_comments(db: AsyncIOMotorDatabase, limit=20):
        comments = await db.comments.find().to_list(limit)
        return comments
