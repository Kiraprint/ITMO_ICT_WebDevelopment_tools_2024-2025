from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, SQLModel, Relationship

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class TeamRole(str, Enum):
    LEADER = "leader"
    MEMBER = "member"
    MENTOR = "mentor"

# Базовые модели для обновления (без связей)
class UserBase(SQLModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    years_of_experience: Optional[float] = None

class SkillBase(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class TeamBase(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectBase(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None

class TaskBase(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[int] = None
    status: Optional[str] = None
    deadline: Optional[datetime] = None

# Существующие модели связей
class UserSkillLink(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)
    level: SkillLevel
    years_of_experience: float

class TeamMemberLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    role: TeamRole
    joined_at: datetime

class ProjectTeamLink(SQLModel, table=True):
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    start_date: datetime
    end_date: Optional[datetime] = None

# Основные модели
class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    users: List["User"] = Relationship(back_populates="skills", link_model=UserSkillLink)

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    full_name: str
    email: str
    bio: Optional[str] = None
    years_of_experience: float
    skills: List[Skill] = Relationship(back_populates="users", link_model=UserSkillLink)
    teams: List["Team"] = Relationship(back_populates="members", link_model=TeamMemberLink)
    tasks: List["Task"] = Relationship(back_populates="assigned_user")

class Team(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    created_at: datetime
    members: List[User] = Relationship(back_populates="teams", link_model=TeamMemberLink)
    projects: List["Project"] = Relationship(back_populates="projects", link_model=ProjectTeamLink)

class Project(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str
    teams: List[Team] = Relationship(back_populates="projects", link_model=ProjectTeamLink)
    tasks: List["Task"] = Relationship(back_populates="project")

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    project_id: Optional[int] = Field(default=None, foreign_key="project.id", primary_key=True)
    project: Optional[Project] = Relationship(back_populates="tasks")
    title: str
    description: str
    assigned_to: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    assigned_user: Optional[User] = Relationship(back_populates="tasks")
    status: str
    deadline: datetime
    created_at: datetime
