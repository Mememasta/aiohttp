from handlers.base import Index, Login, Signup, Logout, PostView, Posts, Profile, Banned, UserDelete
from handlers.avatar import Avatar, Screen
from handlers.comments import CommentsView, CommentsDel

from config.common import BaseConfig


def setup_routes(app):
    app.router.add_get('/', Index.get, name='index')
    app.router.add_get('/user', Profile.get, name='user')
    app.router.add_get('/login', Login.get, name='login')
    app.router.add_post('/login', Login.post)
    app.router.add_get('/signup', Signup.get, name='signup')
    app.router.add_post('/signup', Signup.post)
    app.router.add_get('/logout', Logout.get, name='logout')
    app.router.add_post('/delete_user', UserDelete.post, name='delete_user')
    app.router.add_post('/banned', Banned.post, name='banned')
    app.router.add_post('/save_avatar', Avatar.post, name='save_avatar')
    app.router.add_get('/add_post', PostView.get, name='add_post')
    app.router.add_post('/add_post', PostView.post)
    app.router.add_post('/delete_post', Posts.post, name='delete_post')
    app.router.add_get('/posts', Posts.get, name='posts')
    app.router.add_post('/screen', Screen.post, name='screen')

    app.router.add_get('/comments', CommentsView.get, name='comments')
    app.router.add_post('/send_comment', CommentsView.post, name='send_comment')
    app.router.add_post('/delete_comment', CommentsDel.post, name='delete_comment')

def setup_static_routes(app):
    app.router.add_static('/static/', path=BaseConfig.static_dir, name='static')
