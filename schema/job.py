def individual_job(job) -> dict:
    return {
        "id": str(job["_id"]),
        "position": job["position"],
        "company": job["company"],
        "skills": job["skills"],
        "experience": job["experience"],
        "more_details": job["more_details"]
    }


def list_serial(jobs) -> list:
    return [individual_job(job) for job in jobs]
