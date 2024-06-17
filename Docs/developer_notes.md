# Developer Notes
## TO DOS
Finished

## Completed
- Develop front end interface, including buttons to take to subject pages
- Create csv which can efficiently hold all necessary information
- Allow for the interface to read from the csv
- Allow for user input to edit the csv
- Allow for creation of goals
- Develop graphing module
- Polish looks and functionality, including bugs and error zones

## Problems
- Could not select the individual pages for a subject
- When subjects are deleted it messes up opening new subjects
- Could only delete one goal at a time
- When goals were first added they could not be deleted

## Solutions
- Used an indexed list to hold the subjects so that the opening of the subject page could use the index
- Refreshed the main page when subjects are deleted so that the index of each button is correct
- Refreshed the goals page when a goal is deleted
- Refreshed the goals page when a goal is added including a delete button