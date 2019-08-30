from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase


class LoginPhoto:

    @staticmethod
    async def save_photo_url(db: AsyncIOMotorDatabase, log_photo: str):
        data = {
            'log_photo': log_photo
        }

        await db.login_photo.insert_one(data)
