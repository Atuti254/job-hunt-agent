# Production Automation Rules & Guardrails

## 1. Hard Filters (Auto-Reject if Violated)
- **Work Mode:** STRICTLY 100% Remote (Global, EMEA, Africa, or Kenya Remote). Reject any Hybrid or On-Site role immediately.
- **Target Roles:** Data Analyst, Business Intelligence (BI) Analyst, Product Analyst, Analytics Engineer, SQL Data Analyst, Junior/Mid Data Scientist.
- **Seniority Positioning:** Target Entry-Level through Mid-Level (0–4 years required). Reject Staff, Principal, Lead, or Director roles. Never frame Isaac as an inexperienced student—highlight his 3 years of hands-on SQL, Python, and Power BI production projects.
- **Compensation Floor:** Minimum KES 40,000/month (~$310 USD/month or ~$3,720 USD/year). Auto-reject any listing explicitly below this floor.

## 2. Deliverable Requirements (Every Application)
- Generate BOTH a tailored **Resume PDF** (`output/<job_uid>_resume.pdf`) AND a tailored **Cover Letter PDF** (`output/<job_uid>_cover_letter.pdf`) for every qualifying job.
- Select the top 3–4 projects from `data/profile.md` that best match the job description's tech stack.

## 3. Grounding & Creative Answer Policy
- **Zero Fabrication of Hard Facts:** Never invent tools, certifications, employers, or numeric metrics not present in `data/profile.md`.
- **Creative Synthesis for Unfamiliar Questions:** For open-ended questions not in `data/answers.json` (e.g., *"Tell us about a messy dataset you fixed"* or *"Why this company?"*), synthesize a compelling, mid-level-caliber response by connecting the company's domain directly to Isaac's verified work (`haraka-rides-sql-project`, `wakala-plus-stats-toolkit`, `Car-Sales-end-to-end-analytics`, or retail Power BI automation).

## 4. Mode B Autonomous Execution & Stop Conditions
- **Auto-Submit Threshold:** Automatically submit applications scoring >= 8.0/10 against `data/profile.md` and these rules.
- **Throttle:** Maximum 10 submissions per day with 20–45 second randomized delays between actions.
- **Pause Only On:** CAPTCHA challenges, MFA/email verification prompts, or broken upload widgets—log status as `PAUSED_CAPTCHA` in `data/jobs.db` and move to the next job.
