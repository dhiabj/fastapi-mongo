from pydantic import BaseModel


class Job(BaseModel):
    position: str
    company: str
    skills: list[str]
    experience: str
    more_details: str
