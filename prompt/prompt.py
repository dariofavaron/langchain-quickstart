
class Prompts:
    """
    A class to store all prompts for the game.

    
    """
    def __init__(self):

        self.task_extraction_from_note_inbox = [
            {"role": "system", "content": """
Your role is to extract tasks from the provided notes. 

There are few files attached that are the Database extraction of Notion. use them if needed to create context.
Areas: These are parts of your life that require ongoing attention and maintenance but don't have a specific end date,
Projects: These are defined as a series of tasks that have a goal or outcome.
Tasks: single operations that require an action. connected to a project.
Inbox Notes: all the new tasks, ideas, or information that will be categorized in the Task list.

i will provide as input the note inbox object as Note inbox.

. **Detailed Task Extraction:**
    - For each item or action mentioned in the note, create an individual task.
    - Ensure that the specificity and context of each item/action are preserved.
. **Duplication Check:**
    - Conduct a granular-level check for duplicates, considering each item in the note.
    - Compare with existing tasks to identify any redundancies.
. **Classification and Categorization:**
    - Classify each extracted item as a task.
    - Categorize each task under the most suitable area and project, based on existing lists.
. **Comment Creation:**
    - Provide detailed feedback for each task, explaining its categorization.
    - Include suggestions for improvement and insights for task optimization.
. **Output Format:**
    - Present the refined tasks in a markdown table format.
    - Each task should have its own row, with columns for the task's name, associated area and project, detailed description, and status.

            """},

            {"role": "user", "content": """
Note Name: Da avere una lista di cose da fare nei tempi morti, ogni settimana.
Note URL: None
Note Content: None
Already existing areas: {"Name":{"0":"National Holidays","1":"Holidays","2":"Food","3":"Shopping","4":"Personal Projects","5":"Social Events","6":"Plants","7":"Friends","8":"Dad","9":"Fitness","10":"Legal","11":"Mental Health","12":"Finance","13":"Digital Services","14":"Mom","15":"Organization","16":"Self Improvement","17":"Cleaning","18":"Transportation","19":"Sister","20":"Amazon","21":"Africa Pet"}}
Already existing Projects: {"Name":{"0":"Weekend Trips","1":"National Holidays","2":"Things to buy","3":"Encoder Stefano","4":"Learn Spanish","5":"lamicadellebambole","6":"Meditation","7":"Cleaning Schedule","8":"Digital Wishes","9":"Keep in touch","10":"Festivals","11":"Keep in touch","12":"Keep in touch","13":"Meal Planner","14":"Groceries","15":"Automatize reports","16":"Daily Training","17":"Christmas","18":"House Plants","19":"Drone","20":"Keep in Touch","21":"Friend Database","22":"Clothes","23":"Barcelona Food","24":"Identity cards","25":"Insurance","26":"Damasystem","27":"New Project","28":"Sports","29":"Barcelona Events","30":"Big Travel","31":"Blue Badge","32":"Boat","33":"Media Collection","34":"Communication and Empathy","35":"Christmas 23","36":"Empadronimiento in Spain","37":"Files on Cloud","38":"Define place for objects","39":"Review Art","40":"Morning Routine","41":"AI Task Manager App","42":"Shared Passions","43":"Veterinary","44":"Psychotherapy","45":"Networking","46":"Van","47":"Notion","48":"Storage Room","49":"Investments"}}
Already existing Tasks: {"Name":{"0":"Create Yearly report","1":"Defina all possible actions that an automated agent can do","2":"Find articles on the topic, new technology","3":"Update website","4":"Find best health insurance in Spain","5":"buy ticket plane to back Barcelona","6":"Create Backup schedule for all digital content","7":"Calculate amount to invest each month","8":"define automatically how to differentiate the income and expenses","9":"Setup automatic downloader of movie","10":"Define morning routine","11":"Create month summary","12":"Calesthenic challenge","13":"import in a single place all medias","14":"Import Keep notes","15":"buy return flight from it to bcn","16":"Set up plex","17":"Create excel file with one tab per bank accout","18":"Check logs for malitious actions","19":"define specs of new SERVER","20":"Updates the OS"}}
            """},
            {"role": "assistant", "content": """
## Tasks:

| Name | Area | Project | Description | Status |
| --- | --- | --- | --- | --- |
| Create a list of idle activities | Personal Planning| Weekly Planning | Create a list of activities for idle times | Not started |
| Schedule the activities for the next week | Personal Planning| Weekly Planning | Create a schedule of activities for idle times in the following week | Not started |

### Comments:

- **Areas**: Created "Personal Planning". Could not fit in existing area "Personal Projects".
- **Project**: Created "Weekly planning". For organizing weekly activities.
- **Task**: 2 tasks extracted, single and unique, no duplicate or similar found.

### Suggestions:

- **Flexibility**: Keep the schedule flexible to adapt to unexpected changes in the week.
- **Review and Adjust**: At the end of each week, review what worked and what didn't, and adjust the list and schedule accordingly.
- **Include Relaxation Time**: Ensure that some activities are purely for relaxation and don't require much mental or physical effort.
- **Diversify Activities**: Include a mix of activities that cater to different aspects like physical health, mental well-being, and hobbies.
                """
            }
        ]

        self.parse_extracted_task_to_notion = [
        {"role": "system", "content": """
Your role is to parse the extracted tasks and format them to be aligned with the Notion Database.
            """},

            {"role": "user", "content": """

## Tasks:

| Name | Area | Project | Description | Status |
| --- | --- | --- | --- | --- |
| Create a list of idle activities | Personal Planning| Weekly Planning | Create a list of activities for idle times | Not started |
| Schedule the activities for the next week | Personal Planning| Weekly Planning | Create a schedule of activities for idle times in the following week | Not started |

### Comments:

- **Areas**: Created "Personal Planning". Could not fit in existing area "Personal Projects".
- **Project**: Created "Weekly planning". For organizing weekly activities.
- **Task**: 2 tasks extracted, single and unique, no duplicate or similar found.

### Suggestions:

- **Flexibility**: Keep the schedule flexible to adapt to unexpected changes in the week.
- **Review and Adjust**: At the end of each week, review what worked and what didn't, and adjust the list and schedule accordingly.
- **Include Relaxation Time**: Ensure that some activities are purely for relaxation and don't require much mental or physical effort.
- **Diversify Activities**: Include a mix of activities that cater to different aspects like physical health, mental well-being, and hobbies.

            """},
            {"role": "assistant", "content": """
prova
"""}
        ]

    def update_prompt(self, new_prompt):
        self.task_extraction_from_note_inbox = new_prompt
