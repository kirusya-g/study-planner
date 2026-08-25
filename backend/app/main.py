from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def root():
    return {"message": "Study Planner API"}
@app.get("/calendars")
def get_calendars():
    calendars = [
        {
           "id": 1,
            "name": "University",
            "color": "#A8D8EA" 
        },
        {
            "id": 2,
            "name": "Personal",
            "color": "#CDB4DB"
        }
    ]
    return calendars