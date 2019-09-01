import base64
import os

from aiohttp import web
from aiohttp_session import get_session
import aiohttp_jinja2
import jinja2

from config.common import BaseConfig
from models.user import User


# from models.login_photo import LoginPhoto


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

            image_name = user['first_name'] + '_' + user['_id'] + '.jpg'
            os.rename(os.path.join(BaseConfig.static_dir + '\\avatars\\', avatar.filename),
                      os.path.join(BaseConfig.static_dir + '\\avatars\\', image_name))

            await User.save_avatar_url(db=self.app['db'], user_id=user['_id'],
                                       url='/avatars/{}'.format(image_name))

        except:
            with open(os.path.join(BaseConfig.static_dir + '/avatars/', avatar.filename), 'wb') as f:
                content = avatar.file.read()
                f.write(content)

            image_name = user['first_name'] + '_' + user['_id'] + '.jpg'
            os.rename(os.path.join(BaseConfig.static_dir + '/avatars/', avatar.filename),
                      os.path.join(BaseConfig.static_dir + '/avatars/', image_name))

            await User.save_avatar_url(db=self.app['db'], user_id=user['_id'],
                                       url='/avatars/{}'.format(image_name))

        location = self.app.router['user'].url_for()
        return web.HTTPFound(location=location)


class Screen(web.View):

    async def post(self):
        data = await self.post()

        log_photo = data['log_photo']

        try:
            with open(os.path.join(BaseConfig.static_dir + '\\photoLogin\\', log_photo.filename), 'wb') as f:
                content = log_photo.file.read()
                image = base64.b64decode(content)
                f.write(image)

            os.remove(os.path.join(BaseConfig.static_dir + '\\photoLogin\\', log_photo.filename))

            # await LoginPhoto.save_photo_url(db=self.app['db'],
            #                                 log_photo='/photoLogin/{}'.format('dec' + log_photo.filename))
        except:
            with open(os.path.join(BaseConfig.static_dir + '/photoLogin/', log_photo.filename), 'wb') as f:
                content = log_photo.file.read()
                image = base64.b64decode(content)
                f.write(image)

            os.remove(os.path.join(BaseConfig.static_dir + '/photoLogin/', log_photo.filename))

        return web.Response(text='200', content_type='text/html')
