from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup
import requests
from models.job import Job
from config.database import job_collection
from typing import Optional
from itertools import cycle


router = APIRouter()

# Load proxies from file and create a cycle
with open("working_proxies.txt", "r") as f:
    proxy_pool = cycle([line.strip() for line in f])


@router.get("/scrape")
async def scrape_website(url: str = "https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35&clusterName=CLUSTER_FA&hc=CLUSTER_FA", proxy: Optional[str] = None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/",
    }

    max_retries = 5  # Retry with up to 5 proxies on failure
    retry_count = 0
    last_exception = None

    # Configure proxies
    while retry_count < max_retries:
        # Use provided proxy or get the next one from the pool
        current_proxy = proxy if proxy else next(proxy_pool)
        proxies = {"http": current_proxy, "https": current_proxy}

        try:
            response = requests.get(
                url,
                headers=headers,
                proxies=proxies,
                timeout=20
            )
            response.raise_for_status()
            break  # Exit loop on success
        except Exception as e:
            last_exception = e
            retry_count += 1
            if proxy:
                break  # Don't retry if user provided a specific proxy
            print(f"⚠️ Proxy {current_proxy} failed. Retrying...")

    else:
        # All retries failed
        raise HTTPException(
            status_code=400,
            detail=f"Request failed after {max_retries} retries: {str(last_exception)}"
        )

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    inserted_ids = []
    for job in jobs:
        # Extract job details
        position = job.find('h2', class_="heading-trun")
        position_text = position.a.text.strip() if position else "N/A"
        company = job.find('h3', class_='joblist-comp-name')
        company_text = company.text.strip() if company else "N/A"
        experience_icon = job.find('i', class_='srp-icons experience')
        experience = experience_icon.parent.get_text(
            strip=True) if experience_icon else "N/A"
        detail_link = job.find('a', class_='posoverlay_srp')
        # Skip if no detail link
        if not detail_link or 'href' not in detail_link.attrs:
            continue
        job_url = detail_link['href']
        # Check if job already exists in MongoDB
        existing_job = await job_collection.find_one({"more_details": job_url})
        if existing_job:
            print(f"⏩ Skipping duplicate job: {job_url}")
            continue
        # Extract skills
        skills_div = job.find('div', class_='srp-skills')
        job_skills = []
        if skills_div:
            skills_span = skills_div.find_all('span')
            job_skills = [span.get_text(
                strip=True) for span in skills_span if 'srp-tag' not in span.get('class', [])]

        # Create Job instance
        job_data = Job(
            position=position_text,
            company=company_text,
            skills=job_skills,
            experience=experience,
            more_details=job_url)

        # Insert into MongoDB
        result = await job_collection.insert_one(dict(job_data))
        inserted_ids.append(str(result.inserted_id))

    return {"message": f"Successfully inserted {len(inserted_ids)} jobs", "inserted_ids": inserted_ids}
