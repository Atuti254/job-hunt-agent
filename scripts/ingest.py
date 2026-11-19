import hashlib
import re
import sqlite3
import xml.etree.ElementTree as ET
from pathlib import Path
import requests

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "jobs.db"

GREENHOUSE_BOARDS = [
    "gitlab", "canonical", "automattic", "grafanalabs", "dbt-labs",
    "posthog", "zapier", "wikimedia", "mozilla", "remotecom", "deel"
]

TARGET_KEYWORDS = [
    "data analyst", "business intelligence", "bi analyst",
    "product analyst", "analytics engineer", "sql analyst"
]

EXCLUDE_TITLE_KEYWORDS = [
    "staff ", "principal ", "director", "vp ", "head of", "manager", "lead "
]

EXCLUDE_GEO_KEYWORDS = [
    "us only", "u.s. only", "united states only", "usa only",
    "north america only", "canada only", "uk only", "eu only", "on-site", "onsite", "hybrid"
]

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) JobHuntAgent/1.0"}


def make_dedup_key(company: str, title: str) -> str:
    norm = re.sub(r"[^a-z0-9]", "", f"{company.lower()}_{title.lower()}")
    return hashlib.sha256(norm.encode()).hexdigest()[:24]


def is_valid_role(title: str, location: str, description: str) -> bool:
    t_low = title.lower()
    if not any(kw in t_low for kw in TARGET_KEYWORDS):
        return False
    if any(bad in t_low for bad in EXCLUDE_TITLE_KEYWORDS):
        return False
    combined_geo = f"{location} {description[:600]}".lower()
    if any(bad_geo in combined_geo for bad_geo in EXCLUDE_GEO_KEYWORDS):
        return False
    return True


def fetch_greenhouse():
    results = []
    for slug in GREENHOUSE_BOARDS:
        url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            r.raise_for_status()
            for j in r.json().get("jobs", []):
                results.append({
                    "company": slug,
                    "title": j.get("title", ""),
                    "location": j.get("location", {}).get("name", "Remote"),
                    "source": "greenhouse",
                    "url": j.get("absolute_url", ""),
                    "description": j.get("content", "")
                })
        except Exception as e:
            print(f"[WARN] Greenhouse ({slug}): {e}")
    return results


def fetch_remotive():
    results = []
    try:
        r = requests.get("https://remotive.com/api/remote-jobs?category=data", headers=HEADERS, timeout=15)
        r.raise_for_status()
        for j in r.json().get("jobs", []):
            results.append({
                "company": j.get("company_name", "Unknown"),
                "title": j.get("title", ""),
                "location": j.get("candidate_required_location", "Worldwide"),
                "source": "remotive",
                "url": j.get("url", ""),
                "description": j.get("description", "")
            })
    except Exception as e:
        print(f"[WARN] Remotive: {e}")
    return results


def fetch_jobicy():
    results = []
    try:
        r = requests.get("https://jobicy.com/api/v2/remote-jobs?count=50&tag=data", headers=HEADERS, timeout=15)
        r.raise_for_status()
        for j in r.json().get("jobs", []):
            results.append({
                "company": j.get("companyName", "Unknown"),
                "title": j.get("jobTitle", ""),
                "location": j.get("jobGeo", "Anywhere"),
                "source": "jobicy",
                "url": j.get("url", ""),
                "description": j.get("jobDescription", "")
            })
    except Exception as e:
        print(f"[WARN] Jobicy: {e}")
    return results


def fetch_himalayas():
    results = []
    try:
        r = requests.get("https://himalayas.app/jobs/api?limit=50", headers=HEADERS, timeout=15)
        r.raise_for_status()
        for j in r.json().get("jobs", []):
            locs = ", ".join(j.get("locationRestrictions", [])) or "Worldwide"
            results.append({
                "company": j.get("companyName", "Unknown"),
                "title": j.get("title", ""),
                "location": locs,
                "source": "himalayas",
                "url": j.get("applicationLink") or j.get("guid", ""),
                "description": j.get("description", "")
            })
    except Exception as e:
        print(f"[WARN] Himalayas: {e}")
    return results


def fetch_weworkremotely():
    results = []
    try:
        r = requests.get("https://weworkremotely.com/categories/remote-data-jobs.rss", headers=HEADERS, timeout=15)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        for item in root.findall(".//item"):
            raw_title = item.findtext("title", "")
            company, title = (raw_title.split(":", 1) + [""])[:2] if ":" in raw_title else ("Unknown", raw_title)
            results.append({
                "company": company.strip(),
                "title": title.strip(),
                "location": item.findtext("region", "Worldwide"),
                "source": "weworkremotely",
                "url": item.findtext("link", ""),
                "description": item.findtext("description", "")
            })
    except Exception as e:
        print(f"[WARN] WeWorkRemotely: {e}")
    return results


def ingest():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    all_jobs = fetch_greenhouse() + fetch_remotive() + fetch_jobicy() + fetch_himalayas() + fetch_weworkremotely()
    added = 0
    for job in all_jobs:
        if not job["url"] or not is_valid_role(job["title"], job["location"], job["description"]):
            continue
        job_uid = make_dedup_key(job["company"], job["title"])
        try:
            cursor.execute("""
                INSERT INTO jobs (job_uid, company, title, location, source, url, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (job_uid, job["company"], job["title"], job["location"], job["source"], job["url"], job["description"]))
            added += 1
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()
    print(f"Ingestion complete. Scanned {len(all_jobs)} listings, added {added} qualifying remote Data Analyst roles.")


if __name__ == "__main__":
    ingest()
