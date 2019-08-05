from platform import system
import os


__dbName__ = 'pvault.db'
__dbPath__ = ''
__ver__ = "1.0.0"

if system() == "Windows":
    __dbPath__ = os.path.join(os.getenv('APPDATA'), __dbName__)

if system() == "Linux":
    __dbPath__ = os.path.join(os.getenv('HOME'), 'bin', __dbName__)
