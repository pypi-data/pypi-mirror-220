



class Document:
    name = ''
    content = ''
    title = ''
    auth_id = 0
    kind = ''
    document_id = 0
    def __init__(self, doc_id, connection):
        self.connection = connection
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
    def ispublic(self):
        return self.auth_id == 0
    def getMetaValue(self, ns, name):
        c = self.connection.cursor()
        c.execute('SELECT value FROM document__meta WHERE document_id = ? AND ns = ? AND name = ?', [self.document_id, ns, name])
        result = c.fetchall()
        for x in result:
            return x[0]
        return ''

class Group:
    def __init__(self, group_id, connection):
        self.connection = connection
        self.group_id = group_id
        # `group`
    def docs(self):
        c = self.connection.cursor()
        c.execute('SELECT document_id FROM document WHERE group_id = ?', [self.group_id])
        res = []
        result = c.fetchall()
        for x in result:
            res.append(Document(x[0], self.connection))
        c.close()
        return res