import sys

sys.path.append('../hallucinator')

import hallucinator as hl
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


def add_source_window(position=END):
    def add_source():
        if not position == END:
            scheduled_listbox.delete(position)
        if type.get() == "Point":
            new_source = hl.PointSource(source=(float(x_pos.get()), float(y_pos.get())),
                                        frequency=float(frequency.get()),
                                        amplitude=float(amplitude.get()),
                                        phase_offset=float(phase_offset.get()),
                                        velocity=float(velocity.get()))
        else:
            pass
        sources.append(new_source)
        scheduled_listbox.insert(END, 'source')
        window.destroy()

    window = Toplevel(f)
    Label(window, text="source type").grid(row=0, column=0)
    Label(window, text="x position (m)").grid(row=1, column=0)
    Label(window, text="y position (m)").grid(row=1, column=2)
    Label(window, text="frequency (hertz)").grid(row=2, column=0)
    Label(window, text="amplitude").grid(row=2, column=2)
    Label(window, text="phase offset (0-2pi)").grid(row=3, column=0)
    Label(window, text="velocity (m/s)").grid(row=3, column=2)

    type = ttk.Combobox(window,
                        values=["Point",
                                "Plane"])
    type.grid(row=0, column=1)
    x_pos = Entry(window)
    y_pos = Entry(window)
    frequency = Entry(window)
    amplitude = Entry(window)
    phase_offset = Entry(window)
    velocity = Entry(window)

    velocity.insert(END, 300000000)
    phase_offset.insert(END, 0)
    frequency.insert(END, hl.RED_F)
    amplitude.insert(END, 1)

    x_pos.grid(row=1, column=1)
    y_pos.grid(row=1, column=3)
    frequency.grid(row=2, column=1)
    amplitude.grid(row=2, column=3)
    phase_offset.grid(row=3, column=1)
    velocity.grid(row=3, column=3)
    submit_b = Button(window, text="SUBMIT", command=add_source)
    submit_b.grid(row=4, column=2)
    cancel_b = Button(window, text="CANCEL", command=window.destroy)
    cancel_b.grid(row=4, column=1)


def edit_source():
    pass


def remove_source():
    pass


def add_region():
    pass


def remove_region():
    pass


def show_preview():
    pass


def render():
    pass


sources = []
regions = []

master = Tk()

f = Frame(master, height=500, width=1000)
f.pack_propagate(0)  # don't shrink
f.pack()

sched_new = Button(f, text="ADD SOURCE", command=add_source_window)
sched_new.grid(row=0, column=0, padx=5, pady=10)

edit = Button(f, text="EDIT", command=edit_source)
edit.grid(row=0, column=1, padx=5, pady=10)

edit = Button(f, text="REMOVE", command=remove_source)
edit.grid(row=0, column=2, padx=5, pady=10)

scheduled_listbox = Listbox(f, width=50, selectmode=SINGLE)
scheduled_listbox.grid(row=1, column=0, columnspan=5, padx=5, pady=10)

add_new_account = Button(f, text="ADD REGION", command=add_region)
add_new_account.grid(row=2, column=0, padx=5, pady=10)

logout = Button(f, text="REMOVE REGION", command=remove_region)
logout.grid(row=2, column=1, padx=5, pady=10)

agents_listbox = Listbox(f, width=50,
                         selectmode=SINGLE)
agents_listbox.grid(row=3, column=0, columnspan=5, padx=5, pady=10)

logout = Button(f, text="SHOW PREVIEW", command=show_preview)
logout.grid(row=4, column=0, padx=5, pady=10)
logout = Button(f, text="RENDER", command=render)
logout.grid(row=4, column=1, padx=5, pady=10)

mainloop()
