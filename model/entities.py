from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from database import connector

class Usuario(connector.Manager.Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, Sequence('usuario_id_seq'), primary_key=True)
    nombre = Column(String(100))
    apellidos = Column(String(100))
    representante = Column(Boolean)
    celular = Column(String(10))
    correo = Column(String(100))  
    contrasenha = Column(String(100))

class Albergue(connector.Manager.Base):
    __tablename__ = 'albergues'
    id = Column(Integer, Sequence('albergue_id_seq'), primary_key=True)
    admin_id = Column(Integer, ForeignKey('usuarios.id'))
    nombre = Column(String(100))
    anios = Column(Integer)
    direccion = Column(String(100))
    urbanizacion = Column(String(100))
    distrito = Column(String(100))
    ciudad = Column(String(100))
    departamento = Column(String(100))
    tamanio = Column(Float)
    material = Column(String(100))
    gasto = Column(Float)
    pertenencia = Column(Boolean)
    voluntarios = Column(Integer)
    albergan = Column(String(100))
    num_gatos = Column(Integer)
    acep_donaciones = Column(Boolean)
    acep_apoyo = Column(Boolean)
    banco_name = Column(String(100))
    banco_number = Column(String(100))
    banco_cci = Column(String(100))
    facebook = Column(String(100))
    instagram = Column(String(100))
    correo = Column(String(100))
    otro_contacto = Column(String(100))
    admin = relationship(Usuario, foreign_keys=[admin_id])

class Gato(connector.Manager.Base):
    __tablename__ = 'gatos'
    id = Column(Integer, Sequence('gato_id_seq'), primary_key=True)
    albergue_id = Column(Integer, ForeignKey('albergues.id'))
    nombre = Column(String(100))
    img = Column(String(200))
    edad = Column(Integer)
    adopcion = Column(Boolean)
    albergues_from = relationship(Albergue, foreign_keys=[albergue_id])

class Recomendacion(connector.Manager.Base):
    __tablename__ = 'recomendaciones'
    id = Column(Integer, Sequence('recomendacion_id_seq'), primary_key=True)
    albergue_id = Column(Integer, ForeignKey('albergues.id'))    
    reco = Column(String(420))
    comentarios = Column(String(420))
    albergues_from = relationship(Albergue, foreign_keys=[albergue_id])

class Contacto(connector.Manager.Base):
    __tablename__ = 'contactos'
    id = Column(Integer, Sequence('contacto_id_seq'), primary_key=True)
    nombre = Column(String(100))
    apellidos = Column(String(100))
    celular = Column(String(100))
    correo = Column(String(100))
    mensaje = Column(String(420))

