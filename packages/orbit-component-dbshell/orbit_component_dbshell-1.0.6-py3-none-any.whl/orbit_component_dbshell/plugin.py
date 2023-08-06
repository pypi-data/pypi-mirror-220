from orbit_component_base.src.orbit_plugin import ArgsBase
from orbit_component_base.src.orbit_shells import PluginXTerm
from orbit_component_base.src.orbit_decorators import Sentry, check_permission
from loguru import logger as log

class Plugin (PluginXTerm):

    NAMESPACE = 'dbshell'

    @Sentry(check_permission, NAMESPACE, 'User is allowed to open a new terminal session')
    async def on_mount (self, *args, **kwargs):
        return await super().mount(*args, **kwargs)


class Args (ArgsBase):
    pass
