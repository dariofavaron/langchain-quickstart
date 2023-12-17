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


def create_new_note_vector_with_extracted_data(json_obj, page_content, embeddingClass):
    try:
        # Extracting data
        id_data = (str(json_obj["properties"]["Name"]["title"][0]["text"]["content"] if "title" in json_obj["properties"]["Name"]["title"] else None) +
            " - " +
            str(json_obj["id"]))

        metadata = {
            "object": json_obj["object"],
            "id": json_obj["id"],
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"] if "title" in json_obj["properties"]["Name"]["title"] else None
        }
        content = {
            "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"] if "title" in json_obj["properties"]["Name"]["title"] else None,
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
