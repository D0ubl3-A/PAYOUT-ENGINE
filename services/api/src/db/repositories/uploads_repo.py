from dataclasses import dataclass
from uuid import uuid4

from psycopg.rows import dict_row

from db.connection import get_conn


@dataclass(frozen=True)
class UploadRecord:
    upload_id: str
    source: str
    filename: str
    content_type: str
    size_bytes: int
    sha256: str
    storage_path: str


def create_upload(record: UploadRecord) -> UploadRecord:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                INSERT INTO uploads (
                  upload_id,
                  source,
                  filename,
                  content_type,
                  size_bytes,
                  sha256,
                  storage_path
                )
                VALUES (%(upload_id)s, %(source)s, %(filename)s, %(content_type)s,
                        %(size_bytes)s, %(sha256)s, %(storage_path)s)
                RETURNING upload_id, source, filename, content_type, size_bytes, sha256, storage_path
                """,
                record.__dict__,
            )
            row = cur.fetchone()
            conn.commit()
            return UploadRecord(**row)


def get_upload(upload_id: str) -> UploadRecord | None:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT upload_id, source, filename, content_type, size_bytes, sha256, storage_path
                FROM uploads
                WHERE upload_id = %(upload_id)s
                """,
                {"upload_id": upload_id},
            )
            row = cur.fetchone()
            return UploadRecord(**row) if row else None


def list_uploads(limit: int = 50) -> list[UploadRecord]:
    with get_conn() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT upload_id, source, filename, content_type, size_bytes, sha256, storage_path
                FROM uploads
                ORDER BY created_at DESC
                LIMIT %(limit)s
                """,
                {"limit": limit},
            )
            rows = cur.fetchall()
            return [UploadRecord(**row) for row in rows]


def new_upload_record(
    source: str,
    filename: str,
    content_type: str,
    size_bytes: int,
    sha256: str,
    storage_path: str,
) -> UploadRecord:
    return UploadRecord(
        upload_id=uuid4().hex,
        source=source,
        filename=filename,
        content_type=content_type,
        size_bytes=size_bytes,
        sha256=sha256,
        storage_path=storage_path,
    )
