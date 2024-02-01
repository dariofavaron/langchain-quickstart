import pandas as pd

def ingest_notion_database(notionClass, database_id):
    # Get the JSON structure of the database
    structure_json = notionClass.get_database_structure(database_id)

    # Query all the components of the database
    components_json = notionClass.query_database(database_id)

    # Extract the dataframe structure from the JSON structure
    dataframe_structure = extract_dataframe_structure(structure_json)

    # Populate the dataframe with the components
    dataframe = populate_dataframe(dataframe_structure, components_json)

    return dataframe

def extract_dataframe_structure(structure_json):
    """
        Extract the dataframe structure from the JSON structure of a Notion Database
        the output structure will be a panda dataframe and need to have
            3 columns: Property name, Property type, Property options (when applicable)
            1 row for each property present in the Database

        https://developers.notion.com/reference/property-object
    """

    
    dataframe_structure = []

    # Extract the main properties that are not in the "properties" key
    for main_prop_name, main_prop_details in structure_json.items():
        if main_prop_name == 'created_time':
            dataframe_structure.append([main_prop_name, 'created_time', main_prop_details])
        elif main_prop_name == 'last_edited_time':
            dataframe_structure.append([main_prop_name, 'last_edited_time', main_prop_details])
        elif main_prop_name == 'created_by':
            dataframe_structure.append([main_prop_name, 'created_by', main_prop_details['object']])
        elif main_prop_name == 'last_edited_by':
            dataframe_structure.append([main_prop_name, 'last_edited_by', main_prop_details['object']])

        # Extract the properties from the properties key
        elif main_prop_name == 'properties':
            
            #manage the properties type one by one
            for prop_name, prop_details in main_prop_details.items():
                prop_type = prop_details["type"]
                prop_options = []

                if prop_type == 'formula': #ok
                    prop_options.append(prop_details['formula']['expression'])
                elif prop_type == 'multi_select': #ok
                    prop_options = [[opt['name'], opt['color']] for opt in prop_details['multi_select']['options']]
                elif prop_type == 'number': #ok
                    prop_options.append(prop_details['number']['format'])
                elif prop_type == 'relation': #ok
                    prop_options.append(prop_details['relation']['database_id'])
                elif prop_type == 'rollup':
                    prop_options.append(prop_details['rollup']['function'])
                    prop_options.append(prop_details['rollup']['relation_property_name'])
                    prop_options.append(prop_details['rollup']['rollup_property_name'])
                elif prop_type == 'select': #ok
                    prop_options = [[opt['name'], opt['color']] for opt in prop_details['select']['options']]
                elif prop_type == 'status': #ok
                    for group in prop_details['status']['groups']:
                        group_options = [group['name'], group['color']]
                        group_option_details = []
                        for option_id in group['option_ids']:
                            for option in prop_details['status']['options']:
                                if option['id'] == option_id:
                                    group_option_details.append([option['name'], option['color']])
                        prop_options.append(group_options + [group_option_details])
                else:
                    # For properties without accepted options
                    prop_options = []
                
                # Add property details to dataframe structure
                dataframe_structure.append([prop_name, prop_type, prop_options])
        else:
            # For other properties
            dataframe_structure.append([main_prop_name, 'other', main_prop_details])
        
    # Create the dataframe
    dataframe_structure = pd.DataFrame(dataframe_structure, columns=['Property name', 'Property type', 'Property options'])
    
    return dataframe_structure

def populate_dataframe(dataframe_structure, components_json):
    # Populate the dataframe with the components
    # and return the populated dataframe
    dataframe = pd.DataFrame()
    # Populate the dataframe based on the dataframe_structure and components_json
    # and return the populated dataframe
    return dataframe
