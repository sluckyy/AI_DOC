"""Persistence. SQLite by default; PostgreSQL when DATABASE_URL says so."""
from __future__ import annotations

import os
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, LargeBinary, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./aidoc.sqlite")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    setting = Column(String, nullable=False)
    language = Column(String, nullable=False, default="en")
    consent = Column(JSON, nullable=False, default=dict)
    is_simulation = Column(Integer, nullable=False, default=1)
    versions = Column(JSON, nullable=False, default=dict)
    state = Column(JSON, nullable=False, default=dict)
    created_at = Column(DateTime, default=utcnow)
    ended_at = Column(DateTime, nullable=True)


class Turn(Base):
    __tablename__ = "turns"
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), index=True, nullable=False)
    order = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    phase = Column(String, nullable=True)
    move = Column(String, nullable=True)
    phrasing_variant_id = Column(String, nullable=True)
    slot_id = Column(String, nullable=True)
    expression = Column(String, nullable=True)
    tone = Column(JSON, nullable=True)
    prosody = Column(JSON, nullable=True)
    asr = Column(JSON, nullable=True)            # N-9: provider, per-utterance confidence, n-best, language, timing
    alert_id = Column(String, nullable=True)
    audio = Column(LargeBinary, nullable=True)
    audio_content_type = Column(String, nullable=True)
    visemes = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utcnow)


class SlotValue(Base):
    __tablename__ = "slot_values"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), index=True, nullable=False)
    slot_id = Column(String, nullable=False)
    module = Column(String, nullable=False)
    value = Column(JSON, nullable=True)
    verbatim = Column(Text, nullable=True)
    state = Column(String, nullable=False)
    source = Column(String, nullable=True)
    turn_id = Column(String, nullable=True)
    written_at = Column(String, nullable=True)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), index=True, nullable=False)
    rule_id = Column(String, nullable=False)
    tier = Column(String, nullable=False)
    route = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    verbatim = Column(Text, nullable=True)
    clock_times = Column(JSON, nullable=True)
    fired_at = Column(String, nullable=True)
    turn_id = Column(String, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)


class Handover(Base):
    __tablename__ = "handovers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), index=True, nullable=False)
    version = Column(Integer, nullable=False, default=1)
    document = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=utcnow)


class Attestation(Base):
    __tablename__ = "attestations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), index=True, nullable=False)
    clinician = Column(String, nullable=False)
    handover_version = Column(Integer, nullable=False)
    diagnosis_block = Column(JSON, nullable=False)
    edits = Column(JSON, nullable=False, default=dict)
    signed_at = Column(DateTime, default=utcnow)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, index=True, nullable=True)
    actor = Column(String, nullable=False)
    action = Column(String, nullable=False)
    detail = Column(JSON, nullable=True)
    at = Column(DateTime, default=utcnow)


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
