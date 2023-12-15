import pandas as pd


def visualize_notion_database_row_object(notion_db_row, page_content):
    """
    Function to visualize a Notion object.
    """

    try:

        data_to_format = []

        columns = [
            "Object", "Name", "Content"
        ]

        data_to_format.append([
            "Object": notion_db_row["object"],
            "Name": notion_db_row["properties"]["Name"]["title"][0]["text"]["content"] if "title" in notion_db_row["properties"]["Name"]["title"] else None,
            "Content": page_content if page_content else None
            ])

        # Create a DataFrame
        df = pd.DataFrame(data_to_format, columns=columns)

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
    


def visualize_retrieved_vectors(matches):
    """
    take as an input a list of matches and return a dataframe with selected metadata
    """

    try:
        data_to_format = []
        columns = ["Name", "Score"]

        #if matches["matches"][0]["metadata"]["Type"]:
        #    columns.append("Type")

        for match in matches["matches"]:

            data_to_format.append([
                match["metadata"]["Name"]if "Name" in match["metadata"] else None,
                match["score"]
            #    ,match["metadata"]["Type"] if "Type" in match["metadata"] else None
            ])

        # Create a DataFrame
        df = pd.DataFrame(data_to_format, columns=columns)

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None