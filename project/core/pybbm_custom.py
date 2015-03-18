from pybb import permissions, views as pybb_views
from pybb.permissions import DefaultPermissionHandler

class MyPermissionHandler(permissions.DefaultPermissionHandler):
    def may_create_poll(self, user):
        """
        return True if `user` may attach files to posts, False otherwise.
        By default always True
        """
        return False