from models import Management, db
from app import app

#create tables
db.drop_all()
db.create_all()

Management.query.delete()

#Add new management companies
m1 = Management(company_name='Ranco', contact='212-555-5555')
m2 = Management(company_name='B&H', contact='718-555-1234')
m3 = Management(company_name='Gold', contact='Rena 718-123-4567')

db.session.add_all([m1, m2, m3])
db.session.commit()