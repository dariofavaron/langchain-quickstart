
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
| Create a list of idle activities | Personal Planning| Weekly Planning | Create a list of activities for idle times | Ai Generated |
| Schedule the activities for the next week | Personal Planning| Weekly Planning | Create a schedule of activities for idle times in the following week | Ai Generated |

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

        self.task_extraction_from_note_inbox_system = {"role": "system", "content": """
Your role is to methodically process and organize tasks from the provided notes, which include details about personal and work-related activities. You'll be working with data extracted from a Notion database, which categorizes life aspects into Areas, Projects, and Tasks. An Inbox Notes section contains new tasks, ideas, or information to be categorized.

When you receive the input - consisting of the note name, URL, content, relevant tasks, and all projects with their respective IDs - your responsibilities are as follows:

1. **Detailed Task Extraction:**
    - Extract individual tasks from each note, ensuring clarity and context are maintained.
    - This involves recognizing and outlining specific actions or items mentioned in the notes.
2. **Duplication Check:**
    - Carefully review each extracted item for duplicates.
    - Compare new tasks with existing ones to avoid redundancy.
3. **Classification and Categorization:**
    - Assign each task to the appropriate category, considering its nature and relevance to existing areas and projects.
    - This step involves thoughtful analysis of how each task fits into the broader system.
4. **Comment Creation:**
    - For each task, provide insightful commentary.
    - This should include the rationale behind its categorization, along with any suggestions for task enhancement or efficiency.
    - The comment need to have a section  with the results of the research of duplicate tasks  
5. **Output Format:**
    - Present the organized tasks in a structured json following this example:
        {"task_name": "",
        "related_project_id": "",
        "task_description": "",
        "comment": "duplication check results for task, project selection results, suggestions, and insights"} 
    - Each task should be clearly listed with its name, associated project id, a detailed description, and the comment.

Your goal is to transform the raw input into a well-organized and easily navigable set of tasks, aiding in effective task management and planning.

            """}
        
        self.task_extraction_from_note_inbox_example_request ={"role": "user", "content": """
Note Name: Da avere una lista di cose da fare nei tempi morti, ogni settimana.
Note URL: None
Note Content: Create a list of idle activities, Schedule the activities for the next week
Relevant tasks: columns: ["Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"] [['make the list of gifts for next year', 'Christmas 24', 'National Holidays', 'Fun', '4b285732-1b7f-44e7-9bb9-b382baa3ebd8', '2f0750f5-3f7f-4d00-9453-d305d505eb0e', '4bd41969-5171-45d4-902f-4d484962965c', ''], ['Update website', 'lamicadellebambole', 'Mom', 'Family', '442cdf45-aa50-4069-8931-a3be53ca4155', '941427a8-c969-40c1-a3a5-7e4deeb3d300', 'a4ca8ca0-6895-46e0-81f2-61f2c698aef8', ''], ['Defina all possible actions that an automated agent can do', 'Notion', 'Personal Projects', 'Work', '0bf3cdfe-3abe-4629-9b4b-ddfbfd26c675', 'b2968ac9-bd61-4105-b396-5645ab1fc6bf', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', ''], ['Import Keep notes', 'Notion', 'Personal Projects', 'Work', '28874633-2ff0-4471-8534-8667e66f247b', 'b2968ac9-bd61-4105-b396-5645ab1fc6bf', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', ''], ['find location of weekend trips around barcelona', 'Weekend Trips', 'Holidays', 'Fun', 'd5d6e2f4-5598-42f4-bd18-bb3911c7f18d', 'f8b893bb-dd1b-4305-8ff0-5bec98464ce9', '8d163f49-d55d-4350-a929-3d0fedf108ba', ''], ['plan africa trip', 'Big Travel', 'Holidays', 'Fun', '7f5c57b8-af63-48be-a32b-9a86982bfe52', '70b0c5a7-79e9-4965-bbb3-9f05485ec788', '8d163f49-d55d-4350-a929-3d0fedf108ba', ''], ['Calesthenic challenge', 'Sports', 'Fitness', 'Fun', '1b908c2c-2f8a-441d-8a57-4aaef6562c1f', 'a2476530-b182-4c9b-b9ca-356b0b7196d8', '6d3c1ef8-0e07-403d-9c82-e72ee4a8b8c1', ''], ['Create Yearly report', 'Investments', 'Finance', 'Myself', '937b5992-b582-4fd0-9d11-327163fe96bb', '64849736-e097-4397-a73f-2ac6effd5b5a', 'a44471fa-a95e-4b84-be01-e79af0d36a5d', ''], ['Find articles on the topic, new technology', 'NAS management', 'Digital Services', 'Myself', '37c3ae99-3d55-4ba1-a15a-dbd79332f2bf', '287e7ff7-5b81-42d2-bf53-0bc1be3a9064', '995c8454-3367-4369-8ed3-74132d970985', ''], ['Create Backup schedule for all digital content', 'NAS management', 'Digital Services', 'Myself', 'c260737f-e326-4737-8083-52a6fbb4c80e', '287e7ff7-5b81-42d2-bf53-0bc1be3a9064', '995c8454-3367-4369-8ed3-74132d970985', ''], ['define automatically how to differentiate the income and expenses', 'Automatize reports', 'Finance', 'Myself', '97390f0e-b2f7-44c1-bb71-0bc38e7cd601', 'fa87aa72-b6a3-4019-93cb-706f07d83775', 'a44471fa-a95e-4b84-be01-e79af0d36a5d', ''], ['Define morning routine', 'Morning Routine', 'Mental Health', 'Myself', '282cf512-0ca1-4391-b240-0f3848bff707', 'd80d226c-84e2-403a-a180-0de78d99446f', '9ac83912-0b67-4ceb-b94f-bf4fce504bd4', ''], ['Create month summary', 'Investments', 'Finance', 'Myself', 'ce0396cd-985a-4b48-b686-0108d458fd7d', '64849736-e097-4397-a73f-2ac6effd5b5a', 'a44471fa-a95e-4b84-be01-e79af0d36a5d', ''], ['import in a single place all medias', 'Media Collection', 'Digital Services', 'Myself', '319d5d32-6145-4338-b649-49d26baae6ea', '35c28b8a-9934-4de2-8956-0a2dd7b0f48a', '995c8454-3367-4369-8ed3-74132d970985', ''], ['Create excel file with one tab per bank accout', 'Automatize reports', 'Finance', 'Myself', 'ae7222de-6bbe-4330-a890-96fffe28eb30', 'fa87aa72-b6a3-4019-93cb-706f07d83775', 'a44471fa-a95e-4b84-be01-e79af0d36a5d', ''], ['Setup automatic downloader of movie', 'Media Collection', 'Digital Services', 'Myself', 'd3752a6c-61c8-4275-b785-1da18bd20257', '35c28b8a-9934-4de2-8956-0a2dd7b0f48a', '995c8454-3367-4369-8ed3-74132d970985', ''], ['define specs of new SERVER', 'NAS management', 'Digital Services', 'Myself', '93aae1a0-2611-4bbf-b20e-62e1c71b10e6', '287e7ff7-5b81-42d2-bf53-0bc1be3a9064', '995c8454-3367-4369-8ed3-74132d970985', ''], ['Calculate amount to invest each month', 'Investments', 'Finance', 'Myself', '089531b6-c089-48ce-a67f-c116c3f6a059', '64849736-e097-4397-a73f-2ac6effd5b5a', 'a44471fa-a95e-4b84-be01-e79af0d36a5d', ''], ['Buy a tourtle neck sweather', 'Clothes', 'Shopping', 'Fun', 'a4fd020e-3086-4c3c-8c31-c85363f47bf8', '7db49046-822c-4ee8-98cd-1a9584ad0e40', '5b0a4ff8-9449-4624-818a-07fb23b1acc2', ''], ['Find best health insurance in Spain', 'Insurance', 'Legal', 'Home', 'ada45950-fccd-48eb-8150-53e30c2c1212', 'e6e44aba-e750-471b-85b2-839fe392fbc1', 'c26d92fc-390f-421f-b4c7-5e99f17437ac', '']]
"""}
        self.task_extraction_from_note_inbox_example_assistant = {"role": "assistant", "content": """
{"task_name": "Create a list of idle activities",
"related_area_name": "Personal Planning",
"related_project_name": "Weekly Planning",
"related_project_id": "d1cadfcb-5d92-4e35-93af-b8dd22e4baba",
"task_description": "Start from reading a book, then go for a walk, then do some meditation",
"comment": "duplication check results for task: No duplicate task found.",
"project_selection_results": "No new project needed, the existing project 'Weekly Planning' in Area 'Personal Planning' is appropriate.",
"Suggestions": "Include a mix of activities that cater to different aspects like physical health, mental well-being, and hobbies.",
"Insights": "Ensure that some activities are purely for relaxation and don't require much mental or physical effort."
}"""}


    def update_prompt(self, new_prompt):
        self.task_extraction_from_note_inbox = new_prompt
