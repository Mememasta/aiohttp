import os

from aiohttp import web
from aiohttp_session import get_session

from config.common import BaseConfig

from models.user import User
from models.login_photo import LoginPhoto


class Avatar(web.View):

    async def post(self):

        session = await get_session(self)
        if 'user' not in session:
            return web.HTTPForbidden()

        user = session['user']
        data = await self.post()
        avatar = data['avatar']

        try:
            with open(os.path.join(BaseConfig.static_dir + '\\avatars\\', avatar.filename), 'wb') as f:
                content = avatar.file.read()
                f.write(content)

            await User.save_avatar_url(db=self.app['db'], user_id=user['_id'],
                                       url='/avatars/{}'.format(avatar.filename))

        except:
            pass

        location = self.app.router['user'].url_for()
        return web.HTTPFound(location=location)


class Screen(web.View):

    async def post(self):
        data = await self.post()
        log_photo = data['log_photo']
        try:
            with open(os.path.join(BaseConfig.static_dir + '\\photoLogin\\', log_photo.filename), 'wb') as f:
                content = log_photo.file.read()
                f.write(content)

            await LoginPhoto.save_photo_url(db=self.app['db'], log_photo='/photoLogin/{}'.format(log_photo.filename))
        except:
            return web.HTTPForbidden()

        return web.HTTPFound(location=self.app.router['login'].url_for())
