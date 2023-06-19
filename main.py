from tkinter import *
from tkinter import messagebox
from generate_password import generate_random_password
import json

FONT_NAME = "Courier"

entry_is_missed = False

# ---------------------------- GENERAL FUNCTIONS ------------------------------- #
def entry_missed():
    global entry_is_missed
    login_added.grid_forget()
    login_already_added.grid_forget()
    messagebox.showwarning("Missed value", "Please don't let any fields empty !!!")


def check_entries(*args):
    global entry_is_missed
    for entry in args:
        if len(entry.get()) == 0:
            entry_is_missed = True
            break

    if entry_is_missed:
        entry_missed()
# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_login():
    global entry_is_missed

    website = website_entry.get()
    email   = email_entry.get()
    password = password_entry.get()
    new_data = {
        website : {
            "Email"    : email,
            "PassWord" : password
        }
    }
    check_entries(website_entry, email_entry, password_entry)

    if not entry_is_missed:
        #let's ask the user to confirm the datails to save
        answer_is_ok = messagebox.askokcancel(title="Saving confirmation",
                               message=f"These are the detailed entered:\n \n "
                                       f"Website   : {website}\n Email       : {email}\n Password : {password}\n \n "
                                       f"Is it ok to save?\n")

        if answer_is_ok:
            #the saving block
            data = {}
            try:
                with open(file="login_file.json", mode="r") as file:
                    try:
                        data = json.load(file)
                    except json.decoder.JSONDecodeError:
                        pass

            except FileNotFoundError:
                pass

            # Update data and save it to the file
            if all(key in data and data[key]==new_data[key] for key in new_data):
                login_added.grid_forget()
                login_already_added.grid(column=1, row=5, columnspan=2)
            else :
                with open(file="login_file.json", mode="w") as file:
                    data.update(new_data)
                    json.dump(data, file, indent=4)
                    login_already_added.grid_forget()
                    login_added.grid(column=1, row=5, columnspan=2)

    else:
        entry_is_missed = False  # we need to reinitialise this variable after getting the pop-up


def on_entry_change(event, entry, label):
    if len(entry.get()) == 0:
        label.grid_forget()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    new_password = generate_random_password()
    password_entry.delete(0, END)
    password_entry.insert(0, new_password)


# ---------------------------- SEARCH LOGIN ------------------------------- #
def search_login():

    website = website_entry.get()
    try:
        with open(file="login_file.json", mode="r") as file:
            data = json.load(file)

    except FileNotFoundError:
        messagebox.showwarning(title="File missed", message="You didn't save any login details")

    except KeyError:
        messagebox.showwarning(title="Website missed",
                               message=f"You didn't save any login details relative to {website}")

    else:
        messagebox.showinfo(title="Your Login", message=f"Your login details are :\n"
                                                        f"Email : {data[website]['Email']}\n"
                                                        f"PassWord : {data[website]['PassWord']}")
# ---------------------------- GUI WINDOW ------------------------------- #
window = Tk()
window.title("Password Manager")
#window.config(bg=YELLOW)
window.config(padx=40, pady=40)

# CANVAS
canvas = Canvas(width=200, height=200)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

#Labels
website_label = Label(text="Website:", font=(FONT_NAME, 12))
website_label.grid(column=0, row=1)
email_label =  Label(text="Email/Username:", font=(FONT_NAME, 12))
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=(FONT_NAME, 12))
password_label.grid(column=0, row=3)

login_added         = Label(text="Login added successfully", font=(FONT_NAME, 12), fg="green")
login_already_added = Label(text="Login already added", font=(FONT_NAME, 12), fg="red")

#Entries
website_entry = Entry(width=70)
website_entry.focus()
website_entry.insert(0, "www.amazon.com")
website_entry.bind("<KeyRelease>", func = lambda event : on_entry_change(event, website_entry, login_added))
website_entry.bind("<KeyRelease>", func = lambda event : on_entry_change(event, website_entry, login_already_added))
website_entry.grid(column=1, row=1, columnspan=1, sticky="w")

email_entry = Entry(width=70)
#email_entry.insert(0, "YourEmailAddress@gmail.com")
email_entry.bind("<KeyRelease>", func = lambda event : on_entry_change(event, email_entry, login_added))
email_entry.bind("<KeyRelease>", func = lambda event : on_entry_change(event, email_entry, login_already_added))
email_entry.grid(column=1, row=2, columnspan=2, sticky="w")


password_entry = Entry(width=35)
#password_entry.insert(0, "password")
password_entry.bind("<KeyRelease>", func = lambda event : on_entry_change(event, password_entry, login_added))
password_entry.bind("<KeyRelease>", func = lambda event : on_entry_change(event, password_entry, login_already_added))
password_entry.grid(column=1, row=3, columnspan=1, sticky="w")

#Buttons
generate_password = Button(text="Generate", font=(FONT_NAME, 10), width=24, command=generate)
generate_password.grid(column=1, row=3, columnspan=1, sticky="e")

add = Button(text="Add", font=(FONT_NAME, 10), width=52, command= add_login)
add.grid(column=1, row=4, columnspan=2, sticky="w")

search = Button(text="Search", font=(FONT_NAME, 10), width=24, command= search_login)
search.grid(column=1, row=1, columnspan=1, sticky="e")





# ---------------------------- UI SETUP ------------------------------- #



window.mainloop()