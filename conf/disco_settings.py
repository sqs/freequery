import os

DISCO_USER = "disco"

# --
# -- You can modify these directories as you wish
# --

DISCO_HOME = "/usr/local/lib/disco/"
DISCODEX_HOME = "/usr/local/lib/disco/discodex/"

# Root directory for Disco data.
DISCO_ROOT = "/srv/disco/"

# Root directory for Disco logs.
DISCO_LOG_DIR = "/srv/disco/log"

# Root directory for the Disco PID file.
DISCO_PID_DIR = os.path.join(DISCO_ROOT, "run/")

# --
# -- Variables below this line rarely need to be modified
# --

# disco_worker is installed by setuptools to the system default bin directory
DISCO_WORKER = "/usr/local/bin/disco-worker"

DISCO_MASTER_HOME = DISCO_HOME

# Lighttpd for master and nodes runs on this port.
# disco://host URIs are mapped to http://host:DISCO_PORT.
DISCO_PORT = 8989

# Miscellaneous flags:
# - nocurl: use httplib instead of pycurl even if pycurl is available
DISCO_FLAGS = "nocurl"

DDFS_TAG_MIN_REPLICAS = 1
DDFS_TAG_REPLICAS     = 1
DDFS_BLOB_REPLICAS    = 1
