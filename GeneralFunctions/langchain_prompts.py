
from langchain.llms.openai import OpenAI
from langchain.output_parsers import PandasDataFrameOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import BaseLLM


def langchain_to_convert_json_to_df(inbox_note_to_review):
    """
    Function to convert the JSON response from the Notion API into a DataFrame.
    """
    try:
        model_name = "text-davinci-003"
        temperature = 0.5
        model = OpenAI(model_name=model_name, temperature=temperature)

        properties = inbox_note_to_review["properties"]
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