"""Bounded numeric-table data QC for research assays (no statistical inference).

No column is interpreted as a biological phenotype, treatment response or
clinical outcome. Data rows are never copied into generated reports.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math
from pathlib import Path
from typing import Any

MAX_TABLE_BYTES = 4_000_000
MAX_ROWS = 10_000
MAX_COLUMNS = 32


def audit_numeric_table(path: Path) -> dict[str, Any]:
    if path.stat().st_size > MAX_TABLE_BYTES:
        raise ValueError("numeric-table input exceeds 4MB")
    raw = path.read_bytes()
    if not raw or len(raw) > MAX_TABLE_BYTES or b"\x00" in raw:
        raise ValueError("empty, oversized or binary numeric table")
    try:
        data = raw.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError("numeric table must be UTF-8") from error
    reader = csv.reader(io.StringIO(data, newline=""), strict=True)
    try:
        headers = next(reader)
    except (StopIteration, csv.Error) as error:
        raise ValueError("numeric table has no header") from error
    if not 1 <= len(headers) <= MAX_COLUMNS or any(
        not h or len(h) > 100 or h != h.strip() or "\n" in h or "\r" in h for h in headers
    ) or len(set(headers)) != len(headers):
        raise ValueError("invalid, duplicate or oversized table column names")
    counts = [0] * len(headers)
    missing = [0] * len(headers)
    sums = [0.0] * len(headers)
    means = [0.0] * len(headers)
    m2s = [0.0] * len(headers)
    minimum = [math.inf] * len(headers)
    maximum = [-math.inf] * len(headers)
    row_count = 0
    try:
        for cells in reader:
            if len(cells) != len(headers):
                raise ValueError("ragged numeric table row")
            row_count += 1
            if row_count > MAX_ROWS:
                raise ValueError("numeric table exceeds 10000 rows")
            for i, raw_cell in enumerate(cells):
                value = raw_cell.strip()
                if not value:
                    missing[i] += 1
                    continue
                try:
                    number = float(value)
                except ValueError as error:
                    raise ValueError(f"non-numeric value in column {i + 1}") from error
                if not math.isfinite(number):
                    raise ValueError("NaN or nonfinite numeric measurement")
                counts[i] += 1
                delta = number - means[i]
                means[i] += delta / counts[i]
                m2s[i] += delta * (number - means[i])
                sums[i] += number
                minimum[i] = min(minimum[i], number)
                maximum[i] = max(maximum[i], number)
    except csv.Error as error:
        raise ValueError("invalid CSV syntax") from error
    if not row_count:
        raise ValueError("numeric table requires at least one data row")
    result = []
    for i, name in enumerate(headers):
        c = counts[i]
        sd = math.sqrt(max(0.0, m2s[i] / c)) if c else None
        result.append({
            "column": name, "observed": c, "missing": missing[i],
            "minimum": minimum[i] if c else None,
            "maximum": maximum[i] if c else None,
            "mean": means[i] if c else None,
            "population_stddev": sd,
        })
    if not all(math.isfinite(stat) for column in result for stat in
               (column["minimum"], column["maximum"], column["mean"], column["population_stddev"])
               if stat is not None):
        raise ValueError("overflow in numeric-table summary")
    return {
        "schema_version": "1.0.0", "kind": "NUMERIC_RESEARCH_TABLE_QA",
        "source_sha256": hashlib.sha256(raw).hexdigest(),
        "row_count": row_count, "column_count": len(headers), "columns": result,
        "status": "WARN_MISSING_VALUES" if any(missing) else "PASS",
        "not_verified": [
            "column units or domain semantics",
            "biological or clinical meaning",
            "sample representativeness and batch effects",
            "statistical significance or causal effect",
        ],
    }
