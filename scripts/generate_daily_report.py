"""
Generate the daily Energy Storage Science report.
Aggregates data from all fetch scripts, calls LLM for structured summary,
and writes the daily report Markdown file.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import (
    ensure_dirs, today_str, today_date, read_json, write_markdown,
    call_llm, logger, SRC_DATA_DIR, REPORTS_DIR,
)


REPORT_PROMPT_TEMPLATE = """你是一位储能行业资深分析师。基于以下今日采集的数据，撰写一份简洁的储能科学日报（中文，约500字），包含三个板块：

## 1. 技术突破摘要
- 总结今天值得关注的技术论文和产业新闻

## 2. 工程招标动态
- 汇总新项目招标和中标情况

## 3. 政策变动提醒
- 梳理最新政策法规变化

今日采集数据：

**论文追踪**：
{papers}

**行业新闻与招标**：
{news}

**装机数据**：
{install_data}

**现货市场价格**：
{price_data}

要求：
- 每个板块2-3个要点，用事实和数据说话
- 语言专业但可读，必要术语附带简短说明
- 避免冗余，突出对储能行业从业者有决策参考价值的信息
- 最后附一段50字以内的"今日一句话"总结
"""


def build_report_content(llm_output: str) -> str:
    """Build the final Markdown content for the daily report."""
    today = today_str()
    date_obj = today_date()

    topics = []
    if "技术突破" in llm_output or "电池" in llm_output or "论文" in llm_output:
        topics.append("tech-breakthrough")
    if "招标" in llm_output or "项目" in llm_output or "中标" in llm_output:
        topics.append("bidding")
    if "政策" in llm_output or "法规" in llm_output or "标准" in llm_output:
        topics.append("policy")

    # Generate a brief AI summary (first 2 sentences)
    sentences = llm_output.replace("\n", " ").split("。")
    summary = "。".join(sentences[:2]) + "。"

    md = f"""---
date: {today}
generatedBy: automation
topics:
  - {'\n  - '.join(topics) if topics else 'industry'}
aiSummary: "{summary}"
dataSources:
  - arXiv API
  - 中国储能网
  - 国家能源局
  - 山东电力交易中心
---

# 储能科学日报

**{date_obj.strftime('%Y年%m月%d日')}** · 自动生成

{llm_output}

---
*本日报由自动化系统生成 · 数据来源：公开信息平台 · 仅供参考*
"""
    return md


def main():
    ensure_dirs()

    # Load data from fetch scripts
    papers_feed = read_json(SRC_DATA_DIR / "papers-feed.json")
    bidding_news = read_json(SRC_DATA_DIR / "bidding-news.json")
    install_data = read_json(SRC_DATA_DIR / "install-growth.json")
    price_data = read_json(SRC_DATA_DIR / "price-spread.json")

    # Format data for prompt
    papers_str = str(papers_feed.get("papers", [])[:3])
    news_str = str(bidding_news.get("items", [])[:5])
    install_str = f"最新装机总量: {install_data.get('totalInstalled', {}).get('china', 'N/A')} GWh (中国)"
    price_str = f"峰谷价差: {price_data.get('summary', {}).get('avgSpread', 'N/A')} 元/kWh"

    # Build prompt and call LLM
    prompt = REPORT_PROMPT_TEMPLATE.format(
        papers=papers_str,
        news=news_str,
        install_data=install_str,
        price_data=price_str,
    )

    system_prompt = "你是一位储能行业资深分析师，擅长从海量信息中提取关键决策信息。请用中文回复。"

    logger.info("Calling LLM to generate daily report...")
    llm_output = call_llm(prompt, system_prompt)

    # Build and write report
    md_content = build_report_content(llm_output)
    today = today_str()
    report_path = REPORTS_DIR / f"{today}.md"
    write_markdown(report_path, md_content)

    # Also update chart data
    logger.info("Updating chart data...")
    try:
        from update_chart_data import main as update_charts
        update_charts()
    except Exception as e:
        logger.warning(f"Chart update skipped: {e}")

    logger.info(f"Daily report generated: {report_path}")
    print(f"SUCCESS: Report written to {report_path}")


if __name__ == "__main__":
    main()
