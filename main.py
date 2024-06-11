from tkinter import *
from random import randint, choice, shuffle
from tkinter import messagebox
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def pass_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    a = [choice(letters) for _ in range(randint(8, 10))]
    b = [choice(symbols) for _ in range(randint(2, 4))]
    c = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = a+b+c
    shuffle(password_list)
    pass_word = "".join(password_list)
    pass_input.insert(0, f"{pass_word}")
    pyperclip.copy(pass_word)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    website_data = website_input.get().lower()
    email_data = user_input.get()
    pass_data = pass_input.get()
    new_data = {
        website_data: {
            "email": email_data,
            "password": pass_data
        }
    }

    if len(website_data) == 0 or len(pass_data) == 0 or len(email_data) == 0:
        messagebox.showinfo(title="Fields Empty", message="Enter the details")
    else:
        try:
            with open("data_file.json", "r") as file:
                data = json.load(file)  # Reading old file.

        except FileNotFoundError:
            with open("data_file.json", "w") as file:
                # Creating a json file if it not exists.
                json.dump(new_data, file, indent=4)  # Also added indent to make the data more readable.

        else:
            data.update(new_data)  # Updating old data with new data.

            with open("data_file.json", "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)  # Also added indent to make the data more readable.
        finally:
            website_input.delete(0, END)
            pass_input.delete(0, END)

# ---------------------------- SEARCH BUTTON ------------------------------- #


def search():
    website = website_input.get().lower()
    try:
        with open("data_file.json", "r") as file:
            dict_data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR", message="No Data File Found.")
    else:
        if website in dict_data:
            email = dict_data[website]["email"]
            password = dict_data[website]["password"]
            messagebox.showinfo(title=website_input.get().title(), message=f"Email : {email}\nPassword : {password}")
            pyperclip.copy(password)  # Password get auto copies for pasting.
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=10, pady=50)


canvas = Canvas(width=180, height=180, highlightthickness=0)
pass_img = PhotoImage(file="padlock.png")
canvas.create_image(110, 100, image=pass_img)
canvas.grid(column=1, row=0)

# Website Label and Entry
website_label = Label()
website_label.config(text="Website:")
website_label.grid(column=0, row=1)

website_input = Entry(width=42)
website_input.focus()
website_input.grid(column=1, row=1, columnspan=2)

# Email/Username Entry
email = Label()
email.config(text="Email/Username:")
email.grid(column=0, row=2)

user_input = Entry(width=42)
user_input.insert(0, "dummyemail@gmail.com") # Change your email here.
user_input.grid(column=1, row=2, columnspan=2)

# password
password = Label()
password.config(text="Password:")
password.grid(column=0, row=3)

pass_input = Entry(width=42)
pass_input.grid(column=1, row=3, columnspan=2)

# button
g_button = Button(text="Generate Password", width=14, command=pass_gen)
g_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save_pass)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=14, command=search)
search_button.grid(column=2, row=1)

window.mainloop()
