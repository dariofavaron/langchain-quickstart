
class Prompts:
    """
    A class to store all prompts for the game.

    
    """
    def __init__(self):

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
"related_project_name": "",
"related_project_id": "",
"related_area_name": "",
"task_description": "",
"duplication_check": "",
"project_selection_results": "",
"Suggestions": "",
"Insights": ""
} 
    - Each task should be clearly listed with its name, associated project id, a detailed description, and the comment.

Your goal is to transform the raw input into a well-organized and easily navigable set of tasks, aiding in effective task management and planning.

            """}
        
        self.task_extraction_from_note_inbox_example_request ={"role": "user", "content": """
Note Name: Da avere una lista di cose da fare nei tempi morti, ogni settimana.
Note URL: None
Note Content: Create a list of idle activities, Schedule the activities for the next week
Relevant tasks: columns:["Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"] [['make the list of gifts for next year', 'Christmas 24', 'National Holidays', 'Fun', '4b285732-1b7f-44e7-9bb9-b382baa3ebd8', '2f0750f5-3f7f-4d00-9453-d305d505eb0e', '4bd41969-5171-45d4-902f-4d484962965c', ''], ['Update website', 'lamicadellebambole', 'Mom', 'Family', '442cdf45-aa50-4069-8931-a3be53ca4155', '941427a8-c969-40c1-a3a5-7e4deeb3d300', 'a4ca8ca0-6895-46e0-81f2-61f2c698aef8', ''], ['Defina all possible actions that an automated agent can do', 'Notion', 'Personal Projects', 'Work', '0bf3cdfe-3abe-4629-9b4b-ddfbfd26c675', 'b2968ac9-bd61-4105-b396-5645ab1fc6bf', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', ''], ['Import Keep notes', 'Notion', 'Personal Projects', 'Work', '28874633-2ff0-4471-8534-8667e66f247b', 'b2968ac9-bd61-4105-b396-5645ab1fc6bf', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', '']]
"""}
        self.task_extraction_from_note_inbox_example_assistant = {"role": "assistant", "content": """
{"task_name": "Create a list of idle activities",
"related_project_name": "Weekly Planning",
"related_project_id": "d1cadfcb-5d92-4e35-93af-b8dd22e4baba",
"related_area_name": "Personal Planning",
"task_description": "Start from reading a book, then go for a walk, then do some meditation",
"duplication_check": "No duplicate tasks found in the Relevant Tasks.",
"project_selection_results": "No new project needed, the existing project 'Weekly Planning' in Area 'Personal Planning' is appropriate.",
"Suggestions": "Include a mix of activities that cater to different aspects like physical health, mental well-being, and hobbies.",
"Insights": "Ensure that some activities are purely for relaxation and don't require much mental or physical effort."
}"""}

        self.task_extraction_from_note_inbox_example_request_2 ={"role": "user", "content": """
Note Name: create a Q&A chatbot that uses Notion Workspace in the MVP
Note URL: None
Note Content: 
Relevant tasks: columns:["Task Name", "Project Related", "Area Related", "Area Type", "Task ID", "Project ID", "Area ID", "Task Description"] [['Create a Q&A chatbot using Notion Workspace', 'MVP', 'Personal Projects', 'Work', '3ae7e1b0-31dc-486a-a638-ea70c443d0d9', '088e944d-cd75-444c-a0e4-2db96edf475f', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', 'Develop a Q&A chatbot that utilizes Notion Workspace for information retrieval and interaction.'], ['Import Keep notes', 'Notion', 'Personal Projects', 'Work', '28874633-2ff0-4471-8534-8667e66f247b', 'b2968ac9-bd61-4105-b396-5645ab1fc6bf', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', ''], ['Defina all possible actions that an automated agent can do', 'Notion', 'Personal Projects', 'Work', '0bf3cdfe-3abe-4629-9b4b-ddfbfd26c675', 'b2968ac9-bd61-4105-b396-5645ab1fc6bf', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', ''], ['after uploading the task in notion, update the property archive of the note inbox', 'MVP', 'Personal Projects', 'Work', 'd1eda964-ef3e-4f45-8dcc-4687c24461a9', '088e944d-cd75-444c-a0e4-2db96edf475f', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', ''], ['manage the creation of new Projects and Area, get the structure and fill the blanks. - 2h', 'MVP', 'Personal Projects', 'Work', 'c5e0a5b9-4bef-4f34-90e3-8ea5286af45f', '088e944d-cd75-444c-a0e4-2db96edf475f', '786a19f9-a90f-4a95-897d-8c82a2c0cac2', '']]
"""}
        self.task_extraction_from_note_inbox_example_assistant_2 = {"role": "assistant", "content": """
{"task_name": "Create a Q&A chatbot using Notion Workspace",
"related_project_name": "MVP",
"related_project_id": "088e944d-cd75-444c-a0e4-2db96edf475f",
"related_area_name": "Personal Projects",
"task_description": "Develop a Q&A chatbot that utilizes Notion Workspace for information retrieval and interaction.",
"duplication_check": "This task is a duplicated version of 'Create a Q&A chatbot using Notion Workspace', 'MVP', 'Personal Projects', 'Work'",
"project_selection_results": "No new project needed, the existing project 'MVP' in Area 'Personal Projects' is appropriate.",
"Suggestions": "Consider breaking down the task into smaller subtasks such as designing the chatbot flow, integrating with Notion API, and testing the functionality.",
"Insights": "Ensure to allocate sufficient time for testing and refining the chatbot to ensure seamless integration with Notion Workspace."
}"""}


    def update_prompt(self, new_prompt):
        self.task_extraction_from_note_inbox = new_prompt
