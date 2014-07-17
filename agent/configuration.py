import ConfigParser

import agent.utils.variables as gvars


CONFIG_SECTION = 'agent_config'
INFO_SECTION = 'agent_info'

SERVER_ADDRESS = None
SERVER_PORT = None
AGENT_PORT = None
AGENT_ID = None
TOKEN = None
VIEWS = []
TAGS = []

AGENT_NAME = None
AGENT_VERSION = None
AGENT_DESCRIPTION = None
AGENT_INSTALL_DATE = None

_config = None


def initialize():
    """Initialize all settings variables to be used throughout the agent."""
    global _config

    global AGENT_ID
    global TOKEN
    global SERVER_ADDRESS
    global SERVER_PORT
    global VIEWS
    global TAGS

    global AGENT_NAME
    global AGENT_VERSION
    global AGENT_DESCRIPTION
    global AGENT_INSTALL_DATE

    _config = ConfigParser.ConfigParser()
    _config.read(gvars.CONFIG_FILE)

    AGENT_ID = _config.get(CONFIG_SECTION, 'agentid')
    TOKEN = _config.get(CONFIG_SECTION, 'token')
    SERVER_ADDRESS = int(_config.get(CONFIG_SECTION, 'serveraddress'))
    SERVER_PORT = int(_config.get(CONFIG_SECTION, 'serverport'))

    # If what was loaded for Views and Tags is just an empty strings then leave
    # the default values for Views and Tags (empty list) so that it is sent that
    # way to the server.
    loaded_views = _config.get(CONFIG_SECTION, 'views')
    if loaded_views:
        VIEWS = loaded_views.split(',')

    loaded_tags = _config.get(CONFIG_SECTION, 'tags')
    if loaded_tags:
        TAGS = loaded_tags.split(',')

    AGENT_NAME = _config.get(INFO_SECTION, 'name')
    AGENT_VERSION = _config.get(INFO_SECTION, 'version')
    AGENT_DESCRIPTION = _config.get(INFO_SECTION, 'description')
    AGENT_INSTALL_DATE = _config.get(INFO_SECTION, 'installdate')


def save_settings():
    """Saves the settings to the agent config file."""

    # Lists are strings with commas delimiting the elements in INI files
    views = ','.join(VIEWS)
    tags = ','.join(TAGS)

    _config.set(CONFIG_SECTION, 'agentid', AGENT_ID)
    _config.set(CONFIG_SECTION, 'token', TOKEN)
    _config.set(CONFIG_SECTION, 'serveraddress', SERVER_ADDRESS)
    _config.set(CONFIG_SECTION, 'serverport', SERVER_PORT)
    _config.set(CONFIG_SECTION, 'views', views)
    _config.set(CONFIG_SECTION, 'tags', tags)

    _config.set(INFO_SECTION, 'name', AGENT_NAME)
    _config.set(INFO_SECTION, 'version', AGENT_VERSION)
    _config.set(INFO_SECTION, 'description', AGENT_DESCRIPTION)
    _config.set(INFO_SECTION, 'installdate', AGENT_INSTALL_DATE)

    with open(gvars.CONFIG_FILE, 'w') as _file:
        _config.write(_file)
