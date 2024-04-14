import tkinter as tk
from tkinter import filedialog

from PIL import ImageTk, Image
from backend import Handler


class GUIMainWindow:
    # __init__ is done
    def __init__(self, worker: Handler):
        self.base_color = '#778899'
        self.worker = worker

        self.window = tk.Tk()
        self.task_name_var = tk.StringVar()
        self.task_sub_var = tk.StringVar()
        self.task_deadline_var = tk.StringVar()
        self.window_init_settings()

        self.window.mainloop()

    # method window_init_settings is done
    def window_init_settings(self):
        self.window.title("TodoList by Evil_Jekyll*")

        self.window.geometry(self.window_size())
        self.window.resizable(False, False)
        self.window.config(bg='black')

        self.main_container(self.window)
        self.tasks_container(self.bg_frame)
        self.bottom_container(self.bg_frame)
        self.enter_task_container(self.bottom_con)
        self.buttons_init(self.bottom_con)
        self.enter_fields(self.fields_frame)  # Перемістив виклик після оголошення методу

    # method window_size is done
    def window_size(self) -> str:
        window_width = 500
        window_height = 900
        screen_width = (self.window.winfo_screenwidth() - window_width) // 2
        screen_height = (self.window.winfo_screenheight() - window_height) // 2
        return f'{window_width}x{window_height}+{screen_width}+{screen_height}'

    # method main_container is done
    def main_container(self, places):
        self.bg_frame = tk.Frame(places, bg=self.base_color, bd=0)
        self.bg_frame.pack(fill=tk.BOTH, expand=True)
        self.header = tk.Label(self.bg_frame,
                               height=1,
                               bg=self.base_color,
                               text=f"Список завдань: ",
                               font=('Times New Roman', 20, 'bold', 'underline'),
                               justify='center',
                               anchor='n'
                               )
        self.header.pack(expand=False, fill=tk.X)

    # method tasks_container is done
    def tasks_container(self, places):
        self.tasks_frame = tk.Frame(places,
                                    bg=self.base_color,
                                    width=500,
                                    height=685,
                                    bd=4,
                                    relief='sunken')
        self.tasks_frame.pack(padx=2, pady=2, expand=False)

        canvas = tk.Canvas(self.tasks_frame,
                           bg=self.base_color,
                           width=465,
                           height=675,
                           relief='flat',
                           highlightbackground=self.base_color)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.tasks_frame,
                                 orient=tk.VERTICAL,
                                 command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        self.inner_canvas_frame = tk.Frame(canvas, bg=self.base_color)
        canvas.create_window((0, 0), window=self.inner_canvas_frame, anchor=tk.NW)

        def update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            if canvas.winfo_height() < self.inner_canvas_frame.winfo_reqheight():
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            else:
                scrollbar.pack_forget()

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        self.inner_canvas_frame.bind("<Configure>", update_scrollregion)

    # method bottom_container is done
    def bottom_container(self, places):
        self.bottom_con = tk.Frame(places, bg=self.base_color, relief='flat')
        self.bottom_con.pack(side='bottom', fill='x', )

    # method enter_task_container is done
    def enter_task_container(self, places):
        self.fields_frame = tk.Frame(places,
                                     width=440,
                                     height=200,
                                     bg=self.base_color,
                                     bd=5,
                                     relief='sunken')
        self.fields_frame.pack(side='left', padx=2, pady=2, fill='both', expand=False)

    # TODO:self.window.title must add only name not a path
    def buttons_init(self, places):
        self.load_logo = ImageTk.PhotoImage(Image.open("TodoGUI/Logo/Load.png").resize((40, 40)))
        self.save_logo = ImageTk.PhotoImage(Image.open("TodoGUI/Logo/Save.png").resize((40, 40)))
        self.add_logo = ImageTk.PhotoImage(Image.open("TodoGUI/Logo/Add.png").resize((40, 40)))

        def save_task_list():
            filename = filedialog.asksaveasfilename(title="Save File", defaultextension=".json")
            if filename:
                self.window.title(f"TodoList by Evil_Jekyll | {filename}")
                self.worker.save_todo(filename)

        def load_task_list():
            filename = filedialog.askopenfilename(title="Select File")
            if filename:
                self.window.title(f"TodoList by Evil_Jekyll | {filename}")
                self.task_init(self.worker.load_todo(filename))

        def add_task():
            self.worker.add_task(self.task_name_var.get(), self.task_sub_var.get(), self.task_deadline_var.get())
            self.task_name_var.set('')
            self.task_sub_var.set('')
            self.task_deadline_var.set('')
            self.task_init(self.worker.get_task_list())

        self.b_save = tk.Button(places,
                                image=str(self.save_logo),
                                highlightthickness=0,
                                bg=self.base_color,
                                activebackground=self.base_color,
                                bd=2,
                                command=save_task_list)
        self.b_load = tk.Button(places,
                                image=str(self.load_logo),
                                highlightthickness=0,
                                bg=self.base_color,
                                activebackground=self.base_color,
                                bd=2,
                                command=load_task_list)
        self.b_create_task = tk.Button(places,
                                       image=str(self.add_logo),
                                       highlightthickness=0,
                                       bg=self.base_color,
                                       activebackground=self.base_color,
                                       bd=2,
                                       command=add_task)

        self.b_create_task.pack(anchor='e', padx=5, pady=7)
        self.b_save.pack(anchor='e', padx=5, pady=5)
        self.b_load.pack(anchor='e', padx=5, pady=7)

    # TODO: edit button, d_logo and e_logo destroy buttons
    def task(self, places, task_data):
        undone_logo = ImageTk.PhotoImage(Image.open("TodoGUI/Logo/Done_False.png").resize((55, 55)))
        done_logo = ImageTk.PhotoImage(Image.open("TodoGUI/Logo/Done_True.png").resize((55, 55)))
        self.d_logo = ImageTk.PhotoImage(Image.open("TodoGUI/Logo/Delete2.png").resize((30, 30)))
        self.e_logo = ImageTk.PhotoImage(Image.open("TodoGUI/Logo/Edit2.png").resize((30, 30)))

        task_text = f"Завдання: {task_data['task_text']}\n"
        subs = ''
        for sub in task_data['sub_tasks']:
            if sub != '':
                subs += f'        - {sub}\n'
        if subs != '':
            task_text += f"Деталі: \n{subs}"
        if task_data['deadline']:
            task_text += f"Дедлайн: {task_data['deadline']}\n"
        task_text += f"Від: {task_data['task_create_time']}"

        def toggle_done():
            # Змінює стан завдання на виконане або невиконане
            if task_data['is_done']:
                done_button.config(bg='grey', image=str(undone_logo))
                task_data['is_done'] = False
            else:
                done_button.config(bg='lime green', image=str(done_logo))
                task_data['is_done'] = True

        def delete_task():
            self.worker.delete_task(task_data['id'])
            self.task_init(self.worker.get_task_list())

        def edit_task():
            new_name = self.task_name_var.get()
            new_sub = self.task_sub_var.get()
            new_deadline = self.task_deadline_var.get()
            task_id = task_data['id']
            self.worker.edit_task(task_id, new_name, new_sub, new_deadline)
            self.task_init(self.worker.get_task_list())

        ext_task_frame = tk.Frame(places,
                                  bg=self.base_color,
                                  bd=2,
                                  relief='groove',
                                  width=400)
        ext_task_frame.pack(fill=tk.X, padx=5, pady=5)

        task_label = tk.Label(ext_task_frame,
                              text=task_text,
                              anchor='w',
                              bg=self.base_color,
                              font=('Times New Roman', 12),
                              justify='left',
                              wraplength=320)

        done_button = tk.Button(ext_task_frame,
                                bg='lime green' if task_data['is_done'] else 'grey',
                                image=str(done_logo) if task_data['is_done'] else str(undone_logo),
                                command=toggle_done)
        delete_button = tk.Button(ext_task_frame,
                                  bg='grey',
                                  image=self.d_logo,
                                  command=delete_task)
        edit_button = tk.Button(ext_task_frame,
                                bg='grey',
                                image=self.e_logo,
                                command=edit_task)

        done_button.pack(anchor='n', side='left', padx=5, pady=5)
        task_label.pack(side='left', padx=5, pady=5, fill=tk.BOTH, expand=True)
        edit_button.pack(side='top', padx=5, pady=5)
        delete_button.pack(anchor='s', padx=5, pady=5)

    # method task_init is done
    def task_init(self, task_list):
        for widget in self.inner_canvas_frame.winfo_children():
            widget.destroy()
        for task in task_list:
            self.task(self.inner_canvas_frame, task)

    def enter_fields(self, places):
        task_name_label = tk.Label(places,
                                   text='Завдання: ',
                                   font=('times new roman', 16, 'bold'),
                                   bg=self.base_color)
        task_name_ef = tk.Entry(places,
                                bg='light gray',
                                width=29,
                                font=('times new roman', 14),
                                textvariable=self.task_name_var)

        subtask_label = tk.Label(places,
                                 text='Деталі: ',
                                 font=('times new roman', 16, 'bold'),
                                 bg=self.base_color)
        subtask_ef = tk.Entry(places,
                              bg='light gray',
                              width=29,
                              font=('times new roman', 14),
                              textvariable=self.task_sub_var)

        deadline_label = tk.Label(places,
                                  text='Виконати до: \n(dd.mm.yyyy)',
                                  font=('times new roman', 16, 'bold'),
                                  bg=self.base_color)
        deadline_ef = tk.Entry(places,
                               bg='light gray',
                               width=29,
                               font=('times new roman', 14),
                               textvariable=self.task_deadline_var)

        task_name_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        task_name_ef.grid(row=0, column=1, padx=5, pady=5)

        subtask_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)
        subtask_ef.grid(row=1, column=1, padx=5, pady=5)

        deadline_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)
        deadline_ef.grid(row=2, column=1, padx=5, pady=5)
