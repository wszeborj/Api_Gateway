from pydantic import BaseModel, Field


class UpdateProgressInput(BaseModel):

    course_id: int = Field(..., alias="courseId")
    status: str = "IN_PROGRESS"  # IN_PROGRESS, COMPLETED, PAUSED
    completion_percentage: float | None = Field(None, alias="completionPercentage")
    time_spent_seconds: int | None = Field(None, alias="timeSpentSeconds")
    notes: str | None = None

    class Config:
        populate_by_name = True


class CreateAchievementInput(BaseModel):

    achievement_type: str = Field(..., alias="achievementType")
    achievement_name: str = Field(..., alias="achievementName")
    description: str | None = None

    class Config:
        populate_by_name = True


class CreateCertificateInput(BaseModel):

    course_id: int = Field(..., alias="courseId")
    final_score: float = Field(..., alias="finalScore")
    grade: str
    pdf_url: str | None = Field(None, alias="pdfUrl")
    notes: str | None = None

    class Config:
        populate_by_name = True
