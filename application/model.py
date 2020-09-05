from . import db
import datetime

class rcommand(db.Model):
    __tablename__ = 'rcommand'

    id = db.Column(db.Integer, primary_key=True)
    cmd = db.Column(db.String(2))
    action = db.Column(db.String(1)) 
    rec_date = db.Column(db.DateTime)
    rec_type = db.Column(db.String(1))
    visit_ip = db.Column(db.String(15))

    def __init__(self, cmd, action, rec_type, visit_ip):
        self.cmd = cmd
        self.action = action
        self.rec_type = rec_type
        self.visit_ip = visit_ip
        self.rec_date = datetime.datetime.now() 
        db.session.add(self)
        db.session.commit()