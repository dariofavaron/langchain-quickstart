import pandas as pd
import json

def create_task_table(st, area_json, project_json, task_json):
    """
    Create a task table based on area, project, and task JSON data.

    Args:
        area_json (dict): JSON data for areas.
        project_json (dict): JSON data for projects.
        task_json (dict): JSON data for tasks.

    Returns:
        pd.DataFrame: DataFrame containing the task table.
    """
    # Extracting information
    area_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"]
                    for item in area_json["results"]}
    project_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"]
                    for item in project_json["results"]}
    task_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"]
                    for item in task_json["results"]}

    # Create a list to hold our final data
    final_data = []

    # Matching task IDs with corresponding project and area IDs
    for task_id, task_name in task_info.items():
        # Find project related to the task
        project_id = next((relation["properties"]["Projects"]["relation"][0]["id"] for relation in task_json["results"]
                        if relation["id"] == task_id), None)
        project_name = project_info.get(project_id, "Unknown")

        # Find area related to the project
        area_id = next((relation["properties"]["Areas"]["relation"][0]["id"] for relation in project_json["results"]
                        if relation["id"] == project_id), None)
        area_name = area_info.get(area_id, "Unknown")

        area_type = next((relation["properties"]["Type"]["select"]["name"] for relation in area_json["results"]
                        if relation["id"] == area_id), None)

        # Append to the final data
        final_data.append([task_name, project_name, area_name, area_type])

    # Create DataFrame
    df = pd.DataFrame(final_data, columns=["Task Name", "Project Related", "Area Related", "Area Type"])
    return df


def create_task_row_properties(task_name, project_id, description, status):
    """
    Create properties for a new task row.

    Args:
        task_name (str): Name of the task.
        project_id (str): ID of the project related to the task.
        description (str): Description of the task.
        status (str): Status of the task.

    Returns:
        dict: Properties for the new task row.
    """
    return {
        "Name": {
            "title": [
                {
                    "text": {
                        "content": task_name
                    }
                }
            ]
        },
        "Projects": {
            "relation": [
                {
                    "id": project_id
                }
            ]
        },
        "Description": {
            "rich_text": [
                {
                    "text": {
                        "content": description
                    }
                }
            ]
        },
        "Status": {
            "status": {
                "name": status
            }
        }
    }
