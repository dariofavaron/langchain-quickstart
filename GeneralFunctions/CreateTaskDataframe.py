import pandas as pd
import json

def create_task_table(area_json, project_json, task_json):

    # Extracting information
    area_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"] for item in area_json["results"]}
    project_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"] for item in project_json["results"]}
    task_info = [(item["id"], item["properties"]["Name"]["title"][0]["plain_text"]) for item in task_json["results"]]

    # Create a list to hold our final data
    final_data = []

    # Matching task IDs with corresponding project and area IDs
    for task_id, task_name in task_info:
        # Find project related to the task
        project_id = next((relation["id"] for relation in tasks_data["results"] if relation["id"] == task_id), None)
        project_name = project_info.get(project_id, "Unknown")

        # Find area related to the project
        area_id = next((relation["id"] for relation in projects_data["results"] if relation["id"] == project_id), None)
        area_name = area_info.get(area_id, "Unknown")

        # Append to the final data
        final_data.append([task_name, project_name, area_name])

    # Create DataFrame
    df = pd.DataFrame(final_data, columns=["Task Name", "Project Related", "Area Related"])
    return df