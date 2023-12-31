def create_area_vector_with_extracted_data(json_obj, embeddingClass):
    try:
        # Extracting data
        id_data = (str(json_obj["properties"]["Name"]["title"][0]["text"]["content"]) + 
            " - " +
            str(json_obj["id"]))

        metadata = {
            "object": json_obj["object"],
            "id": json_obj["id"],
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
            "Type": json_obj["properties"]["Type"]["select"]["name"] if "select" in json_obj["properties"]["Type"] else None,
            "Projects": json_obj["properties"]["Projects"]["relation"][0]["id"] if "relation" in json_obj["properties"]["Projects"] else None
        }
        content = {
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
            "Type": json_obj["properties"]["Type"]["select"]["name"] if "select" in json_obj["properties"]["Type"] else None,
            "Projects": json_obj["properties"]["Projects"]["relation"][0]["id"] if "relation" in json_obj["properties"]["Projects"] else None
        }

        # Creating vector
        embedded_content = embeddingClass.generate_embedding(str(content))
        vector = {
            'id': str(id_data),
            'values': embedded_content,
            'metadata': metadata,
        }
        
        return vector
    except Exception as e:
        raise Exception(f"Error in create_area_vector_with_extracted_data: {str(e)}")

def create_project_vector_with_extracted_data(json_obj, embeddingClass):
    try:
        # Extracting data
        id_data = (str(json_obj["properties"]["Name"]["title"][0]["text"]["content"]) + 
            " - " +
            str(json_obj["id"]))
        
        metadata = {
            "object": json_obj["object"],
            "id": json_obj["id"],
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
            "Areas": [relation["id"] for relation in json_obj["properties"]["Areas"]["relation"]] if "relation" in json_obj["properties"]["Areas"] else [],
            "Priority": json_obj["properties"]["Priority"]["status"]["name"] if "status" in json_obj["properties"]["Priority"] else None,
            "Tasks": [relation["id"] for relation in json_obj["properties"]["Tasks"]["relation"]] if "relation" in json_obj["properties"]["Tasks"] else [],
            "Knowledge": [relation["id"] for relation in json_obj["properties"]["Knowledge"]["relation"]] if "relation" in json_obj["properties"]["Knowledge"] else []
        }
        content = {
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
            "Areas": [relation["id"] for relation in json_obj["properties"]["Areas"]["relation"]] if "relation" in json_obj["properties"]["Areas"] else [],
            "Priority": json_obj["properties"]["Priority"]["status"]["name"] if "status" in json_obj["properties"]["Priority"] else None,
            "Tasks": [relation["id"] for relation in json_obj["properties"]["Tasks"]["relation"]] if "relation" in json_obj["properties"]["Tasks"] else [],
            "Knowledge": [relation["id"] for relation in json_obj["properties"]["Knowledge"]["relation"]] if "relation" in json_obj["properties"]["Knowledge"] else []
        }

        # Creating vector
        embedded_content = embeddingClass.generate_embedding(str(content))
        vector = {
            'id': str(id_data),
            'values': embedded_content,
            'metadata': metadata,
        }
        return vector
    except Exception as e:
        raise Exception(f"Error in create_project_vector_with_extracted_data: {str(e)}")


def create_task_vector_with_extracted_data(json_obj, embeddingClass):
    try:
        # Extracting data
        id_data = (str(json_obj["properties"]["Name"]["title"][0]["text"]["content"]) + 
            " - " +
            str(json_obj["id"]))
        
        metadata = {
            "object": json_obj["object"],
            "id": json_obj["id"],
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
            "Status": json_obj["properties"]["Status"]["status"]["name"] if "status" in json_obj["properties"]["Status"] else None

        }
        content = {
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
            "Projects": [relation["id"] for relation in json_obj["properties"]["Projects"]["relation"]] if "relation" in json_obj["properties"]["Projects"] else [],
            "Knowledge": [relation["id"] for relation in json_obj["properties"]["Knowledge"]["relation"]] if "relation" in json_obj["properties"]["Knowledge"] else [],
            "Description": json_obj["properties"]["Description"]["rich_text"][0]["text"]["content"] if "rich_text" in json_obj["properties"]["Description"] and json_obj["properties"]["Description"]["rich_text"] else None
        }

        # Creating vector
        embedded_content = embeddingClass.generate_embedding(str(content))
        vector = {
            'id': str(id_data),
            'values': embedded_content,
            'metadata': metadata,
        }
        return vector
    except Exception as e:
        raise Exception(f"Error in create_task_vector_with_extracted_data: {str(e)}")

def create_full_task_vector(tasks_dataframe, embeddingClass):
    """
        - id: Area - Project - Task
        - metadata: "Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID"
        - content: "Task Name", "Project Related", "Area Related", "Area Type", “Task Description”

        df = pd.DataFrame(final_data, columns=["Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"])

    """
    try:

        vectors = []
        for _,task in tasks_dataframe.iterrows():

            # Extracting data
            id_data = (
                task["Area Related"] +
                " - " +
                task["Project Related"] +
                " - " +
                task["Task Name"]
                )
            
            metadata = {
                "Task Name": task["Task Name"],
                "Project Related": task["Project Related"],
                "Area Related": task["Area Related"],
                "Area Type": task["Area Type"],
                "Task ID": task["Task ID"],
                "Project ID": task["Project ID"],
                "Area ID": task["Area ID"]
            }

            content = {
                "Task Name": task["Task Name"],
                "Project Related": task["Project Related"],
                "Area Related": task["Area Related"],
                "Area Type": task["Area Type"],
                "Task Description": task["Task Description"]
            }

            # Creating vector
            embedded_content = embeddingClass.generate_embedding(str(content))
            vector = {
                'id': str(id_data),
                'values': embedded_content,
                'metadata': metadata,
            }
            vectors.append(vector)
        
        return vectors
    except Exception as e:
        raise Exception(f"Error in create_full_task_vector: {str(e)}")


def create_new_note_vector_with_extracted_data(id, object, page_name, page_properties_url, page_content, embeddingClass):
    try:
        # Extracting data
        id_data = (page_name +
            " - " +
            str(id))

        metadata = {
            "object": object,
            "id": id,
            "Name": page_name
        }
        content = {
            "Name": page_name,
            "URL": page_properties_url if page_properties_url else None,
            "Content": page_content if page_content else None
        }

        # Creating vector
        embedded_content = embeddingClass.generate_embedding(str(content))
        vector = {
            'id': str(id_data),
            'values': embedded_content,
            'metadata': metadata,
        }
        return vector
    except Exception as e:
        raise Exception(f"Error in create_new_note_vector_with_extracted_data: {str(e)}")
