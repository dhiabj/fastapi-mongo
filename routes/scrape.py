from fastapi import APIRouter, HTTPException
from bs4 import BeautifulSoup
import requests
from models.job import Job
from config.database import job_collection


router = APIRouter()


def extract_job_skills(detail_url):
    try:
        response = requests.get(detail_url, timeout=10)
        response.raise_for_status()
        skills_soup = BeautifulSoup(response.content, 'html.parser')
        job_skills = skills_soup.find_all('span', class_='jd-skill-tag')
        return [skill.text.strip() for skill in job_skills]

    except Exception as e:
        return [f"Failed to retrieve skills: {str(e)}"]


@router.get("/scrape")
async def scrape_website(url: str = "https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35&clusterName=CLUSTER_FA&hc=CLUSTER_FA"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # Fetch webpage content
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Request failed: {str(e)}")

    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    inserted_ids = []
    for job in jobs:
        position = job.find('h2', class_="heading-trun")
        position_text = position.a.text.strip() if position else "N/A"
        company = job.find('h3', class_='joblist-comp-name')
        company_text = company.text.strip() if company else "N/A"
        experience_icon = job.find('i', class_='srp-icons experience')
        experience = experience_icon.parent.get_text(
            strip=True) if experience_icon else "N/A"
        detail_link = job.find('a', class_='posoverlay_srp')
        job_skills = extract_job_skills(
            detail_link['href']) if detail_link else []

        # Create Job instance
        job_data = Job(
            position=position_text,
            company=company_text,
            skills=job_skills,
            experience=experience
        )

        # Insert into MongoDB
        result = await job_collection.insert_one(dict(job_data))
        inserted_ids.append(str(result.inserted_id))

    return {"message": f"Successfully inserted {len(inserted_ids)} jobs", "inserted_ids": inserted_ids}
