import os
import logging

from typing import Dict, List, Optional

try:
    from airflow.www.security import AirflowSecurityManager as BaseAirflowSecurityManager
except ImportError:
    BaseAirflowSecurityManager = None

try:
    from superset.security import BaseSupersetSecurityManager
except ImportError:
    BaseSupersetSecurityManager = None


from flask_appbuilder.security.manager import BaseSecurityManager as DefaultSecurityManager


logger = logging.getLogger("izroq-auth")


def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)


class IzroqAuthMixin:
    # Izroq workspace id
    @property
    def workspace_id(self) -> str:
        return get_env_variable("IZROQ_WORKSPACE_ID")

    def is_demo_workspace(self) -> bool:
        return bool(self.workspace_id.startswith("demo"))

    def get_izroq_userinfo(self, data):
        email = data.get("email")
        if not email:
            logger.error("OAuth did not return an email address")
            return {}
        user_info = {"username": email, "email": email}
        name = data.get("name")
        given_name = data.get("given_name")
        family_name = data.get("family_name")
        if given_name:
            user_info["first_name"] = given_name
            if family_name:
                user_info["last_name"] = family_name
        elif name:
            user_info["first_name"] = name
        else:
            user_info["first_name"] = user_info["email"]
        user_info["workspace_roles"] = data.get("workspace_roles", {}) or {}
        return user_info

    # this function is taken from the flask appbuild source code
    # flask_appbuilder/security/manager.py:1355
    def auth_user_oauth(self, userinfo):
        """
        Method for authenticating user with OAuth.

        :userinfo: dict with user information
                   (keys are the same as User model columns)
        """
        # extract the username from `userinfo`
        username = userinfo.get("username")

        # If username is empty, go away
        if (username is None) or username == "":
            return None

        # Search the DB for this user
        user = self.find_user(username=username)

        # # If user is not active, go away
        # if user and (not user.is_active):
        #     return None
        
        # check the user's workspace roles
        # first check is if he is even a member of the workspace
        workspace_roles = self._calculate_workspace_roles(userinfo)
        if not workspace_roles:
            # deactivate user if he is not a member of the workspace
            if user:
                user.active = False
                self.update_user(user)
            # go away
            return None

        # If user is not registered, and not self-registration, go away
        if (not user) and (not self.auth_user_registration):
            return None

        # Sync the user's roles and names
        if user:
            user.roles = workspace_roles
            user.active = True
            logger.debug(
                "Calculated new roles for user='{0}' as: {1}".format(
                    username, user.roles
                )
            )
            first_name = userinfo.get("first_name")
            last_name = userinfo.get("last_name")
            if first_name and (first_name != user.first_name):
                user.first_name = first_name
            if last_name and (last_name != user.last_name):
                user.last_name = last_name

        # If the user is new, register them
        if (not user) and self.auth_user_registration:
            user = self.add_user(
                username=username,
                first_name=userinfo.get("first_name", ""),
                last_name=userinfo.get("last_name", ""),
                email=username,
                role=workspace_roles,
            )
            logger.debug("New user registered: {0}".format(user))

            # If user registration failed, go away
            if not user:
                logger.error("Error creating a new OAuth user {0}".format(username))
                return None

        # LOGIN SUCCESS (only if user is now registered)
        if user:
            self.update_user_auth_stat(user)
            return user
        else:
            return None

    # function to calculate workspace roles from the user info dictionary
    def _calculate_workspace_roles(self, user_info: Dict) -> List[str]:
        workspace_roles = user_info["workspace_roles"].get(self.workspace_id)

        # check for demo workspace
        if not workspace_roles and self.is_demo_workspace():
            workspace_roles = user_info["workspace_roles"].get("demo")

        roles = set()
        if not workspace_roles:
            logger.warning("User tried to login but is not a member of the workspace")
            return []

        # now we add the roles from the workspace
        for role in workspace_roles:
            if role.lower() == "admin" or role.lower() == "owner":
                roles.add(self.ADMIN_ROLE)
            elif role.lower() == "contributor":
                roles.add(self.CONTRIBUTOR_ROLE)
            elif role.lower() == "user":
                roles.add(self.USER_ROLE)
            elif role.lower() == "viewer":
                roles.add(self.VIEWER_ROLE)

        # if the user has no roles in the workspace, we add the public role
        if len(roles) == 0:
            logger.warning("User {} tried to login but has no roles in the workspace".format(user_info.get("username")))
            roles.add(self.PUBLIC_ROLE)

        # lookup roles in flask db
        fab_roles = []
        for role in roles:
            fab_role = self.find_role(role)
            if fab_role:
                fab_roles.append(fab_role)
            else:
                logger.warning("Can't find role: {0}".format(role))

        return fab_roles


class IzroqSecurityManager(DefaultSecurityManager, IzroqAuthMixin):
    ADMIN_ROLE = "Admin"
    CONTRIBUTOR_ROLE = "Alpha"
    USER_ROLE = "User"
    VIEWER_ROLE = "Viewer"
    PUBLIC_ROLE = "Public"

    # return a user info dictionary from an OAuth provider response
    # - we need username and email at least (username is used for lookup)
    # - first_name and last_name are optional
    # - role is optional (default is set in AUTH_USER_REGISTRATION_ROLE)
    # - if we return an empty dictionary, the user is not allowed to login
    def get_oauth_user_info(self, provider, resp):
        if provider == "izroq":
            me = self.appbuilder.sm.oauth_remotes[provider].get("/oauth/whoami")
            data = me.json()
            return self.get_izroq_userinfo(data)
        return super(DefaultSecurityManager, self).get_oauth_user_info(provider, resp)


if BaseSupersetSecurityManager:
    class SupersetSecurityManager(IzroqAuthMixin, BaseSupersetSecurityManager):
        ADMIN_ROLE = "Admin"
        CONTRIBUTOR_ROLE = "Alpha"
        USER_ROLE = "Alpha"
        VIEWER_ROLE = "Viewer"
        PUBLIC_ROLE = "Public"

        # return a user info dictionary from an OAuth provider response
        # - we need username and email at least (username is used for lookup)
        # - first_name and last_name are optional
        # - role is optional (default is set in AUTH_USER_REGISTRATION_ROLE)
        # - if we return an empty dictionary, the user is not allowed to login
        def get_oauth_user_info(self, provider, resp):
            if provider == "izroq":
                me = self.appbuilder.sm.oauth_remotes[provider].get("/oauth/whoami")
                data = me.json()
                return self.get_izroq_userinfo(data)
            return super(BaseSupersetSecurityManager, self).get_oauth_user_info(provider, resp)

        # override the sync_roles function to not sync the roles from the user info
        def sync_role_definitions(self) -> None:
            super(BaseSupersetSecurityManager, self).sync_role_definitions()

            # add a new viewer role
            viewer_role = self.add_role("Viewer")
            self.copy_role(role_from_name="Gamma", role_to_name="Viewer")
            pv = self.find_permission_view_menu("all_datasource_access", "all_datasource_access")
            viewer_role.permissions.append(pv)
            pv2 = self.find_permission_view_menu("can_explore_json", "Superset")
            viewer_role.permissions.append(pv2)
            pv3 = self.find_permission_view_menu("can_explore", "Superset")
            viewer_role.permissions.append(pv3)
            pv4 = self.find_permission_view_menu("can_samples", "Datasource")
            viewer_role.permissions.append(pv4)
            self.get_session.merge(viewer_role)
            self.get_session.commit()


if BaseAirflowSecurityManager:
    class AirflowSecurityManager(IzroqAuthMixin, BaseAirflowSecurityManager):
        ADMIN_ROLE = "Admin"
        CONTRIBUTOR_ROLE = "User"
        USER_ROLE = "User"
        VIEWER_ROLE = "Viewer"
        PUBLIC_ROLE = "Public"

        # return a user info dictionary from an OAuth provider response
        # - we need username and email at least (username is used for lookup)
        # - first_name and last_name are optional
        # - role is optional (default is set in AUTH_USER_REGISTRATION_ROLE)
        # - if we return an empty dictionary, the user is not allowed to login
        def get_oauth_user_info(self, provider, resp):
            if provider == "izroq":
                me = self.appbuilder.sm.oauth_remotes[provider].get("/oauth/whoami")
                data = me.json()
                return self.get_izroq_userinfo(data)
            return super(BaseAirflowSecurityManager, self).get_oauth_user_info(provider, resp)