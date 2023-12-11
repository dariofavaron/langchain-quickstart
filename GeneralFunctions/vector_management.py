def create_area_vector_with_extracted_data(json_obj, embeddingClass):
    # Extracting data
    id_data = (str(json_obj["properties"]["Name"]["title"][0]["text"]["content"]) + 
        str(json_obj["id"]))

    metadata = {
        "object": json_obj["object"],
        "id": json_obj["id"],
        "created_time": json_obj["created_time"],
        "last_edited_time": json_obj["last_edited_time"],
        "created_by": json_obj["created_by"]["id"],
        "last_edited_by": json_obj["last_edited_by"]["id"],
        #"archived": json_obj["archived"],
        #"cover": json_obj["cover"],
        #"icon": json_obj["icon"],
        "parent": json_obj["parent"]["database_id"],
        "url": json_obj["url"],
        #"public_url": json_obj["public_url"],
        # Properties
        "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
        "Type": json_obj["properties"]["Type"]["select"]["name"] if "select" in json_obj["properties"]["Type"] else None,
        "Projects": json_obj["properties"]["Projects"]["relation"][0]["id"] if "relation" in json_obj["properties"]["Projects"] else None
    }
    content = {
        "id": json_obj["id"],
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

def create_project_vector_with_extracted_data(json_obj, embeddingClass):
    # Extracting data
    id_data = {
        "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
        "id" : json_obj["id"]
    }
    metadata = {
        "object": json_obj["object"],
        "id": json_obj["id"],
        "created_time": json_obj["created_time"],
        "last_edited_time": json_obj["last_edited_time"],
        "created_by": json_obj["created_by"]["id"],
        "last_edited_by": json_obj["last_edited_by"]["id"],
        #"archived": str(json_obj["archived"]),
        #"cover": json_obj["cover"],
        #"icon": json_obj["icon"],
        "parent": json_obj["parent"]["database_id"],
        "url": json_obj["url"],
        #"public_url": json_obj["public_url"],
        # Properties
        "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
        "Areas": [relation["id"] for relation in json_obj["properties"]["Areas"]["relation"]] if "relation" in json_obj["properties"]["Areas"] else [],
        "Priority": json_obj["properties"]["Priority"]["status"]["name"] if "status" in json_obj["properties"]["Priority"] else None,
        "Tasks": [relation["id"] for relation in json_obj["properties"]["Tasks"]["relation"]] if "relation" in json_obj["properties"]["Tasks"] else [],
        "Knowledge": [relation["id"] for relation in json_obj["properties"]["Knowledge"]["relation"]] if "relation" in json_obj["properties"]["Knowledge"] else []
    }
    content = {
        "id": json_obj["id"],
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


def create_task_vector_with_extracted_data(json_obj, embeddingClass):
    # Extracting data
    id_data = {
        "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
        "id" : json_obj["id"]
    }
    metadata = {
        "object": json_obj["object"],
        "id": json_obj["id"],
        "created_time": json_obj["created_time"],
        "last_edited_time": json_obj["last_edited_time"],
        "created_by": json_obj["created_by"]["id"],
        "last_edited_by": json_obj["last_edited_by"]["id"],
        #"archived": json_obj["archived"],
        #"cover": json_obj["cover"],
        #"icon": json_obj["icon"],
        "parent": json_obj["parent"]["database_id"],
        "url": json_obj["url"],
        #"public_url": json_obj["public_url"],
        # Properties
        "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
        "Projects": [relation["id"] for relation in json_obj["properties"]["Projects"]["relation"]] if "relation" in json_obj["properties"]["Projects"] else [],
        "Knowledge": [relation["id"] for relation in json_obj["properties"]["Knowledge"]["relation"]] if "relation" in json_obj["properties"]["Knowledge"] else [],
        "Status": json_obj["properties"]["Status"]["status"]["name"] if "status" in json_obj["properties"]["Status"] else None,
        "Description": json_obj["properties"]["Description"]["rich_text"][0]["text"]["content"] if "rich_text" in json_obj["properties"]["Description"] and json_obj["properties"]["Description"]["rich_text"] else None

    }
    content = {
        "id": json_obj["id"],
        "Name": json_obj["properties"]["Name"]["title"][0]["text"]["content"],
        "Projects": [relation["id"] for relation in json_obj["properties"]["Projects"]["relation"]] if "relation" in json_obj["properties"]["Projects"] else [],
        "Knowledge": [relation["id"] for relation in json_obj["properties"]["Knowledge"]["relation"]] if "relation" in json_obj["properties"]["Knowledge"] else [],
        "Status": json_obj["properties"]["Status"]["status"]["name"] if "status" in json_obj["properties"]["Status"] else None,
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
