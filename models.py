from sqlmodel import SQLModel, create_engine, Field
from datetime import date


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


class Bug(SQLModel, table=False):
    id: int | None = Field(default= None, primary_key=True)
    name: str
    description: str

class Camera(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)
    serialId: str
    name: str
    member_id: int = Field(default=None, foreign_key="member.id")

class DetectedBugStats(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)
    bug_id: int = Field(default=None, foreign_key="bug.id")
    detectedBugStats: int
    calculatedDate: int = Field(default_factory=date.today().day, nullable=False)

class DetectionHistory (SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    imageUrl: str | None = Field(default=None)
    detectedAt: int =Field(default_factory=date.today().day, nullable=True)
    member_id: int = Field(default=None, foreign_key="member.id")
    camera_id: int = Field(default=None, foreign_key="camera.id")
    bug_id: int = Field(default=None, foreign_key="bug.id")
    visit_id: int = Field(default=None, foreign_key="visit.id")

class member(SQLModel, table=False):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    phoneNumber: str
    note: str
    recenVisit: int = Field(default_factory=date.today().day, nullable=True)
    registerAt: int = Field(default_factory=date.today().day, nullable=True)
    expiresAt: int = Field(default_factory=date.today().day, nullable=True)
    staff_id: int = Field(default=None, foreign_key="staff.id")

class Nottification(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    profileUrl: str
    title: str
    content: str
    staff_id: int = Field(default=None, foreign_key="staff.id")

class Staff(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    position: str
    profileUrl: str | None = Field(default=None)
    phoneNumber: str

class Visit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    visitedAt: int = Field(default_factory=date.today().day, nullable=True)
    visitPurpose: str
    visitComment: str
    staff_id: int = Field(default=None, foreign_key="staff.id")
    member_id: int = Field(default=None, foreign_key="member.id")