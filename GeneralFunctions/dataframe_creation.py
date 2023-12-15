import pandas as pd


def visualize_notion_database_row_object(notion_db_row):
    """
    Function to visualize a Notion object.
    """

    try:

        data_to_format = [
            {
            "object": notion_db_row["object"]
            #,"id": notion_db_row["id"]
            #,"url": notion_db_row["url"]
            }
        ]
        columns = [
            "object"
            #,"id"
            #,"url"
        ]

        properties = notion_db_row["properties"]

        for property in properties.items():

            #extract property name
            prop_name = property[0]
            
            #extract property type
            prop_type = property[1]["type"]

            if prop_type == "title":
                if property[1]["title"]:
                    prop_value = property[1]["title"][0]["plain_text"]
                else:
                    prop_value = ""

                columns.append(prop_name)
                data_to_format[0][prop_name] = prop_value


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

        if matches["matches"][0]["metadata"]["Type"]:
            columns.append("Type")

        for match in matches["matches"]:

            data_to_format.append([
                match["metadata"]["Name"]if "Name" in match["metadata"] else None,
                match["score"],
                match["metadata"]["Type"] if "Type" in match["metadata"] else None
            ])

        # Create a DataFrame
        df = pd.DataFrame(data_to_format, columns=columns)

        return df

    except Exception as e:
        print(f"Error: {e}")
        return None