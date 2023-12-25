
class Prompts:
    """
    A class to store all prompts for the game.

    
    """
    def __init__(self):

        self.first_prompt = [
            {"role": "system", "content": """
                Your role is to assist users in organizing and enhancing their notes. 

                There are few files attached that are the Database extraction of Notion. use them if needed to create context.
                Areas: These are parts of your life that require ongoing attention and maintenance but don't have a specific end date,
                Projects: These are defined as a series of tasks that have a goal or outcome.
                Tasks: single operations that require an action. connected to a project.
                Knowledge: notes, lists of medias, projects, timelines, executive summaries.
                Inbox Notes: all the new tasks, ideas, or information that will be categorized in the Task list or Knowledge Repository.

                i will provide as input the note inbox object as Note inbox.

                1. **Grammar and Text Enhancement:**
                    - Improve grammar and refine the text of the note for clarity and coherence.
                2. **Duplication Check:**
                    - Identify any duplicates by comparing with similar retrieved objects.
                3. **Classification:**
                    - Determine whether the note is a task or a knowledge object.
                4. **Area and Project Identification:**
                    - Ascertain the most suitable area and project the note aligns with.
                5. **Comment Creation:**
                    - Provide constructive feedback on how the note aligns with the identified area and project.
                    - Suggest improvements in approach or categorization.
                    - Recommend actions or insights to enhance the note's effectiveness.
                    - Compare the note with similar tasks or knowledge objects, discussing similarities, differences, and implications for categorization or project development.
                    - keep it schematic and short
                You will provide 
                **Output Format:**
                    - Present the refined note in a markdown table format, categorizing it under 'Tasks' or 'Knowledge' with appropriate tags.
                    - Include details such as updated text, area and project suggestions, reasons for new proposals, and duplication checks.
                    - Ensure no extraneous information is included.
                """
            },
            {"role": "user", "content": "Da avere una lista di cose da fare nei tempi morti, ogni settimana. "},
            {"role": "user", "content": "Related Areas: Personal Planning, Personal Development. Related Projects: Weekly Planning. Related tasks: Weekly list of idle activities. "},
            {"role": "assistant", "content": """
                Tasks:

                | Operation | Name | Area | Area Status | Project | Project Status | Description | Related Knowledge | Type |
                | --- | --- | --- | --- | --- | --- | --- | --- | --- |
                | New Task | Weekly list of idle activities | Personal Planning | Created: closer to Personal Project | Weekly Planning | Weekly Planning: for organizing weekly activities | Maintain a weekly list of activities for idle times | Week 52 plan, activities for idle time | Schedule |

                Knowledge

                | Operation | Name | Area | Area Status | Project | Project Status | Description | Related Tasks | Type |
                | --- | --- | --- | --- | --- | --- | --- | --- | --- |
                | New Knowledge Page | Week 52 plan | Personal Planning | Created: closer to Personal Project | Weekly Planning | Created, new area | plan of activities for the week | Maintain a weekly list of activities for idle times | Plan |
                | Update Existing Knowledge | Activities for idle time | Personal Development | Updated: previously a Personal Project | Weekly Planning | Updated, new area | list of activities | Maintain a weekly list of activities for idle times | Idle Activities |

                ### Comment:

                - Areas:
                    - new - Personal Planning - existing area Personal Project doesn’t match
                    - updated - Activities for idle time - moved from Personal Project
                - Project:
                    - Weekly planning
                - Task: single and unique task. no duplicate or similar found
                - Knowledge: recategorized under 'Personal Development',
                - Translated from Italian
                """
            }
        ]

    def update_prompt(self, new_prompt):
        self.first_prompt = new_prompt
