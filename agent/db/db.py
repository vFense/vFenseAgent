import os
import sys
import sqlite3 as lite

import agent.utils.variables as gvars

conn = None


def initialize():
    """Initialize the database and any global variables for later use."""
    global conn

    if not os.path.exists(gvars.DB_FILE):
        open(gvars.DB_FILE, 'w+').close()

    conn = lite.connect(gvars.DB_FILE)
