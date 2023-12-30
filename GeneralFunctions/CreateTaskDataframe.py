import pandas as pd

def create_task_table(areas_json, project_json, task_json):
    """
    Create a DataFrame table with task name, project related to the task, and area related to the task.

    :param areas_json: JSON data for areas
    :param project_json: JSON data for projects
    :param task_json: JSON data for tasks
    :return: DataFrame with the required information
    """

    # Extracting necessary information
    area_name = areas_json["properties"]["Name"]["title"][0]["plain_text"]
    area_projects = [relation["id"] for relation in areas_json["properties"]["Projects"]["relation"]]

    project_name = project_json["properties"]["Name"]["title"][0]["plain_text"]
    project_areas = [relation["id"] for relation in project_json["properties"]["Areas"]["relation"]]
    project_tasks = [relation["id"] for relation in project_json["properties"]["Tasks"]["relation"]]

    task_name = task_json["properties"]["Name"]["title"][0]["plain_text"]
    task_projects = [relation["id"] for relation in task_json["properties"]["Projects"]["relation"]]

    # Creating the dataframe
    df_data = []

    # Check if the task is related to the project
    if task_json["id"] in project_tasks:
        df_data.append({
            "task_name": task_name,
            "project_related_to_task": project_name,
            "area_related_to_task": area_name if project_json["id"] in area_projects else "N/A"
        })

    df = pd.DataFrame(df_data, columns=["task_name", "project_related_to_task", "area_related_to_task"])
    return df

