
from nwebclient import base as b

class DocUi(b.Base):
    def __init__(self):
        super().__init__()
    def onOwnerChanged(self, newOnwer):
        pass
    def toHtml(self, params={}):
        return "NWeb Doc Serv"
