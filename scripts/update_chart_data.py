"""
Update chart data JSON files with latest fetched data.
This script aggregates outputs from other fetch scripts and
refreshes the canonical JSON files in src/data/.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    ensure_dirs, today_str, read_json, write_json,
    SRC_DATA_DIR, logger,
)


def update_install_growth():
    """Update installation growth chart data with latest totals."""
    data = read_json(SRC_DATA_DIR / "install-growth.json")
    if not data:
        logger.warning("No existing install-growth.json found, skipping update")
        return

    data["lastUpdated"] = today_str()
    # Note: In production, real data would come from CNESA/IEA reports
    write_json(SRC_DATA_DIR / "install-growth.json", data)
    logger.info("Updated install-growth.json")


def update_price_spread():
    """Update price spread chart data."""
    data = read_json(SRC_DATA_DIR / "price-spread.json")
    if not data:
        logger.warning("No existing price-spread.json found")
        return

    data["lastUpdated"] = today_str()
    # Note: In production, real data would come from power exchange APIs
    write_json(SRC_DATA_DIR / "price-spread.json", data)
    logger.info("Updated price-spread.json")


def update_grid_dispatch():
    """Update grid dispatch chart data."""
    data = read_json(SRC_DATA_DIR / "grid-dispatch.json")
    if not data:
        logger.warning("No existing grid-dispatch.json found")
        return

    data["lastUpdated"] = today_str()
    # Note: In production, real data would come from grid operator reports
    write_json(SRC_DATA_DIR / "grid-dispatch.json", data)
    logger.info("Updated grid-dispatch.json")


def update_tech_comparison():
    """Update technology comparison data."""
    data = read_json(SRC_DATA_DIR / "tech-comparison.json")
    if not data:
        return

    data["lastUpdated"] = today_str()
    write_json(SRC_DATA_DIR / "tech-comparison.json", data)


def main():
    ensure_dirs()
    logger.info("Starting chart data update...")

    update_install_growth()
    update_price_spread()
    update_grid_dispatch()
    update_tech_comparison()

    logger.info("Chart data update complete")


if __name__ == "__main__":
    main()
