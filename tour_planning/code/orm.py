from sqlalchemy import ForeignKey,Column, VARCHAR, Date, SmallInteger,Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



Base = declarative_base()

class Tour(Base):
    """Tabelle für Touren."""
    __tablename__ = 'tour'

    tour_id = Column(Integer,primary_key=True, autoincrement=True)
    address_id = Column(SmallInteger, ForeignKey('address.address_id'))
    client_id = Column(SmallInteger, ForeignKey('client.client_id'))
    date = Column(Date)
    kolonne_type = Column(VARCHAR(255))
    private = Column(VARCHAR(225))
    further_info = Column(VARCHAR(255))
    zeitbedarf = Column(Numeric(3,2))

    client = relationship("Client", back_populates="tours")
    address = relationship("Address")


    def __repr__(self):
        """Gibt eine lesbare Repräsentation der Tour-Tabelle zurück."""
        return f"<TourTable(id={self.tour_id}, kolonne_type={self.kolonne_type})>"

class Address(Base):
    """Tabelle für Adressen."""
    __tablename__ = 'address'

    address_id = Column(Integer, primary_key=True, autoincrement=True)
    strasse = Column(VARCHAR(255))
    hausnr = Column(VARCHAR(20))
    plz = Column(Integer)
    ort = Column(VARCHAR(100))

class Client(Base):
    """Tabelle für Kunden."""
    __tablename__ = 'client'

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    firmenname = Column(VARCHAR(255))
    
    tours = relationship("Tour")

