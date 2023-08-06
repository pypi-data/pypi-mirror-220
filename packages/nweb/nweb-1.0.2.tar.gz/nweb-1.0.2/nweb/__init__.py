
import json
from os.path import exists
import sqlite3
from sqlite3.dbapi2 import Cursor
from mysql import connector
import hashlib
import datetime

from nwebclient import base
from nwebclient import util


def loadConfig():
    cfg_files = ['./nweb.json', '/etc/nweb.json']
    for cfg_file in cfg_files:
        if exists(cfg_file):
            with open(cfg_file) as f:
                return json.load(f)
    return None


class NWeb(base.Base):
    cfg = {}
    c = None

    def __init__(self, cfg=None, connection=None):
        if cfg is None:
            cfg = loadConfig()
        self.cfg = cfg
        if connection is None:
            self.connection = nw_dbconnect(cfg)
        else:
            self.connection = connection

    def select(self, sql, params):
        if self.c is not None:
            self.c.close()
        self.c = self.connection.cursor()
        self.c.execute(sql, params)
        result = self.c.fetchall()
        return result

    def select_one(self, sql, params):
        res = self.select(sql, params)
        for x in res:
            return x
        return []

    def select_scalar(self, sql, params, default=None):
        res = self.select(sql, params)
        for x in res:
            return x[0]
        return default

    def setting(self, name):
        """ Einstellung aus system__setting """
        return self.select_scalar("SELECT value FROM system__setting WHERE name = ?", [name], None)

    def get(self, name, default=None):
        if name in self.cfg:
            return self.cfg[name]
        else:
            return default

    def __getitem__(self, name):
        return self.get(name, None)

    def __getattr__(self, name):
        return self.get(name, None)

    def __call__(self, *args, **kwargs):
        return "nweb request"

    def rootGroups(self):
        c = self.connection.cursor()
        c.execute('SELECT group_id FROM `group` WHERE parent_id = 0')
        result = c.fetchall()
        res = []
        for x in result:
            g = Group(x[0], self)
            self.addChild(g)
            res.append(g)
        return res


class TableRow(base.Base):

    def __init__(self, table_name, row_id, connection):
        self.table_name = table_name
        self.id = row_id
        if isinstance(connection, NWeb):
            self.connection = connection.connection
        else:
            self.connection = connection

    def __str__(self):
        return self.table_name+'('+str(self.id)+')'


class Document(TableRow):
    name = ''
    content = ''
    title = ''
    auth_id = 0
    kind = ''
    document_id = 0

    def __init__(self, doc_id, connection):
        super().__init__('document', doc_id, connection)
        self.document_id = doc_id
        if isinstance(doc_id, int) or doc_id.isnumeric():
            c = connection.cursor()
            c.execute('SELECT name,auth_id,content,title,kind FROM document WHERE document_id = ?', [doc_id])
            result = c.fetchall()
            for x in result:
                self.name    = str(x[0])
                self.auth_id = x[1]
                self.content = str(x[2])
                self.title   = str(x[3])
                self.kind    = str(x[4])
            c.close()

    def get(self, name: str, default=None):
        if '.' in name:
            a = name.split('.')
            return self.getMetaValue(a[0], a[1])
        else:
            return default

    def __getitem__(self, name):
        return self.get(name, None)

    def ispublic(self):
        return self.auth_id == 0

    def is_image(self):
        return self.kind == 'image'

    def getMetaValue(self, ns: str, name: str):
        c = self.connection.cursor()
        params = [self.document_id, ns, name]
        c.execute('SELECT value FROM document__meta WHERE document_id = ? AND ns = ? AND name = ?', params)
        for x in c.fetchall():
            return x[0]
        return ''


class Group(TableRow):

    def __init__(self, group_id, connection):
        super().__init__('`group`', group_id, connection)
        self.group_id = group_id
        # `group`

    def __str__(self):
        return 'Group('+str(self.group_id)+')'

    def docs(self):
        c = self.connection.cursor()
        c.execute('SELECT document_id FROM document WHERE group_id = ?', [self.group_id])
        res = []
        result = c.fetchall()
        for x in result:
            d = Document(x[0], self.connection)
            self.addChild(d)
            res.append(d)
        c.close()
        return res


nweb_cfg = loadConfig()

def nw_dbconnect(cfg=None):
    """
      Liefert eine Python-DBAPI Connection zurueck
    """
    if cfg is None:
        cfg = nweb_cfg
    if 'DB_HOST' in cfg:
        h = cfg['DB_HOST']
        u = cfg['DB_USER']
        return connector.connect(host=h, user=u, password=cfg['DB_PASSWORD'], database=cfg['DB_NAME'])
    elif 'DB_SQLITE' in cfg:
        return sqlite3.connect(cfg['DB_SQLITE'])
    else:
        raise Exception("No Database Configuration")


def nw_gtoken():
    hstr = datetime.datetime.now().strftime('%Y-%m-%d') + nweb_cfg['V4_INNER_SECRET']
    return hashlib.md5(hstr.encode()).hexdigest()

if __name__ == '__main__':
    args = util.Args()
    if args.help_requested():
        print("nweb python")