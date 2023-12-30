import pandas as pd
import json

def create_task_table(area_json, project_json, task_json):
    # Parse JSON data
    areas_data = json.loads(area_json)
    projects_data = json.loads(project_json)
    tasks_data = json.loads(task_json)

    # Extracting information
    area_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"] for item in areas_data["results"]}
    project_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"] for item in projects_data["results"]}
    task_info = [(item["id"], item["properties"]["Name"]["title"][0]["plain_text"]) for item in tasks_data["results"]]

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