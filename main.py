from json import JSONDecodeError
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_text.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(4, 8)
    nr_symbols = random.randint(2, 5)
    nr_numbers = random.randint(2, 5)
    password_a = [random.choice(letters) for x in range(nr_letters)]
    password_b = [random.choice(symbols) for x in range(nr_symbols)]
    password_c = [random.choice(numbers) for x in range(nr_numbers)]
    password = password_a + password_b + password_c

    random.shuffle(password)
    password = "".join(password)
    password_text.insert(0, string=password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_name.get()
    email = email_name.get()
    password = password_text.get()
    new_data = {website: {
        "Email": email,
        "Password": password
    }
    }
    # ans = website_name.get() + " | " + email_name.get() + " | " + password_text.get() + "\n"
    if len(website) > 0 and len(email) > 0 and len(password) > 0:
        opt = messagebox.askokcancel(title=website,
                                     message=f"Email:{email}\nPassword:{password}\nAre you confirm?")
        if opt:
            # with open("data.txt", mode="a") as fl:
            #     fl.write(ans)
            try:
                with open("data.json", mode="r") as f:
                    data = json.load(f)
                    data.update(new_data)
            except FileNotFoundError:
                with open("data.json", mode="w") as f:
                    json.dump(new_data, f, indent=4)
            else:
                with open("data.json", mode="w") as f:
                    json.dump(data, f, indent=4)
            website_name.delete(0, END)
            email_name.delete(0, END)
            email_name.insert(END, string="romitdas2002@gmail.com")
            password_text.delete(0, END)
            messagebox.showinfo(title='Success', message="Your password have been saved Successfully")
    else:
        messagebox.showerror(title="Failed", message="Please input all the entries correctly!")


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def find_password():
    user_entry = website_name.get()
    if len(user_entry) > 0:
        e = "Email"
        p = "Password"
        try:
            with open("data.json", mode="r") as f:
                search_data = json.load(f)
                if user_entry in search_data:
                    messagebox.showinfo(title="Found", message=f"{user_entry}\nEmail: {search_data[user_entry][e]}\nPassword: {search_data[user_entry][p]}")
                else:
                    messagebox.showerror(title="Failed", message=f"{user_entry} is not found")

        except FileNotFoundError:
            messagebox.showerror(title="Failed", message="File is not created yet")
        except JSONDecodeError:
            messagebox.showerror(title="Error", message="Storage data is empty")
    else:
        messagebox.showerror(title="Error", message="Website name can't be empty")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username")
email_label.grid(row=2, column=0)

password_label = Label(text="Password")
password_label.grid(row=3, column=0)

# Entries
website_name = Entry(width=21)
website_name.grid(row=1, column=1, sticky="EW")

email_name = Entry(width=35)
email_name.insert(END, string="romitdas2002@gmail.com")
email_name.grid(row=2, column=1, columnspan=2, sticky="EW")

password_text = Entry(width=21)
password_text.grid(row=3, column=1, sticky="EW")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()
