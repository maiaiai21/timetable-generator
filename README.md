# Automated School Timetable Generator
## Overview
The Automated School Timetable Generator is a Python application that automates the creation and management of school timetables. It integrates a Tkinter GUI with a MySQL database backend to handle subjects, professors, and teaching hours, while providing features to generate, view, edit, and export timetables.
## Features
### Database Management
- Creates and manages a timetable database in MySQL.
- Tables for subject, professor, and teaching hours with relational constraints.
### GUI Interface (Tkinter)
- Add, view, and delete subjects, professors, and teaching hours.
- Scrollable listboxes and styled Treeview for displaying records.
- Error handling with message boxes for invalid or duplicate entries.
### Timetable Generation
- Randomized allocation of professors to timeslots based on availability.
- Breaks automatically inserted (e.g., 12:00–13:00).
- Alternating row colors for readability.
### Data Export
- Export generated timetables to CSV.
- Open exported files directly from the GUI.
- Editing Tools
- Remove classes from the timetable.
- Modify subjects and teaching hours dynamically.
## Benefits
- Saves significant time in timetable creation.
- Ensures efficient resource allocation by enforcing constraints.
- Provides a practical, user-friendly solution for schools and institutions.
## Future Improvements
- Advanced scheduling algorithms (e.g., constraint satisfaction, optimization).
- Classroom and student group management.
- Web-based interface for broader accessibility.
- Integration with cloud databases.
