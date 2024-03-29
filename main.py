from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 0.5
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None

def check_state(todo_item):
    if checkbox_vars[todo_item].get() == 1:
        print(f"Checkbox for {todo_item} is checked")
        todo_list.remove(todo_item)
        with open ("Day_28/todos.txt", 'w') as f:
            for todo in todo_list:
                f.write(f"{todo}\n")
        update_todo_list()
    else:
        print(f"Checkbox for {todo_item} is unchecked")

def add_todo():
    todo_item = todo.get()
    with open ('Day_28/todos.txt', 'a') as f:
        f.write(f'{todo_item}\n')
    todo.delete(0, END)
    update_todo_list()

def update_todo_list():
    # Clear existing checkboxes
    for widget in window.winfo_children():
        if isinstance(widget, Checkbutton):
            widget.destroy()

    placement = 8
    with open('Day_28/todos.txt') as f:
        todo_list = f.read().splitlines()
    for item in todo_list:
        checkbox_vars[item] = IntVar()  # Create a variable for each checkbox
        Checkbutton(window, text=item, variable=checkbox_vars[item],
                    command=lambda item=item: check_state(item)).grid(row=placement, column=1, sticky="w", pady=10)
        placement += 2

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    canvas.after_cancel(timer)
    canvas.itemconfig(time_label, text = "00:00")
    timer_label.config(text = "Timer")
    check_marks.config(text = "")
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if (reps % 8 == 0):
        countdown(long_break_sec)
        timer_label.config(text = "Break", fg = RED)
    elif (reps % 2 == 0):
        countdown(short_break_sec)
        timer_label.config(text = "Break", fg = PINK)
    else:
        countdown(work_sec)
        timer_label.config(text = "Work", fg = GREEN)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def countdown(count):
    count_min = count // 60
    count_sec = count % 60
    global reps
    global timer

    if count_sec < 10:
        canvas.itemconfig(time_label, text = f"{int(count_min)}:0{int(count_sec)}")
    else:
        canvas.itemconfig(time_label, text = f"{int(count_min)}:{int(count_sec)}")
    if count > 0:
        timer = canvas.after(1000, countdown, count - 1)
    else:
        start_timer()
        if (reps > 0 and reps % 2 == 0):
            check_marks.config(text = "✔" * (reps // 2))

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx = 100, pady = 50)

checkbox_vars = {} 
with open('Day_28/todos.txt') as f:
    todo_list = f.read().splitlines()

timer_label = Label(text = "Timer",  fg = GREEN, font = (FONT_NAME, 35, "bold"))
timer_label.grid(column = 1, row = 0)

tomato_img = PhotoImage(file="Day_28/tomato.png")
canvas = Canvas(width = 200, height = 224,  highlightthickness = 0)
canvas.create_image(100, 112, image = tomato_img)

time_label = canvas.create_text(100, 130, text = "00:00", fill = "white", font = (FONT_NAME, 24, "bold"))
canvas.grid(column = 1, row = 2)

start_button = Button(text = "Start", borderwidth=0, highlightthickness=0,  font=(FONT_NAME, 15, "bold"), command = start_timer)
start_button.grid(column = 0, row = 3)

reset_button = Button(text = "Reset", borderwidth=0, highlightthickness=0,  font=(FONT_NAME, 15, "bold"), command = reset_timer)
reset_button.grid(column = 2, row = 3)

check_marks = Label( fg = GREEN, font = (FONT_NAME, 35, "bold"))
check_marks.grid(column = 1, row = 4)

todo_label = Label(text="To-Do List:",  fg="black", font = (FONT_NAME, 18, "bold"))
todo_label.grid(column=1, row=5)

todo = Entry(width=30)
todo.focus()
todo.grid(column=1, row=6)

todo_button = Button(text = "Add", borderwidth=0, highlightthickness=0,  font=(FONT_NAME, 15, "bold"), command = add_todo)
todo_button.grid(column=2, row=6)

update_todo_list()

window.mainloop()