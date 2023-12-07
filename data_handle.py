import pandas as pd

def visualize_notion_db_properties(db_response):
    """
    Takes the JSON response from a Notion API query for a database,
    and formats the relevant details into a DataFrame for visualization,
    including properties like 'relation', 'rollup', 'status', and 'date'.
    """
    try:
        properties = db_response["properties"]
        data = []

        for prop_name, prop_details in properties.items():
            prop_type = prop_details["type"]
            options = ""
            related_db_id = ""

            # For 'select' and 'status' types, extract options
            if prop_type in ["select", "status"]:
                if 'options' in prop_details:
                    options = " - ".join([f"{opt['name']}, {opt['color']}" for opt in prop_details["options"]])

            # For 'relation' and 'rollup' types, extract related database ID
            if prop_type in ["relation", "rollup"]:
                related_db_id = prop_details["relation"]["database_id"]

            # Additional property type handling can be added here if needed

            data.append([prop_name, prop_type, options, related_db_id])

        # Create a DataFrame
        df = pd.DataFrame(data, columns=["Property", "Type", "Options", "Related Database ID"])
        return df

    except KeyError as e:
        print(f"Error: {e} key not found in the JSON response.")
        return None
