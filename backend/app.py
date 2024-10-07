from flask import Flask, request, render_template, redirect, url_for
from algorithm import merge_sort, counting_sort, heap_sort, naive_string_search, insertion_sort

# Initialize the Flask application and specify the template folder
app = Flask(__name__, template_folder="../templates")

# Global variables for storing tasks and notes temporarily
tasks = []
notes = []

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for managing tasks
@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    global tasks
    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_description = request.form.get('task_description')
        due_date = request.form.get('due_date')
        priority = int(request.form.get('priority'))

        if task_name and task_description and due_date:
            tasks.append({
                'name': task_name,
                'description': task_description,
                'dueDate': due_date,
                'priority': priority,
                'completed': False
            })

            # Sort tasks by due date immediately (excluding completed tasks)
            tasks = insertion_sort([task for task in tasks if not task['completed']], 'dueDate') + [task for task in tasks if task['completed']]

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

    return render_template('notes.html', notes=notes, enumerate=enumerate)

# Route to search through notes using a naive string search algorithm
@app.route('/search_notes', methods=['POST'])
def search_notes():
    global notes
    search_pattern = request.form.get('search_pattern')
    search_results = []

    # Perform naive string search on each note's title and content
    for note in notes:
        indices_title = naive_string_search(note['title'], search_pattern)
        indices_content = naive_string_search(note['content'], search_pattern)

        # If a match is found, add it to the search results
        if indices_title or indices_content:
            search_results.append({
                'note': note,
                'indices_title': indices_title,
                'indices_content': indices_content
            })

    return render_template('notes.html', notes=notes, search_results=search_results, search_pattern=search_pattern, enumerate=enumerate)

# Other task routes as provided before...
@app.route('/edit_task/<int:index>', methods=['POST'])
def edit_task(index):
    global tasks
    new_name = request.form.get('edit_name')
    new_description = request.form.get('edit_description')

    if new_name and new_description:
        tasks[index]['name'] = new_name
        tasks[index]['description'] = new_description

    # Re-sort tasks by due date after editing
    tasks = insertion_sort([task for task in tasks if not task['completed']], 'dueDate') + [task for task in tasks if task['completed']]

    return redirect(url_for('manage_tasks'))

@app.route('/toggle_completed/<int:index>', methods=['POST'])
def toggle_completed(index):
    global tasks
    tasks[index]['completed'] = not tasks[index]['completed']
    return redirect(url_for('manage_tasks'))

@app.route('/delete_task/<int:index>', methods=['POST'])
def delete_task(index):
    global tasks
    del tasks[index]
    return redirect(url_for('manage_tasks'))

@app.route('/sort_by_due_date', methods=['POST'])
def sort_by_due_date():
    global tasks
    incomplete_tasks = [task for task in tasks if not task['completed']]
    tasks = insertion_sort(incomplete_tasks, 'dueDate') + [task for task in tasks if task['completed']]
    return redirect(url_for('manage_tasks'))

@app.route('/sort_by_priority', methods=['POST'])
def sort_by_priority():
    global tasks
    incomplete_tasks = [task for task in tasks if not task['completed']]
    tasks = counting_sort(incomplete_tasks, 'priority') + [task for task in tasks if task['completed']]
    return redirect(url_for('manage_tasks'))

@app.route('/sort_by_both', methods=['POST'])
def sort_by_both():
    global tasks
    incomplete_tasks = [task for task in tasks if not task['completed']]
    tasks = heap_sort(incomplete_tasks, 'dueDate', 'priority') + [task for task in tasks if task['completed']]
    return redirect(url_for('manage_tasks'))

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)
