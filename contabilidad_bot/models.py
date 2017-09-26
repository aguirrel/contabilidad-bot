from sqlalchemy.event import listen
from sqlalchemy import event
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

import datetime
from datetime import timedelta

Base = declarative_base()

'''
class TenantMixin(object):
    _exclude_columns = []
    tenant_id = db.Column(db.String(32), index=True, nullable=False)

    @classmethod
    def query(cls):
        return db.session.query(cls).filter(cls.tenant_id == request.tenant_id)

def tenant_creation_or_update(mapper, connection, target):
    target.tenant_id = request.tenant_id

listen(TenantMixin, 'before_insert', tenant_creation_or_update, propagate=True)
listen(TenantMixin, 'before_update', tenant_creation_or_update, propagate=True)
'''

association_table = Table('gasto_tag', Base.metadata,
    Column('gasto_id', Integer, ForeignKey('gastos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Gasto(Base):
	__tablename__ = 'gastos'
	id = Column(Integer, primary_key=True)
	descripcion = Column(String(250), nullable=False)
	importe = Column(Float, nullable=False)
	chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
	chat = relationship("Chat", back_populates="gastos")
	tags = relationship(
        "Tag",
        secondary=association_table,
        back_populates="gastos")

class Tag(Base):
	__tablename__ = 'tags'
	id = Column(Integer, primary_key=True)
	descripcion = Column(String(250), nullable=False)
	gastos= relationship(
        "Gasto",
        secondary=association_table,
        back_populates="tags")

class Chat(Base):
	__tablename__ = 'chats'
	id = Column(Integer, primary_key=True)
	chat_id = Column(Integer, nullable=False)
	name = Column(String(250), nullable=False)
	gastos = relationship("Gasto", back_populates="chat")

engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(engine)