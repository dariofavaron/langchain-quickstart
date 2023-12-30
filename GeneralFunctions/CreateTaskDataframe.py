import pandas as pd

def create_task_table(areas_json, projects_json, tasks_json):
    # Parse the JSON data
    areas = areas_json["results"]
    projects = projects_json["results"]
    tasks = tasks_json["results"]

    # Create dictionaries for quick ID to name mapping
    area_id_to_name = {area["id"]: area["properties"]["Name"]["title"][0]["plain_text"] for area in areas}
    project_id_to_name = {project["id"]: project["properties"]["Name"]["title"][0]["plain_text"] for project in projects}

    # List to hold the task data
    task_data = []

    # Iterate through tasks to build the task data
    for task in tasks:
        task_name = task["properties"]["Name"]["title"][0]["plain_text"]
        project_ids = [relation["id"] for relation in task["properties"]["Projects"]["relation"]]
        area_ids = [relation["id"] for relation in task["properties"]["Areas"]["rollup"]["array"][0]["relation"]]

        # Find corresponding project and area names
        project_names = [project_id_to_name.get(pid, "Unknown") for pid in project_ids]
        area_names = [area_id_to_name.get(aid, "Unknown") for aid in area_ids]

        # Create a record for each project-area combination
        for project_name in project_names:
            for area_name in area_names:
                task_data.append([task_name, project_name, area_name])

    # Convert the list to a DataFrame
    df = pd.DataFrame(task_data, columns=["Task Name", "Project Related to the Task", "Area Related to the Task"])
    return df

