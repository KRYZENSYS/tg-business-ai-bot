"""Database export to JSON / CSV."""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


async def export_db(session: AsyncSession, target_dir: str = "exports", fmt: str = "json") -> str:
    """Export every table to a single file and return the path."""
    os.makedirs(target_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(target_dir, f"export_{ts}.{fmt}")

    dump = {}
    for table in Base.metadata.sorted_tables:
        rows = (await session.execute(select(table))).mappings().all()
        dump[table.name] = [dict(r) for r in rows]

    if fmt == "json":
        with open(path, "w", encoding="utf-8") as f:
            json.dump(dump, f, ensure_ascii=False, indent=2, default=str)
    else:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            for tbl, rows in dump.items():
                if not rows:
                    continue
                w.writerow([f"### {tbl}"])
                w.writerow(list(rows[0].keys()))
                for r in rows:
                    w.writerow(list(r.values()))
    return path
