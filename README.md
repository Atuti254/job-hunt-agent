<div align="center">

# Autonomous Job-Hunt Agent

**A $0/month, local-first AI pipeline that scrapes remote Data Analyst jobs, scores them against strict guardrails, generates tailored PDF resumes & cover letters, and submits applications autonomously.**

![Cost](https://img.shields.io/badge/API_Cost-$0%2Fmonth-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Qwen_2.5_Coder_7B-000000?style=for-the-badge)
![Playwright](https://img.shields.io/badge/Playwright-MCP_Automation-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)

</div>

---

## How It Works

1. **Multi-Source Remote Scraping (`scripts/ingest.py`):** Pulls live listings from Greenhouse remote boards, Remotive, Jobicy, Himalayas, and WeWorkRemotely RSS feeds, filtering out hybrid/on-site or region-locked roles into SQLite (`data/jobs.db`).
2. **Zero-Hallucination Tailoring (`Codex CLI` + `Ollama`):** Scores each role (`0–10`) against `data/rules.md`. Matches $\ge 8.0$ are tailored via local `qwen2.5-coder:7b` into HTML templates (`templates/`) strictly from verified projects in `data/profile.md`.
3. **PDF Compilation (`scripts/compile_pdf.py`):** Renders custom A4 resume and cover letter PDFs via headless Chromium.
4. **Autonomous Submission (`agy` + `Playwright MCP`):** Fills ATS forms from `data/answers.json`, uploads both PDFs, answers open-ended questions, captures confirmation screenshots, and pauses on CAPTCHAs (`PAUSED_CAPTCHA`).

---

## Quickstart

```bash
git clone [https://github.com/Atuti254/job-hunt-agent.git](https://github.com/Atuti254/job-hunt-agent.git)
cd job-hunt-agent
pip install requests beautifulsoup4 playwright
python -m playwright install chromium
ollama pull qwen2.5-coder:7b

cp data/answers.example.json data/answers.json
python scripts/init_db.py
python scripts/ingest.py
agy
```

Inside `agy`, run:
> `Read AGENT_PROMPT.md and execute the Mode B pipeline for qualifying NEW jobs in data/jobs.db.`
