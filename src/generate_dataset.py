from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

random.seed(42)

NUM_CANDIDATES = 500

SOURCES = [
    "LinkedIn",
    "Referral",
    "Campus",
    "Job Portal",
    "Hackathon",
]

ROLES = [
    "Backend Engineer",
    "ML Engineer",
    "Data Analyst",
    "Frontend Engineer",
]

STAGES = [
    "Applied",
    "Assessment Cleared",
    "Technical Interview",
    "HR Interview",
    "Hired",
]

DROPOUT_REASONS = [
    "Low Assessment Score",
    "Poor Communication",
    "Salary Mismatch",
    "Offer Declined",
    "Technical Rejection",
    "No Dropout",
]


def weighted_source_bonus(source: str) -> int:
    """
    Stronger candidate sources receive small score boosts.
    """

    bonuses = {
        "Referral": 12,
        "Hackathon": 8,
        "LinkedIn": 5,
        "Campus": 3,
        "Job Portal": 0,
    }

    return bonuses[source]


def determine_stage(final_score: float) -> str:
    """
    Simulate candidate funnel progression.
    """

    if final_score >= 85:
        return "Hired"

    if final_score >= 72:
        return "HR Interview"

    if final_score >= 58:
        return "Technical Interview"

    if final_score >= 45:
        return "Assessment Cleared"

    return "Applied"


def generate_candidate(candidate_id: int) -> dict:
    """
    Generate one synthetic candidate row.
    """

    source = random.choice(SOURCES)
    role = random.choice(ROLES)

    assessment_score = min(
        100,
        max(
            35,
            int(random.gauss(65 + weighted_source_bonus(source), 12)),
        ),
    )

    communication_score = min(
        100,
        max(
            30,
            int(random.gauss(68, 10)),
        ),
    )

    resume_score = min(
        100,
        max(
            40,
            int(random.gauss(70, 9)),
        ),
    )

    experience_years = round(
        max(0, random.gauss(1.5, 1.2)),
        1,
    )

    interview_score = int(
        (assessment_score * 0.5 + communication_score * 0.3 + resume_score * 0.2)
    )

    final_score = (
        assessment_score * 0.5 + interview_score * 0.3 + communication_score * 0.2
    )

    application_stage = determine_stage(final_score)

    selected = application_stage == "Hired"

    days_in_pipeline = {
        "Applied": random.randint(1, 5),
        "Assessment Cleared": random.randint(5, 10),
        "Technical Interview": random.randint(10, 18),
        "HR Interview": random.randint(18, 25),
        "Hired": random.randint(25, 40),
    }[application_stage]

    if selected:
        dropout_reason = "No Dropout"
    else:
        dropout_reason = random.choice(DROPOUT_REASONS[:-1])

    return {
        "candidate_id": candidate_id,
        "source": source,
        "role": role,
        "assessment_score": assessment_score,
        "communication_score": communication_score,
        "resume_score": resume_score,
        "interview_score": interview_score,
        "experience_years": experience_years,
        "final_score": round(final_score, 2),
        "application_stage": application_stage,
        "selected": selected,
        "days_in_pipeline": days_in_pipeline,
        "dropout_reason": dropout_reason,
    }


def main() -> None:
    """
    Generate full recruitment dataset.
    """

    rows = [
        generate_candidate(candidate_id)
        for candidate_id in range(1, NUM_CANDIDATES + 1)
    ]

    dataframe = pd.DataFrame(rows)

    output_path = Path("data/raw/candidates.csv")

    dataframe.to_csv(output_path, index=False)

    print(f"Dataset generated successfully at: {output_path}")
    print(f"Total candidates: {len(dataframe)}")


if __name__ == "__main__":
    main()
