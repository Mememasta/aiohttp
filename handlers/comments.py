import aiohttp_jinja2
from aiohttp import web
from aiohttp_session import get_session

from models.comments import Comments
from models.post import Post


class CommentsView(web.View):

    @aiohttp_jinja2.template('comments.html')
    async def get(self):
        session = await get_session(self)

        if 'user' not in session:
            return web.HTTPForbidden()

        posts = await Post.get_post(db=self.app['db'])  # user_id=user['_id']

        user = session['user']

        inbox_comment = await Comments.get_inbox_comments_by_post(db=self.app['db'],
                                                                  post_id=session['user']['_id'])

        send_comment = await Comments.get_send_comments_by_user(db=self.app['db'], user_id=user['_id'])

        all_comment = await Comments.get_send_comments(db=self.app['db'])

        return dict(inbox_comment=inbox_comment, send_comment=send_comment, all_comment=all_comment, posts=posts, user=user)

    async def post(self):
        session = await get_session(self)

        if 'user' not in session:
            return web.HTTPForbidden

        data = await self.post()
        await Comments.create_comment(db=self.app['db'], from_user=session['user']['_id'], author=session['user']['first_name'], to_post=data['to_post'],
                                      message=data['comment_text'])

        location = self.app.router['posts'].url_for()
        return web.HTTPFound(location=location)
