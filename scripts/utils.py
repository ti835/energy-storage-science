"""
Shared utilities for energy storage automation scripts.
Handles HTTP client, LLM API calls, file I/O, and logging.
"""

import json
import os
import sys
import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

import httpx

# ---- Paths ----
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DATA_DIR = PROJECT_ROOT / "src" / "data"
SRC_CONTENT_DIR = PROJECT_ROOT / "src" / "content"
REPORTS_DIR = SRC_CONTENT_DIR / "reports"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
CACHE_DIR = SCRIPTS_DIR / ".cache"

# Beijing timezone
TZ_BEIJING = timezone(timedelta(hours=8))

# ---- Logging ----
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("energy-storage-automation")


def ensure_dirs():
    """Ensure required directories exist."""
    SRC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)


def today_str() -> str:
    """Return today's date in Beijing time as YYYY-MM-DD."""
    return datetime.now(TZ_BEIJING).strftime("%Y-%m-%d")


def today_date():
    """Return today's date object in Beijing time."""
    return datetime.now(TZ_BEIJING).date()


def read_json(filepath: Path) -> dict:
    """Read and parse a JSON file. Returns empty dict if file not found."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to read {filepath}: {e}")
        return {}


def write_json(filepath: Path, data: dict):
    """Write data to a JSON file atomically (write to temp, then rename)."""
    tmp_path = filepath.with_suffix(".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp_path.replace(filepath)
    logger.info(f"Wrote {filepath}")


def write_markdown(filepath: Path, content: str):
    """Write markdown content to file."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info(f"Wrote {filepath}")


def cache_key(*args) -> str:
    """Generate a cache key from arguments."""
    raw = "|".join(str(a) for a in args)
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def cached_fetch(url: str, ttl_hours: int = 6, **kwargs) -> Optional[str]:
    """
    Fetch a URL with disk-based caching.
    If a cached response exists and is younger than ttl_hours, return it.
    """
    ensure_dirs()
    key = cache_key(url, json.dumps(kwargs, sort_keys=True))
    cache_file = CACHE_DIR / f"http_{key}.json"

    # Check cache
    if cache_file.exists():
        cached = read_json(cache_file)
        cached_time = datetime.fromisoformat(cached.get("fetched_at", "2000-01-01"))
        if (datetime.now() - cached_time).total_seconds() < ttl_hours * 3600:
            logger.info(f"Cache hit for {url[:80]}")
            return cached.get("body")

    # Fetch
    try:
        with httpx.Client(timeout=30, follow_redirects=True) as client:
            resp = client.get(url, **kwargs)
            resp.raise_for_status()
            body = resp.text
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {url[:80]}: {e}")
        # Return stale cache if available
        if cache_file.exists():
            cached = read_json(cache_file)
            logger.info("Returning stale cache")
            return cached.get("body")
        return None

    # Write cache
    write_json(cache_file, {
        "url": url,
        "fetched_at": datetime.now().isoformat(),
        "body": body,
    })
    return body


def call_llm(prompt: str, system_prompt: str = "", model: str = None) -> str:
    """
    Call an OpenAI-compatible LLM API.
    Config via env vars:
      - LLM_API_URL: API endpoint (default: https://api.openai.com/v1/chat/completions)
      - LLM_API_KEY: API key
      - LLM_MODEL: Model name (default: gpt-4o-mini)
    """
    api_url = os.environ.get("LLM_API_URL", "https://api.openai.com/v1/chat/completions")
    api_key = os.environ.get("LLM_API_KEY", "")
    model = model or os.environ.get("LLM_MODEL", "gpt-4o-mini")

    if not api_key:
        logger.warning("LLM_API_KEY not set. Returning placeholder.")
        return _generate_placeholder_report(prompt)

    try:
        with httpx.Client(timeout=60) as client:
            resp = client.post(
                api_url,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.5,
                    "max_tokens": 2000,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
    except httpx.HTTPError as e:
        logger.error(f"LLM API call failed: {e}")
        return _generate_placeholder_report(prompt)


def _generate_placeholder_report(prompt: str) -> str:
    """Generate a placeholder when LLM is unavailable."""
    today = today_str()
    return f"""## 技术突破摘要

今日暂无重大技术突破报告。自动化系统将在配置 LLM API 后自动生成结构化日报。

## 工程招标动态

数据抓取模块已部署，等待 API 密钥配置。请设置 `LLM_API_KEY` 环境变量启用自动生成。

## 政策变动提醒

政策追踪模块就绪。配置完成后，系统将每日自动扫描国家能源局、各省能源主管部门的最新政策文件。

---
*本日报由自动化系统于 {today} 生成 · 状态：LLM 未配置（占位报告）*
"""


# ---- Runners ----
def run_script(name: str) -> bool:
    """Run a sibling script and return success/failure."""
    script_path = SCRIPTS_DIR / name
    if not script_path.exists():
        logger.error(f"Script not found: {script_path}")
        return False
    logger.info(f"Running {name}...")
    # Import and run if it's a module; otherwise subprocess
    # For simplicity in this project, we'll use exec
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()
        exec(compile(code, script_path, "exec"))
        return True
    except Exception as e:
        logger.error(f"Script {name} failed: {e}", exc_info=True)
        return False
