import os

SELF_GENERATED_OP_ID = '-agent'

LOG_DIR = 'logs'
ETC_DIR = 'etc'

CONFIG_FILE = 'agent.config'
LOG_FILE = os.path.join(LOG_DIR, 'agent.log')
DB_FILE = os.path.join(ETC_DIR, 'vFenseAgent.db')
