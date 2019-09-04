import hashlib
import aiohttp_jinja2
import os

from aiohttp import web
from aiohttp_session import get_session
from config.common import BaseConfig

from models.post import Post
from models.user import User
from models.comments import Comments
from faceid.FaceIdent_v2 import *


class Index(web.View):

    @aiohttp_jinja2.template('base.html')
    async def get(self):
        conf = self.app['config']
        session = await get_session(self)
        user = {}
        posts = []
        all_users = {}
        if 'user' in session:
            all_users = await User.get_user(db=self.app['db'])
            user = session['user']
            posts = await Post.get_post(db=self.app['db'])
        return dict(conf=conf, user=user, posts=posts, all_users=all_users)


class Profile(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        conf = self.app['config']
        session = await get_session(self)
        user = {}
        posts_user = []
        send_comment = None
        if 'user' in session:
            user = session['user']
            posts_user = await Post.get_post_by_user(db=self.app['db'], user_id=session['user']['_id'])
            send_comment = await Comments.get_send_comments_by_user(db=self.app['db'], user_id=user['_id'])
        return dict(conf=conf, user=user, posts_user=posts_user, send_comment=send_comment)


class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        user = {}
        session = await get_session(self)
        login_photo = screen()

        users = await User.get_user(db=self.app['db'])

        for user in users:
            try:
                photo_user = os.path.join(BaseConfig.static_dir + user['avatar_url'])
            except:
                photo_user = None
            # login_photo = os.path.join(BaseConfig.static_dir + '/photoLogin/decod_image_user403446826629198.jpg')
            try:
                thisUser = ident(photo_user, login_photo)  # login_photo

            except:
                continue

            if thisUser:
                os.remove(login_photo)
                return dict(user=user)
                break

        user = {}
        os.remove(login_photo)
        return dict(user=user)

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        location = self.app.router['login'].url_for()
        email = data['email']
        password = data['password']
        user = await User.get_user_by_email(db=self.app['db'], email=email)

        if user.get('error'):
            location = self.app.router['login'].url_for()
            return web.HTTPFound(location=location)

        if user['password'] == hashlib.sha256(password.encode('utf-8')).hexdigest() or user['password'] == password:
            session['user'] = user

            location = self.app.router['index'].url_for()
            return web.HTTPFound(location=location)

        return web.HTTPFound(location=location)


class Signup(web.View):

    @aiohttp_jinja2.template('signup.html')
    async def get(self):
        return dict()

    async def post(self):
        data = await self.post()
        first_name = data['first_name']

        result = await User.create_new_user(db=self.app['db'], data=data)
        if not result:
            location = self.app.router['signup'].url_for()
            return web.HTTPFound(location=location)

        location = self.app.router['login'].url_for()
        return web.HTTPFound(location=location)


class Logout(web.View):

    async def get(self):
        session = await get_session(self)
        try:
            del session['user']
        except:
            pass

        location = self.app.router['index'].url_for()
        return web.HTTPFound(location=location)


class Banned(web.View):

    async def post(self):
        data = await self.post()
        banned = data['banned']
        user_id = data['user_id']

        if banned == 'True':
            await User.unban_user(db=self.app['db'], user_id=user_id)
        else:
            await User.ban_user(db=self.app['db'], user_id=user_id)

        location = self.app.router['index'].url_for()

        return web.HTTPFound(location=location)


class UserDelete(web.View):

    async def post(self):
        data = await self.post()
        user_id = data['user_id']
        session = await get_session(self)
        users = await User.get_user(db=self.app['db'])

        await User.delete_user(db=self.app['db'], user_id=user_id)

        location = self.app.router['index'].url_for()

        return web.HTTPFound(location=location)


class PostView(web.View):

    @aiohttp_jinja2.template('create_post.html')
    async def get(self):
        session = await get_session(self)
        user = {}
        if 'user' in session:
            user = session['user']
        return dict(user=user)

    async def post(self):
        data = await self.post()
        session = await get_session(self)
        photo = data['photo']
        try:
            with open(os.path.join(BaseConfig.static_dir + '\\photo\\', photo.filename), 'wb') as f:
                content = photo.file.read()
                f.write(content)

            if 'user' in session and data['message']:
                await Post.create_post_with_photo(db=self.app['db'], user_id=session['user']['_id'],
                                                  author=session['user']['first_name'], title=data['title'],
                                                  message=data['message'],
                                                  photo='/photo/{}'.format(photo.filename))
                return web.HTTPFound(location=self.app.router['posts'].url_for())

            return web.HTTPForbidden()
        except:
            if 'user' in session and data['message']:
                await Post.create_post(db=self.app['db'], user_id=session['user']['_id'],
                                       author=session['user']['first_name'], title=data['title'],
                                       message=data['message'])
                return web.HTTPFound(location=self.app.router['posts'].url_for())

            return web.HTTPForbidden()


class Posts(web.View):

    @aiohttp_jinja2.template('post.html')
    async def get(self):
        session = await get_session(self)
        user = {}
        all_comment = []
        posts = []
        user_banned = {}
        if 'user' in session:
            user = session['user']
            posts = await Post.get_post(db=self.app['db'])  # user_id=user['_id']
            all_comment = await Comments.get_send_comments(db=self.app['db'])

        return dict(all_comment=all_comment, posts=posts, user=user)

    async def post(self):
        data = await self.post()
        post_id = data['post_id']

        await Post.delete_post_by_id(db=self.app['db'], post_id=post_id)

        return web.HTTPFound(location=self.app.router['posts'].url_for())
