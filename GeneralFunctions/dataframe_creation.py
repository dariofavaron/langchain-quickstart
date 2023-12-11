import pandas as pd

def visualize_notion_database_row_object(notion_db_row):
    """
    Function to visualize a Notion object.
    """
    try:

        data = [
            {
            "Object": notion_db_row["object"],
            "id": notion_db_row["id"],
            "url": notion_db_row["url"]
            }
        ]

        #scan the input jason properties and append to the dataframe structure the properties
        # Create a DataFrame
        df = pd.DataFrame(data, columns=["Object", "id", "url"])

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None 



def visualize_notion_db_properties(db_response):
    """
    Improved version of the function to visualize Notion database properties.
    This version includes handling for 'status' and 'rollup' property types.
    """
    try:
        properties = db_response["properties"]
        data = []

        for prop_name, prop_details in properties.items():
            prop_type = prop_details["type"]
            options = ""
            related_db_id = ""

            # For 'select' types, extract options
            if prop_type == "select":
                if 'options' in prop_details.get(prop_type, {}):
                    options = " - ".join([f"{opt['name']}, {opt['color']}"
                                          for opt in prop_details[prop_type]["options"]])
                    
            # For 'status' types, extract options
            if prop_type == "status":
                if 'options' in prop_details.get(prop_type, {}):
                    options = " - ".join([f"{opt['name']}, {opt['color']}"
                                          for opt in prop_details[prop_type]["options"]])
            
            # For 'relation' and 'rollup' types, extract related database ID
            if prop_type in ["relation"]:
                related_db_id = prop_details[prop_type]["database_id"]

            # Additional property type handling can be added here if needed

            data.append([prop_name, prop_type, options, related_db_id])

        # Create a DataFrame
        df = pd.DataFrame(data, columns=["Property", "Type", "Options", "Related Database ID"])
        return df

    except KeyError as e:
        print(f"Error: {e} key not found in the JSON response.")
        return None