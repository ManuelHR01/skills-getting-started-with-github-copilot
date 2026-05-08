"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_dir = Path(__file__).parent
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(current_dir, "static")),
    name="static",
)

activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills through competitive debate",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"],
    },
    "Science Olympiad": {
        "description": "Compete in science and engineering challenges at regional and state competitions",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["james@mergington.edu", "isabella@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Basketball Team": {
        "description": "Join the school basketball team and compete in the regional league",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["marcus@mergington.edu", "lucas@mergington.edu"],
    },
    "Soccer Team": {
        "description": "Play competitive soccer and develop teamwork skills",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["carlos@mergington.edu"],
    },
    "Drama Club": {
        "description": "Perform in school plays and musicals, develop acting and stage skills",
        "schedule": "Wednesdays and Saturdays, 2:00 PM - 4:00 PM",
        "max_participants": 20,
        "participants": ["sarah@mergington.edu", "rachel@mergington.edu"],
    },
    "Art Studio": {
        "description": "Explore painting, drawing, sculpture, and other visual arts",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["maya@mergington.edu"],
    },
    "Music Ensemble": {
        "description": "Play instruments and perform in concerts and school events",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["david@mergington.edu", "grace@mergington.edu"],
    },
}


class UnregisterRequest(BaseModel):
    email: str


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email in activity["participants"]:
        raise HTTPException(
            status_code=400,
            detail="El estudiante ya está inscrito en esta actividad",
        )

    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.post("/activities/{activity_name}/unregister")
def unregister_participant(activity_name: str, req: UnregisterRequest):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if req.email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found")

    activity["participants"].remove(req.email)
    return {"message": f"Removed {req.email} from {activity_name}"}
