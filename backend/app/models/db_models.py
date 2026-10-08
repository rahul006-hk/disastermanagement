import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, JSON, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class ScenarioDB(Base):
    __tablename__ = "scenarios"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    disaster_type = Column(String, default="Flood")
    severity_level = Column(String, default="Severe")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    active = Column(Boolean, default=True)

class ZoneDB(Base):
    __tablename__ = "zones"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    population = Column(Integer, default=0)
    severity = Column(String, default="Medium")
    critical_needs = Column(JSON, default=dict)  # {"food": 500, "water": 1000, ...}

class WarehouseDB(Base):
    __tablename__ = "warehouses"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    stock = Column(JSON, default=dict)  # {"food": 5000, "water": 10000, ...}

class HospitalDB(Base):
    __tablename__ = "hospitals"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    capacity = Column(Integer, default=100)
    available_beds = Column(Integer, default=20)
    emergency_capability = Column(Boolean, default=True)
    incoming_patients = Column(Integer, default=0)

class ShelterDB(Base):
    __tablename__ = "shelters"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    capacity = Column(Integer, default=500)
    occupancy = Column(Integer, default=100)
    facilities = Column(JSON, default=list)  # ["Medical", "Kitchen"]
    accessibility = Column(String, default="Good")

class VehicleDB(Base):
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # ambulance, relief truck, rescue vehicle
    capacity = Column(Integer, default=100)
    assigned_warehouse = Column(String, ForeignKey("warehouses.id"), nullable=True)
    status = Column(String, default="Available")  # Available, Dispatched, Maintenance

class TeamDB(Base):
    __tablename__ = "teams"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)  # Medical, Search & Rescue, Logistics
    members = Column(Integer, default=5)
    status = Column(String, default="Ready")

class RoadDB(Base):
    __tablename__ = "roads"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    target = Column(String, nullable=False)
    distance_km = Column(Float, nullable=False)
    travel_time_min = Column(Float, nullable=False)
    is_blocked = Column(Boolean, default=False)

class EventDB(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    scenario_id = Column(String, ForeignKey("scenarios.id"), nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    event_type = Column(String, nullable=False)  # RoadBlockage, DemandSpike, ResourceDepletion
    target_id = Column(String, nullable=False)
    details = Column(JSON, default=dict)

class PlanDB(Base):
    __tablename__ = "plans"

    id = Column(String, primary_key=True)
    scenario_id = Column(String, ForeignKey("scenarios.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    priority_order = Column(JSON, default=list)
    allocations = Column(JSON, default=list)
    routes = Column(JSON, default=list)
    assignments = Column(JSON, default=dict)
    validations = Column(JSON, default=dict)
    explanations = Column(JSON, default=list)
