

def extract_metadata_and_content_ares(json_obj):
    metadata = {
        "id": json_obj["id"],
        "created_time": json_obj["created_time"],
        "last_edited_time": json_obj["last_edited_time"],
        "created_by": json_obj["created_by"]["id"],
        "last_edited_by": json_obj["last_edited_by"]["id"],
        "archived": json_obj["archived"]
    }
    content = json_obj["properties"]["Name"]["title"][0]["text"]["content"]
    return metadata, content
