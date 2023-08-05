from typing import Optional, List, Dict, Any
try:
    from sqlalchemy.orm import Session, sessionmaker
    from sqlalchemy.schema import MetaData, Table
    from sqlalchemy.sql.expression import text, select
    from sqlalchemy.engine import create_engine, Engine
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.engine.row import Row
except ImportError:
    raise ImportError("`sqlalchemy` not installed")

from phi.llm.conversation.storage.base import ConversationStorage
from phi.utils.log import logger


class PgConversationStorage(ConversationStorage):
    def __init__(
        self,
        table_name: str,
        schema: Optional[str] = None,
        db_url: Optional[str] = None,
        db_engine: Optional[Engine] = None,
    ):
        _engine: Optional[Engine] = db_engine
        if _engine is None and db_url is not None:
            _engine = create_engine(db_url)

        if _engine is None:
            raise ValueError("Must provide either db_url or db_engine")

        # Database attributes
        self.table_name: str = table_name
        self.schema: Optional[str] = schema
        self.db_url: Optional[str] = db_url
        self.db_engine: Engine = _engine
        self.metadata: MetaData = MetaData(schema=self.schema)

        # Database session
        self.Session: sessionmaker[Session] = sessionmaker(bind=self.db_engine)

        # Database table for the collection
        self.table: Table = self.get_table()

        if self.schema is not None:
            logger.debug(f"Creating schema: {self.schema}")
            with self.Session() as sess:
                with sess.begin():
                    sess.execute(text(f"create schema if not exists {self.schema};"))
            logger.debug("Schema created")

    def get_table(self) -> Table:
        from sqlalchemy.schema import Column
        from sqlalchemy.types import DateTime, String, BigInteger

        return Table(
            self.table_name,
            self.metadata,
            Column("id", BigInteger, primary_key=True, autoincrement=True),
            Column("user_id", String),
            Column("user_persona", String),
            Column("user_data", postgresql.JSONB),
            Column("is_active", postgresql.BOOLEAN, server_default=text("true")),
            Column("user_chat_history", postgresql.JSONB),
            Column("llm_chat_history", postgresql.JSONB),
            Column("usage_data", postgresql.JSONB),
            Column("created_at", DateTime(timezone=True), server_default=text("now()")),
            Column("updated_at", DateTime(timezone=True), onupdate=text("now()")),
            extend_existing=True,
        )

    def table_exists(self) -> bool:
        from sqlalchemy import inspect

        logger.debug(f"Checking if table exists: {self.table.name}")
        try:
            return inspect(self.db_engine).has_table(self.table.name)
        except Exception as e:
            logger.error(e)
            return False

    def create(self) -> None:
        if not self.table_exists():
            logger.debug(f"Creating table: {self.table_name}")
            self.table.create(self.db_engine)

    def _read(self, session: Session, user_id: str) -> Optional[Row[Any]]:
        stmt = select(self.table)\
            .where(self.table.c.user_id == user_id)\
            .where(self.table.c.is_active == True)
        result = session.execute(stmt).first()
        return result

    def read(self, user_id: str) -> Optional[Dict[str, Any]]:
        with self.Session() as sess:
            with sess.begin():
                existing_row: Optional[Row[Any]] = self._read(sess, user_id)
                return existing_row._asdict() if existing_row is not None else None

    def upsert(
        self,
        user_id: str,
        user_persona: Optional[str] = None,
        user_data: Optional[Dict[str, Any]] = None,
        user_chat_history: Optional[List[Dict[str, Any]]] = None,
        llm_chat_history: Optional[List[Dict[str, Any]]] = None,
        usage_data: Optional[Dict[str, Any]] = None
    ) -> None:
        with self.Session() as sess:
            with sess.begin():
                existing_row: Optional[Row[Any]] = self._read(sess, user_id)
                if existing_row is None:
                    insert_stmt = postgresql.insert(self.table).values(
                        user_id=user_id,
                        user_persona=user_persona,
                        user_data=user_data,
                        user_chat_history=user_chat_history,
                        llm_chat_history=llm_chat_history,
                        usage_data=usage_data,
                    )
                    sess.execute(insert_stmt)
                else:
                    update_stmt = self.table.update()\
                        .where(self.table.c.user_id == user_id)\
                        .values(
                            user_persona=user_persona,
                            user_data=user_data,
                            user_chat_history=user_chat_history,
                            llm_chat_history=llm_chat_history,
                            usage_data=usage_data,
                        )
                    sess.execute(update_stmt)

    def end(self, user_id: str) -> None:
        with self.Session() as sess:
            with sess.begin():
                existing_row: Optional[Row[Any]] = self._read(sess, user_id)
                if existing_row is not None:
                    stmt = self.table.update()\
                        .where(self.table.c.user_id == user_id)\
                        .values(is_active=False)
                    sess.execute(stmt)

    def delete(self) -> None:
        if self.table_exists():
            logger.debug(f"Deleting table: {self.table_name}")
            self.table.drop(self.db_engine)
