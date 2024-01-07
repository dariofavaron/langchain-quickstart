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
        task_description = next((relation["properties"]["Description"]["rich_text"][0]["text"]["content"] for relation in task_json["results"]
                        if relation["id"] == task_id and relation["properties"]["Description"]["rich_text"]), None)
        project_name = project_info.get(project_id, "Unknown")

        # Find area related to the project
        area_id = next((relation["properties"]["Areas"]["relation"][0]["id"] for relation in project_json["results"]
                        if relation["id"] == project_id), None)
        area_name = area_info.get(area_id, "Unknown")

        area_type = next((relation["properties"]["Type"]["select"]["name"] for relation in area_json["results"]
                        if relation["id"] == area_id), None)

        # Append to the final data
        final_data.append([task_name, project_name, area_name, area_type, task_id, project_id, area_id, task_description])

    # Create DataFrame
    df = pd.DataFrame(final_data, columns=["Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"])
    #st.dataframe(df)
    return df


def create_project_table(st, area_json, project_json):
    """
    Create a project table based on area, and the project JSON data.

    Args:
        area_json (dict): JSON data for areas.
        project_json (dict): JSON data for projects.

    Returns:
        pd.DataFrame: DataFrame containing the project table.
    """
    # Extracting information
    area_info = {item["id"]: item["properties"]["Name"]["title"][0]["plain_text"]
                    for item in area_json["results"]}

    # Create a list to hold our final data
    final_data = []

    # Iterate over each project
    for project_item in project_json["results"]:
        project_id = project_item["id"]
        project_name = project_item["properties"]["Name"]["title"][0]["plain_text"]

        # Extract the area ID related to the project
        area_id = project_item["properties"]["Areas"]["relation"][0]["id"] if project_item["properties"]["Areas"]["relation"] else None
        area_name = area_info.get(area_id, "Unknown")

        # Extract the area type
        area_type = None
        if area_id:
            for area in area_json["results"]:
                if area["id"] == area_id and "Type" in area["properties"]:
                    area_type = area["properties"]["Type"]["select"]["name"]
                    break

        # Extract project description
        project_description = project_item["properties"]["Description"]["rich_text"][0]["plain_text"] if "Description" in project_item["properties"] and project_item["properties"]["Description"]["rich_text"] else "No Description"

        # Append to the final data
        final_data.append([project_name, area_name, area_type, project_id, area_id, project_description])

    # Create DataFrame
    df = pd.DataFrame(final_data, columns=["Project Name", "Area Related", "Area Type", "Project ID", "Area ID", "Project Description"])
    st.dataframe(df)
    return df

def create_note_table(st, notionClass, note_json, only_one_note):
    """
    Create a project table based on area, and the project JSON data.

    Args:
        area_json (dict): JSON data for areas.
        project_json (dict): JSON data for projects.

    Returns:
        pd.DataFrame: DataFrame containing the project table.
    """

    # Create a list to hold our final data
    final_data = []

    # Iterate over each project
    for note_item in note_json["results"]:
        note_id = note_item["id"]
        note_name = note_item["properties"]["Name"]["title"][0]["plain_text"]
        note_url = note_item["properties"]["URL"]["url"] if "URL" in note_item["properties"] else None

        # Extract note content
        note_content = notionClass.get_page_content(st, note_id)
        #note_content = note_item["properties"]["Content"]["rich_text"][0]["plain_text"] if "Content" in note_item["properties"] and note_item["properties"]["Content"]["rich_text"] else "No Content"
        
        # Append to the final data
        final_data.append([note_name, note_url, note_content, note_id])
        if only_one_note:
            break

    # Create DataFrame
    df = pd.DataFrame(final_data, columns=["Note Name", "Note URL", "Note Content", "Note ID"])
    st.dataframe(df)
    return df

def create_task_row_properties(task_name, related_project_id, description, status):
    """
    Create properties for a new task row.

    Args:
        task_name (str): Name of the task.
        related_project_id (str): ID of the project related to the task.
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
                    "id": related_project_id
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
