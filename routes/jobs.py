from fastapi import APIRouter, Query
from config.database import job_collection
from schema.job import list_serial
import pandas as pd

router = APIRouter()


@router.get("/jobs")
async def get_jobs():
    jobs_list = await job_collection.find().to_list(length=None)  # Fetch all documents
    jobs = list_serial(jobs_list)  # Serialize the list
    return jobs


# Helper function to get data as pandas DataFrame
async def get_jobs_df():
    """
    Converts MongoDB collection data to pandas DataFrame
    DataFrame: A 2-dimensional labeled data structure with columns of potentially different types.
    Similar to a spreadsheet or SQL table - the primary pandas data structure.
    """
    jobs_list = await job_collection.find().to_list(length=None)
    return pd.DataFrame(list_serial(jobs_list))


@router.get("/jobs/analysis")
async def basic_analysis():
    df = await get_jobs_df()
    # Basic DataFrame info
    analysis = {
        # Total number of rows (jobs)
        "total_jobs": len(df),
        # Column names (df.columns is an Index object)
        "columns": df.columns.tolist(),
        # Data types of each column
        "data_types": df.dtypes.astype(str).to_dict(),
        # First 5 records (df.head() returns first N rows)
        "sample_data": df.head().to_dict(orient='records')
    }
    return analysis


@router.get("/jobs/filter")
async def filter_jobs(
    company: str = Query(None),
    min_experience: int = Query(None),
    skill: str = Query(None)
):
    """
    DataFrame filtering endpoint
    Shows pandas querying capabilities with string operations
    """
    df = await get_jobs_df()
    # Copy original DataFrame for filtering
    filtered_df = df.copy()
    # Company filter using string contains (case-insensitive)
    if company:
        # pandas string operations via .str accessor
        filtered_df = filtered_df[filtered_df['company'].str.contains(
            company, case=False)]

    # Experience filter using regex extraction
    if min_experience:
        # Extract minimum experience from string using regular expression
        # str.extract() returns a DataFrame with capture groups
        filtered_df['min_exp'] = filtered_df['experience'].str.extract(
            r'(\d+)').astype(float)
        # Boolean indexing to filter rows
        filtered_df = filtered_df[filtered_df['min_exp'] >= min_experience]

    # Skill filter using list membership check
    if skill:
        # Apply lambda function to check skill presence in list
        # Lowercase both for case-insensitive search
        filtered_df = filtered_df[
            filtered_df['skills'].apply(
                lambda skills: skill.lower() in [s.lower() for s in skills]
            )
        ]

    # Convert filtered results to JSON-serializable format
    return filtered_df.to_dict(orient='records')


@router.get("/jobs/skills")
async def skills_analysis():
    """
    Skills analysis using DataFrame operations
    Demonstrates explode() and value_counts()
    """
    df = await get_jobs_df()
    # Explode the skills array into multiple rows
    # Before explode: 1 row per job with list of skills
    # After explode: 1 row per skill per job
    exploded_df = df.explode('skills')

    # Normalize skill names to lowercase
    exploded_df['skills'] = exploded_df['skills'].str.lower()

    # Count skill occurrences using value_counts()
    # value_counts() returns Series with unique values as index and counts as values
    skill_counts = exploded_df['skills'].value_counts()

    return {
        "most_common_skills": skill_counts.to_dict(),
        "total_unique_skills": skill_counts.nunique()  # Count unique skills
    }


@router.get("/jobs/experience-analysis")
async def experience_analysis():
    """
    Experience analysis using regex and numerical operations
    Shows pandas string extraction and aggregation
    """
    df = await get_jobs_df()

    # Extract experience ranges using regular expression
    # str.extract() with capture groups for min/max experience
    exp_ranges = df['experience'].str.extract(r'(\d+)\s*-\s*(\d+)')

    # Convert extracted strings to numerical values
    df['min_exp'] = exp_ranges[0].astype(float)
    df['max_exp'] = exp_ranges[1].astype(float)

    return {
        # Numerical aggregation methods
        "average_min_exp": df['min_exp'].mean(),
        "average_max_exp": df['max_exp'].mean(),

        # Count frequency of each experience range
        "experience_distribution": df['experience'].value_counts().to_dict()
    }


@router.get("/jobs/company-stats")
async def company_stats():
    """
    GroupBy and aggregation example
    Shows pandas' split-apply-combine pattern
    """
    df = await get_jobs_df()

    # Extract numerical experience first
    df['min_exp'] = df['experience'].str.extract(r'(\d+)').astype(float)

    # Normalize skills to lowercase
    df['skills'] = df['skills'].apply(lambda x: [s.lower() for s in x])

    # Group by company and aggregate statistics
    stats = df.groupby('company').agg(
        # Count unique job IDs per company
        total_jobs=('id', 'count'),
        # Average minimum experience
        average_min_exp=('min_exp', 'mean'),
        # Custom aggregation for top 3 skills
        common_skills=('skills', lambda x: x.explode(
        ).value_counts().head(3).to_dict())
    ).reset_index()  # Convert groupby object back to DataFrame

    return stats.to_dict(orient='records')


@router.get("/jobs/sorted")
async def sorted_jobs(
    sort_by: str = Query('position'),
    descending: bool = Query(False),
    limit: int = Query(10)
):
    """
    Sorting and pagination example
    Demonstrates DataFrame sorting and slicing
    """
    df = await get_jobs_df()

    # Sort values by specified column
    # sort_values returns new sorted DataFrame
    sorted_df = df.sort_values(
        sort_by,
        ascending=not descending  # Control sort direction
    )

    # Get top N results using head()
    paginated_df = sorted_df.head(limit)

    return paginated_df.to_dict(orient='records')
