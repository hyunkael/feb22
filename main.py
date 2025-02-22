from fastapi import FastAPI
from pydantic import BaseModel
import csv
import os

app = FastAPI()

@app.get("/data")
def all_data():
    data = read_from_csv("user_data.csv")
    return {"data": data}
    
# Define the data model for creating users
class UserCreate(BaseModel):
    user_id: int
    username: str

# Initialize an empty list to store user data
user_data_list = []

# CSV file path
csv_file = "user_data.csv"

# Function to export data to CSV without pandas
def export_to_csv(data_list):
    file_exists = os.path.isfile(csv_file)
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["user_id", "username"])
        
        # Write header only if the file does not exist
        if not file_exists:
            writer.writeheader()

        # Write data
        writer.writerows(data_list)

@app.post("/create_user/")
async def create_user(user_data: UserCreate):
    user_id = user_data.user_id
    username = user_data.username

    # Append new user data to the list
    user_data_list.append({"user_id": user_id, "username": username})

    # Export the updated data list to CSV using the helper function
    export_to_csv(user_data_list)

    return {
        "message": "We got data successfully",
        "user_id": user_id,
        "username": username,
    }

@app.get("/")
async def root():
    return {"message": "Hello World. I was here!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

#