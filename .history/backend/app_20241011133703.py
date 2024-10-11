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

# Global variable to store flashcards
flashcards = []

@app.route('/flashcards', methods=['GET', 'POST'])
def manage_flashcards():
    global flashcards
    if request.method == 'POST':
        term = request.form.get('term')
        meaning = request.form.get('meaning')
        difficulty = request.form.get('difficulty')  # Capture the difficulty level

        # Create a new flashcard with 'incorrect_count' initialized to 0 and difficulty level
        new_flashcard = {'term': term, 'meaning': meaning, 'difficulty': difficulty, 'incorrect_count': 0}

        # Use the uniqueness testing function to avoid duplicates
        if uniqueness_testing(flashcards, new_flashcard):
            print("Flashcard added successfully!")
        else:
            print("Duplicate term found! Flashcard not added.")

    # Render the flashcards page with the flashcards list and total number
    return render_template('flashcards.html', flashcards=flashcards, enumerate=enumerate)


# Route to start flashcard practice (randomizes flashcards before starting)
@app.route('/start_practice', methods=['GET'])
def start_practice():
    global flashcards
    # Randomize flashcards before starting practice
    flashcards = random_flashcards(flashcards)
    return redirect(url_for('practice_flashcard', index=0))

@app.route('/practice_flashcard/<int:index>', methods=['GET', 'POST'])
def practice_flashcard(index):
    global flashcards
    if index >= len(flashcards):
        # If the index is out of range, redirect to the practice completion page
        return redirect(url_for('practice_completed'))

    if request.method == 'POST':
        # Check if the answer was correct or not
        is_correct = request.form.get('is_correct') == 'true'
        if not is_correct:
            flashcards[index]['incorrect_count'] += 1

        # Move to the next flashcard
        next_index = index + 1
        if next_index < len(flashcards):
            return redirect(url_for('practice_flashcard', index=next_index))
        else:
            return redirect(url_for('practice_completed'))

    # Render the current flashcard for practice
    flashcard = flashcards[index]
    return render_template('practice_flashcard.html', flashcard=flashcard, index=index)


@app.route('/practice_completed')
def practice_completed():
    global flashcards

    # Group flashcards based on incorrect_count
    low_threshold = 1
    grouped_flashcards = divide_and_conquer_flashcards(flashcards, low_threshold)

    # Separate correct and incorrect flashcards for the result page
    correct_flashcards = [fc for fc in grouped_flashcards if fc['incorrect_count'] == 0]
    incorrect_flashcards = [fc for fc in grouped_flashcards if fc['incorrect_count'] > 0]

    # Show the result in terms of high-priority (incorrect more often) and low-priority flashcards
    return render_template('practice_completed.html', correct_flashcards=correct_flashcards, incorrect_flashcards=incorrect_flashcards)

@app.route('/practice_again', methods=['GET'])
def practice_again():
    global flashcards

    # ตรวจสอบพารามิเตอร์ 'sort_mode' จาก URL
    sort_mode = request.args.get('sort_mode')

    if sort_mode == 'easy_to_hard':
        flashcards = counting_sortflash(flashcards, 'difficulty')  # เรียงจากง่ายไปยาก
        print("Flashcards sorted from Easy to Hard")
    else:
        flashcards = random_flashcards(flashcards)  # แบบสุ่มสำหรับ practice ปกติ
        print("Flashcards randomized")

    return redirect(url_for('practice_flashcard', index=0))

@app.route('/start_practice_by_difficulty', methods=['GET'])
def start_practice_by_difficulty():
    global flashcards

    if len(flashcards) == 0:
        # Redirect to the flashcards management page if there are no flashcards
        return redirect(url_for('manage_flashcards'))

    # Sort flashcards by difficulty in the order of Easy -> Medium -> Hard
    flashcards = counting_sortflash(flashcards, 'difficulty')

    return redirect(url_for('practice_flashcard', index=0))

@app.route('/start_focused_practice', methods=['GET'])
def start_focused_practice():
    global flashcards

    # Set a low_threshold for incorrect answers to define "high-priority"
    low_threshold = 2  # For example, focus on flashcards with incorrect_count > 2

    # Group flashcards based on how often the user gets them wrong
    flashcards = divide_and_conquer_flashcards(flashcards, low_threshold)

    return redirect(url_for('practice_flashcard', index=0))

@app.route('/practice_focused_flashcards/<int:index>', methods=['GET', 'POST'])
def practice_focused_flashcards(index):
    global flashcards_to_practice

    if index >= len(flashcards_to_practice):
        # หากฝึกฝนครบหมดแล้วให้กลับไปที่หน้าผลลัพธ์
        return redirect(url_for('focused_practice_completed'))

    if request.method == 'POST':
        # เช็คว่าผู้ใช้ตอบถูกหรือไม่
        is_correct = request.form.get('is_correct') == 'true'
        if is_correct:
            # ถ้าตอบถูก ตัด flashcard นั้นออกจากรายการ
            flashcards_to_practice.pop(index)
        else:
            # ถ้าตอบผิด เพิ่ม incorrect_count
            flashcards_to_practice[index]['incorrect_count'] += 1

        # ย้ายไปยัง flashcard ถัดไป
        next_index = index if is_correct else index + 1
        if next_index < len(flashcards_to_practice):
            return redirect(url_for('practice_focused_flashcards', index=next_index))
        else:
            return redirect(url_for('focused_practice_completed'))

    # แสดง flashcard ที่กำลังทบทวน
    flashcard = flashcards_to_practice[index]
    return render_template('practice_focused_flashcards.html', flashcard=flashcard, index=index)

# Route for displaying the result after focused practice
@app.route('/focused_practice_completed')
def focused_practice_completed():
    global flashcards_to_practice

    # แสดงผลลัพธ์ว่าผู้ใช้ได้ทบทวน flashcards ทั้งหมดครบแล้ว
    return render_template('focused_practice_completed.html', flashcards_left=len(flashcards_to_practice))

# Run the Flask server
if __name__ == "__main__":
    app.run(debug=True)
    print(tasks)
    print(notes)