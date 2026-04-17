"""Database module – SQLAlchemy session management

Why PostgreSQL?
---------------
SQLite is sufficient for a single-user prototype but fails under concurrent
load and does not support JSON column indexing efficiently.  PostgreSQL is
chosen because:

* ACID-compliant transactions protect diagnosis records even if the server
  crashes mid-write.
* Native JSONB columns let us store variable-length lists (symptoms,
  recommendations) while still being queryable with SQL predicates.
* Row-level locking allows multiple workers (uvicorn --workers N) to safely
  write feedback records simultaneously without corruption.
* It scales horizontally via read replicas when the user base grows.
* SQLAlchemy's ORM abstracts the dialect so switching back to SQLite for
  local testing requires only a one-line change to DATABASE_URL.

Connection is configured through the DATABASE_URL environment variable
(default: postgresql://farmer:password@localhost:5432/plant_disease_db).
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

__version__ = "0.1.0"


def _build_engine(database_url: str):
	"""Create the SQLAlchemy engine, silently returning None if the DB is unreachable."""
	try:
		engine = create_engine(
			database_url,
			pool_pre_ping=True,   # verify connection before handing it out
			pool_size=5,
			max_overflow=10,
		)
		return engine
	except Exception as exc:
		logger.warning(f"Could not create DB engine: {exc} – running without persistence.")
		return None


def build_session_factory(database_url: str):
	"""Return a sessionmaker bound to the given DB URL, or None on failure."""
	engine = _build_engine(database_url)
	if engine is None:
		return None, None
	SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
	return engine, SessionLocal


def get_db_dependency(session_factory):
	"""Return a FastAPI-compatible generator dependency for the given session factory."""
	def _get_db():
		if session_factory is None:
			yield None
			return
		db = session_factory()
		try:
			yield db
		finally:
			db.close()
	return _get_db
