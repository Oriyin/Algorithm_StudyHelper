# app.py

from flask import Flask, request, render_template, redirect, url_for
from algorithm import *

# Initialize the Flask application and specify the template folder
app = Flask(__name__, template_folder="../templates")

# Global variables for storing tasks and notes temporarily
tasks = []
notes = []
task_counter = 0  # A counter to uniquely identify each task

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for managing tasks
@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    global tasks, task_counter
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        due_date = request.form.get('due_date')
        priority = int(request.form.get('priority'))

        if task_name and task_description and due_date:
            task_counter += 1  # Increment task counter for each new task
            tasks.append({
                'id': task_counter,  # Assign unique ID to each task
                'name': task_name,
                'description': task_description,
                'dueDate': due_date,
                'priority': priority,
                'completed': False
            })

            # Sort tasks by due date immediately (excluding completed tasks) using Insertion Sort
            tasks = insertion_sort([task for task in tasks if not task['completed']], 'dueDate') + [task for task in tasks if task['completed']] 
            
            print("Updated tasks list:")
            print(tasks)

    todo_tasks = [task for task in tasks if not task['completed']]
    done_tasks = [task for task in tasks if task['completed']]

    return render_template('tasks.html', todo_tasks=todo_tasks, done_tasks=done_tasks, enumerate=enumerate)

# Route for managing notes
@app.route('/notes', methods=['GET', 'POST'])
def manage_notes():
    global notes
    if request.method == 'POST':
        note_title = request.form.get('note_title')
        note_content = request.form.get('note_content')

        if note_title and note_content:
            notes.append({
                'title': note_title,
                'content': note_content
            })
            print("Updated notes list:")
            print(notes)

    return render_template('notes.html', notes=notes, enumerate=enumerate)

# Route to edit a specific note by index
@app.route('/edit_note/<int:index>', methods=['POST'])
def edit_note(index):
    global notes
    new_title = request.form.get('edit_note_title')
    new_content = request.form.get('edit_note_content')

    if new_title and new_content:
        # Update the note with new values
        notes[index]['title'] = new_title
        notes[index]['content'] = new_content
        print("Updated notes list:")
        print(notes)

    return redirect(url_for('manage_notes'))

# Route to delete a specific note by index
@app.route('/delete_note/<int:index>', methods=['POST'])
def delete_note(index):
    global notes
    if index < len(notes):
        notes.pop(index)
        print("Updated notes list:")
        print(notes)
    return redirect(url_for('manage_notes'))

# Route to search through notes using a case-insensitive search with highlighted results
@app.route('/search_notes', methods=['POST'])
def search_notes():
    global notes
    search_pattern = request.form.get('search_pattern').lower()  # Make the search pattern lowercase
    search_results = []

    # Perform case-insensitive search on each note's title and content using naive string search
    for index, note in enumerate(notes):
        title = note['title']
        content = note['content']
        highlighted_content = content

        # Use naive string search to find matches (case-insensitive)
        matches = naive_string_search(content.lower(), search_pattern)  # Perform the search on lowercase text

        # If matches are found, highlight them in the content
        if matches:
            for match_index in matches:
                # Highlight the matched text using HTML <mark> tag
                match = content[match_index:match_index + len(search_pattern)]
                highlighted_content = highlighted_content.replace(match, f"<mark>{match}</mark>")
            search_results.append({
                'index': index,
                'title': title,
                'highlighted_content': highlighted_content
            })

    # If no matches are found, set a message to be displayed
    no_match_message = None
    if not search_results:
        no_match_message = "Don't have any file that match with finding word."

    return render_template('notes.html', notes=notes, search_results=search_results, no_match_message=no_match_message, search_pattern=search_pattern, enumerate=enumerate)

# Route to edit a specific task by index
@app.route('/edit_task/<int:index>', methods=['POST'])
def edit_task(index):
    global tasks
    new_name = request.form.get('edit_name')
    new_description = request.form.get('edit_description')
    new_due_date = request.form.get('edit_due_date')
    new_priority = int(request.form.get('edit_priority'))

    if new_name and new_description and new_due_date:
        # Update the task with new values
        tasks[index]['name'] = new_name
        tasks[index]['description'] = new_description
        tasks[index]['dueDate'] = new_due_date
        tasks[index]['priority'] = new_priority
        print("Updated tasks list:")
        print(tasks)

    # Re-sort tasks by due date immediately after editing using Insertion Sort
    tasks = insertion_sort([task for task in tasks if not task['completed']], 'dueDate') + [task for task in tasks if task['completed']]

    return redirect(url_for('manage_tasks'))

# Route to toggle a task's completion status using its unique ID
@app.route('/toggle_completed/<int:task_id>', methods=['POST'])
def toggle_completed(task_id):
    global tasks
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            print("Updated tasks list:")
            print(tasks)
            break
    # Re-sort the tasks to ensure they are in the correct order
    tasks = insertion_sort([task for task in tasks if not task['completed']], 'dueDate') + [task for task in tasks if task['completed']]
    return redirect(url_for('manage_tasks'))

# Route to delete a task by its unique ID
@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    print("Updated tasks list:")
    print(tasks)
    return redirect(url_for('manage_tasks'))

# Route to sort tasks by due date using Merge Sort
@app.route('/sort_by_due_date', methods=['POST'])
def sort_by_due_date():
    global tasks
    incomplete_tasks = [task for task in tasks if not task['completed']]
    # Use merge_sort to sort the incomplete tasks by 'dueDate'
    tasks = merge_sort(incomplete_tasks, 'dueDate') + [task for task in tasks if task['completed']]
    print("Updated tasks list:")
    print(tasks)
    return redirect(url_for('manage_tasks'))

# Route to sort tasks by priority
@app.route('/sort_by_priority', methods=['POST'])
def sort_by_priority():
    global tasks
    incomplete_tasks = [task for task in tasks if not task['completed']]
    tasks = counting_sort(incomplete_tasks, 'priority') + [task for task in tasks if task['completed']]
    print("Updated tasks list:")
    print(tasks)
    return redirect(url_for('manage_tasks'))

# Route to sort tasks by both due date and priority
@app.route('/sort_by_both', methods=['POST'])
def sort_by_both():
    global tasks
    incomplete_tasks = [task for task in tasks if not task['completed']]
    tasks = heap_sort(incomplete_tasks, 'dueDate', 'priority') + [task for task in tasks if task['completed']]
    print("Updated tasks list:")
    print(tasks)
    return redirect(url_for('manage_tasks'))

# Global variables for storing flashcards
flashcards = []

# Route for managing flashcards
@app.route('/flashcards', methods=['GET', 'POST'])
def manage_flashcards():
    global flashcards
    if request.method == 'POST':
        term = request.form.get('term')
        meaning = request.form.get('meaning')

        # Set incorrect_count to 0 by default when adding a new flashcard
        new_flashcard = {'term': term, 'meaning': meaning, 'incorrect_count': 0}

        # Use the uniqueness testing function to check for duplicates
        if uniqueness_testing(flashcards, new_flashcard):
            flashcards.append(new_flashcard)
            print("Flashcard added successfully!")
        else:
            print("Duplicate term found!")

    # Send 'enumerate' function to the template
    return render_template('flashcards.html', flashcards=flashcards, enumerate=enumerate)

# Route to randomize flashcards
@app.route('/randomize_flashcards', methods=['POST'])
def randomize_flashcards():
    global flashcards
    flashcards = random_flashcards(flashcards)
    return redirect(url_for('manage_flashcards'))

# Route to sort flashcards by incorrect count
@app.route('/sort_flashcards', methods=['POST'])
def sort_flashcards():
    global flashcards
    flashcards = merge_sort(flashcards, 'incorrect_count')
    return redirect(url_for('manage_flashcards'))

# Route to divide flashcards by incorrect count
@app.route('/divide_flashcards', methods=['POST'])
def divide_flashcards():
    global flashcards
    low_threshold = int(request.form.get('low_threshold', 3))  # Set threshold for incorrect_count
    flashcards = divide_and_conquer_flashcards(flashcards, low_threshold)
    return redirect(url_for('manage_flashcards'))

# Route to start flashcard review (displaying the first flashcard)
@app.route('/start_review')
def start_review():
    return redirect(url_for('review_flashcard', index=0))

# Route to review each flashcard
@app.route('/review_flashcard/<int:index>', methods=['GET', 'POST'])
def review_flashcard(index):
    global flashcards
    if request.method == 'POST':
        is_correct = request.form.get('is_correct') == 'true'
        if not is_correct:
            # Increase the incorrect count if the answer was incorrect
            flashcards[index]['incorrect_count'] += 1

        # Move to the next flashcard
        next_index = index + 1
        if next_index < len(flashcards):
            return redirect(url_for('review_flashcard', index=next_index))
        else:
            return redirect(url_for('review_completed'))

    # Display the current flashcard
    flashcard = flashcards[index]
    return render_template('review_flashcard.html', flashcard=flashcard, index=index)

# Route for review completion
@app.route('/review_completed')
def review_completed():
    return render_template('review_completed.html')

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)