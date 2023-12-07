import pandas as pd

def visualize_notion_db_properties(db_response):
    """
    Takes the JSON response from a Notion API query for a database,
    and formats the relevant details into a DataFrame for visualization.
    """
    properties = db_response["properties"]
    data = []

    for prop_name, prop_details in properties.items():
        prop_type = prop_details["type"]
        
        # For 'select' type, extract options
        if prop_type == "select":
            options = ", ".join([f"{opt['name']}, {opt['color']}" for opt in prop_details["select"]["options"]])
        else:
            options = ""

        # For 'relation' type, extract related database ID
        if prop_type == "relation":
            related_db_id = prop_details["relation"]["database_id"]
        else:
            related_db_id = ""

        data.append([prop_name, prop_type, options, related_db_id])

    # Create a DataFrame
    df = pd.DataFrame(data, columns=["Property", "Type", "Options", "Related Database ID"])
    return df