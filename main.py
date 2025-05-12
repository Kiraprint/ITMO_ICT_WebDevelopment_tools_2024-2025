from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from sqlmodel import Session, select
from contextlib import asynccontextmanager

from models import Project, Skill, Team, TeamMemberLink, User, UserSkillLink, SkillLevel, Task, ProjectTeamLink
from connection import get_session, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize the database
    init_db()
    yield
    # Shutdown: cleanup operations can go here if needed

app = FastAPI(lifespan=lifespan)

@app.get("/")
def hello():
    return "Hello, World!"



# Users
@app.get("/users/", response_model=List[User])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Обновление пользователя
@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserBase, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# Skills
@app.get("/skills/", response_model=List[Skill])
def get_skills(session: Session = Depends(get_session)):
    skills = session.exec(select(Skill)).all()
    return skills

@app.get("/skills/{skill_id}", response_model=Skill)
def get_skill(skill_id: int, session: Session = Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@app.post("/skills/", response_model=Skill)
def create_skill(skill: Skill, session: Session = Depends(get_session)):
    session.add(skill)
    session.commit()
    session.refresh(skill)
    return skill

# Обновление навыка
@app.patch("/skills/{skill_id}", response_model=Skill)
def update_skill(skill_id: int, skill: SkillBase, session: Session = Depends(get_session)):
    db_skill = session.get(Skill, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    skill_data = skill.model_dump(exclude_unset=True)
    for key, value in skill_data.items():
        setattr(db_skill, key, value)
    
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill

# Projects
@app.get("/projects/", response_model=List[Project])
def get_projects(session: Session = Depends(get_session)):
    projects = session.exec(select(Project)).all()
    return projects

@app.post("/projects/", response_model=Project)
def create_project(project: Project, session: Session = Depends(get_session)):
    session.add(project)
    session.commit()
    session.refresh(project)
    return project

# Обновление проекта
@app.patch("/projects/{project_id}", response_model=Project)
def update_project(project_id: int, project: ProjectBase, session: Session = Depends(get_session)):
    db_project = session.get(Project, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = project.model_dump(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    
    session.add(db_project)
    session.commit()
    session.refresh(db_project)
    return db_project

# Teams
@app.get("/teams/", response_model=List[Team])
def get_teams(session: Session = Depends(get_session)):
    teams = session.exec(select(Team)).all()
    return teams

@app.get("/teams/{team_id}/members", response_model=List[TeamMemberLink])
def get_team_members(team_id: int, session: Session = Depends(get_session)):
    members = session.exec(select(TeamMemberLink).where(TeamMemberLink.team_id == team_id)).all()
    return members

# Обновление команды
@app.patch("/teams/{team_id}", response_model=Team)
def update_team(team_id: int, team: TeamBase, session: Session = Depends(get_session)):
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

# Поиск пользователей по навыкам
@app.get("/users/search/", response_model=List[User])
def search_users_by_skills(
    skill_ids: List[int] = Query(None), 
    min_level: Optional[SkillLevel] = None,
    session: Session = Depends(get_session)
):
    if not skill_ids:
        return session.exec(select(User)).all()
    
    query = select(User).join(UserSkillLink)
    
    if min_level:
        query = query.where(
            UserSkillLink.skill_id.in_(skill_ids),
            UserSkillLink.level >= min_level
        )
    else:
        query = query.where(UserSkillLink.skill_id.in_(skill_ids))
    
    return session.exec(query).all()

# Получение навыков пользователя
@app.get("/users/{user_id}/skills", response_model=List[UserSkillLink])
def get_user_skills(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_skills = session.exec(
        select(UserSkillLink).where(UserSkillLink.user_id == user_id)
    ).all()
    return user_skills

# Добавление навыка пользователю
@app.post("/users/{user_id}/skills", response_model=UserSkillLink)
def add_user_skill(user_id: int, user_skill: UserSkillLink, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    skill = session.get(Skill, user_skill.skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    # Проверяем, есть ли уже такой навык у пользователя
    existing_skill = session.exec(
        select(UserSkillLink).where(
            UserSkillLink.user_id == user_id,
            UserSkillLink.skill_id == user_skill.skill_id
        )
    ).first()
    
    if existing_skill:
        raise HTTPException(status_code=400, detail="User already has this skill")
    
    user_skill.user_id = user_id
    session.add(user_skill)
    session.commit()
    session.refresh(user_skill)
    return user_skill

# Обновление связи пользователя и навыка
@app.patch("/users/{user_id}/skills/{skill_id}", response_model=UserSkillLink)
def update_user_skill(
    user_id: int, 
    skill_id: int, 
    user_skill: UserSkillLink, 
    session: Session = Depends(get_session)
):
    db_user_skill = session.exec(
        select(UserSkillLink).where(
            UserSkillLink.user_id == user_id,
            UserSkillLink.skill_id == skill_id
        )
    ).first()
    
    if not db_user_skill:
        raise HTTPException(status_code=404, detail="User skill link not found")
    
    user_skill_data = user_skill.model_dump(exclude_unset=True)
    for key, value in user_skill_data.items():
        if key not in ["user_id", "skill_id"]:  # Не обновляем первичные ключи
            setattr(db_user_skill, key, value)
    
    session.add(db_user_skill)
    session.commit()
    session.refresh(db_user_skill)
    return db_user_skill

@app.get("/teams/matching/{user_id}", response_model=List[Team])
def find_matching_teams(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Получаем навыки пользователя
    user_skills = session.exec(
        select(UserSkillLink).where(UserSkillLink.user_id == user_id)
    ).all()
    user_skill_ids = [us.skill_id for us in user_skills]
    
    # Находим команды, в которых пользователь еще не состоит
    user_teams = session.exec(
        select(TeamMemberLink.team_id).where(TeamMemberLink.user_id == user_id)
    ).all()
    
    # Получаем все команды
    teams = session.exec(select(Team)).all()
    matching_teams = []
    
    for team in teams:
        # Пропускаем команды, в которых пользователь уже состоит
        if team.id in user_teams:
            continue
        
        # Получаем навыки всех участников команды
        team_members = session.exec(
            select(TeamMemberLink.user_id).where(TeamMemberLink.team_id == team.id)
        ).all()
        
        team_skill_ids = []
        for member_id in team_members:
            member_skills = session.exec(
                select(UserSkillLink.skill_id).where(UserSkillLink.user_id == member_id)
            ).all()
            team_skill_ids.extend(member_skills)
        
        # Проверяем, есть ли у пользователя уникальные навыки для команды
        has_unique_skills = any(skill_id not in team_skill_ids for skill_id in user_skill_ids)
        
        # Проверяем, есть ли у пользователя навыки высокого уровня
        has_high_level_skills = session.exec(
            select(UserSkillLink).where(
                UserSkillLink.user_id == user_id,
                UserSkillLink.level.in_([SkillLevel.ADVANCED, SkillLevel.EXPERT])
            )
        ).first() is not None
        
        if has_unique_skills or has_high_level_skills:
            matching_teams.append(team)
    
    return matching_teams

@app.get("/projects/matching/{user_id}", response_model=List[Project])
def find_matching_projects(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Получаем навыки пользователя
    user_skills = session.exec(
        select(UserSkillLink.skill_id).where(UserSkillLink.user_id == user_id)
    ).all()
    
    # Получаем все проекты
    projects = session.exec(select(Project)).all()
    matching_projects = []
    
    for project in projects:
        # Находим команды, работающие над проектом
        project_teams = session.exec(
            select(ProjectTeamLink.team_id).where(ProjectTeamLink.project_id == project.id)
        ).all()
        
        for team_id in project_teams:
            # Получаем навыки всех участников команды
            team_members = session.exec(
                select(TeamMemberLink.user_id).where(TeamMemberLink.team_id == team_id)
            ).all()
            
            team_skills = []
            for member_id in team_members:
                member_skills = session.exec(
                    select(UserSkillLink.skill_id).where(UserSkillLink.user_id == member_id)
                ).all()
                team_skills.extend(member_skills)
            
            # Проверяем, есть ли у пользователя навыки, которые дополняют команду
            for skill_id in user_skills:
                if skill_id not in team_skills:
                    matching_projects.append(project)
                    break
    
    return matching_projects

# Обновление связи команды и участника
@app.patch("/teams/{team_id}/members/{user_id}", response_model=TeamMemberLink)
def update_team_member(
    team_id: int, 
    user_id: int, 
    team_member: TeamMemberLink, 
    session: Session = Depends(get_session)
):
    db_team_member = session.exec(
        select(TeamMemberLink).where(
            TeamMemberLink.team_id == team_id,
            TeamMemberLink.user_id == user_id
        )
    ).first()
    
    if not db_team_member:
        raise HTTPException(status_code=404, detail="Team member link not found")
    
    team_member_data = team_member.model_dump(exclude_unset=True)
    for key, value in team_member_data.items():
        if key not in ["team_id", "user_id"]:  # Не обновляем первичные ключи
            setattr(db_team_member, key, value)
    
    session.add(db_team_member)
    session.commit()
    session.refresh(db_team_member)
    return db_team_member
