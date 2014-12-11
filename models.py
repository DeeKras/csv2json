from views import db

class PastedData(db.Model):
    uuid = db.Column(db.String(16), primary_key=True, unique=True)
    data_type = db.Columns(db.String(5))
    data_blob = db.Column(db.Text)

    def __init__(self, uuid, data_type, data_blob):
        self.uuid = uuid
        self.data_type = data_type
        self.data_blob = data_blob

    def __repr__(self):
        return 'PastedData: {}'.format(self.uuid)
