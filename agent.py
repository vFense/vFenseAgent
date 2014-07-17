import os
import sys

from agent.core import AgentCore
#from plugins import AgentPlugin


#def load_plugins():
#    """Load all plugins in the plugin folder."""
#    # Hardcoding plugin imports for now
#    import plugins.patcher.patcherplugin as patcher
#
#    plugins = {
#        # TODO: change key to patcher
#        'rv': patcher.PatcherPlugin()
#    }
#
#    #return [p for p in plugins if isinstance(p, AgentPlugin)]
#    return plugins


if __name__ == '__main__':
    #if os.getuid() != 0:
    #    sys.exit("vFense Agent must be run with root privileges.")

    core = AgentCore()
    core.initialize()
    core.start()
    AgentCore().start()
