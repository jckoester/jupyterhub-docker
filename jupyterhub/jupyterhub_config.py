# JupyterHub configuration
#
## If you update this file, do not forget to delete the `jupyterhub_data` volume before restarting the jupyterhub service:
##
##     docker volume rm jupyterhub_jupyterhub_data
##
## or, if you changed the COMPOSE_PROJECT_NAME to <name>:
##
##    docker volume rm <name>_jupyterhub_data
##

import os
import sys

## Generic
c.JupyterHub.admin_access = True
c.Spawner.default_url = '/lab'

## Authenticator
from oauthenticator.generic import GenericOAuthenticator

#c.Application.log_level = 'DEBUG'

c.JupyterHub.authenticator_class = GenericOAuthenticator
c.GenericOAuthenticator.client_id = os.environ['OAUTH2_CLIENT_ID']
c.GenericOAuthenticator.client_secret = os.environ['OAUTH2_CLIENT_SECRET']
c.GenericOAuthenticator.token_url = 'https://gymnasium-ditzingen.de/iserv/oauth/v2/token'
c.GenericOAuthenticator.userdata_url = os.environ['OAUTH2_USERDATA_URL']
c.GenericOAuthenticator.userdata_params = {'state': 'state'}
# the next can be a callable as well, e.g.: lambda t: t.get('complex').get('structure').get('username')
#c.GenericOAuthenticator.username_key = 'preferred_username'
c.GenericOAuthenticator.login_service = 'IServ'
c.GenericOAuthenticator.scope = ['openid', 'profile', 'email', 'groups']
c.GenericOAuthenticator.admin_groups = ['Admins', 'admins']
c.GenericOAuthenticator.oauth_callback_url = 'https://jupyter.gymnasium-ditzingen.de/hub/oauth_callback'
c.OAuthenticator.tls_verify = False


# from oauthenticator.oauth2 import OAuthLoginHandler
# from oauthenticator.generic import GenericOAuthenticator
# from tornado.auth import OAuth2Mixin

# # OAuth2 endpoints
# class MyOAuthMixin(OAuth2Mixin):
#     _OAUTH_AUTHORIZE_URL = 'https://gymnasium-ditzingen.de/iserv/oauth/v2/auth' ## Better move this to .env!
#     _OAUTH_ACCESS_TOKEN_URL = 'https://gymnasium-ditzingen.de/iserv/oauth/v2/token'

# class MyOAuthLoginHandler(OAuthLoginHandler, MyOAuthMixin):
#     pass

# # Authenticator configuration
# class MyOAuthAuthenticator(GenericOAuthenticator):
#     login_service = 'IServ'
#     login_handler = MyOAuthLoginHandler
#     userdata_url = 'https://gymnasium-ditzingen.de/iserv/public/oauth/userinfo'
#     token_url = 'https://gymnasium-ditzingen.de/iserv/oauth/v2/token'
#     oauth_callback_url = 'https://jupyter.gymnasium-ditzingen.de/hub/oauth_callback'
#     client_id = os.environ['OAUTH2_CLIENT_ID']      # Your client ID and secret, as provided to you
#     client_secret = os.environ['OAUTH2_CLIENT_SECRET']  # by the OAuth2 service.

# c.JupyterHub.authenticator_class = MyOAuthAuthenticator


## Docker spawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.DockerSpawner.image = os.environ['DOCKER_JUPYTER_CONTAINER']
c.DockerSpawner.network_name = os.environ['DOCKER_NETWORK_NAME']
# See https://github.com/jupyterhub/dockerspawner/blob/master/examples/oauth/jupyterhub_config.py
c.JupyterHub.hub_ip = os.environ['HUB_IP']

# user data persistence
# see https://github.com/jupyterhub/dockerspawner#data-persistence-and-dockerspawner
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan' # THIS NEEDS TO CHANGE?
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { 'jupyterhub-user-{username}': notebook_dir }

# Other stuff
c.Spawner.cpu_limit = 1
c.Spawner.mem_limit = '10G'


## Services
c.JupyterHub.load_roles = [
    {
        "name": "jupyterhub-idle-culler-role",
        "scopes": [
            "list:users",
            "read:users:activity",
            "delete:servers",
            # "admin:users", # if using --cull-users
        ],
        # assignment of role's permissions to:
        "services": ["jupyterhub-idle-culler-service"],
    }
]
c.JupyterHub.services = [
    {
        "name": "jupyterhub-idle-culler-service",
        "command": [
            sys.executable,
            "-m", "jupyterhub_idle_culler",
            "--timeout=3600",
        ],
         "admin": True, # Has to be disabled version>2.0
    }
]

