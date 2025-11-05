from tkinter import *




def back():
    window.destroy()
    import main

# Create the tkinter window
window = Tk()
window.title("HealUp")
window.geometry('400x650')
# Set the background color to black
window.configure(bg="#272727")

# Add a chat frame to display the conversation
chat_frame = Frame(window, bg="#272727")
chat_frame.place(x=0,y=10)

# Add a text box for user input
user_input = Entry(window, width=33, fg="black", bg="white",font=('Arial',12))
user_input.place(x=8, y=595)
print(user_input)

# Define a function to handle the user input
def send_message():
    message = user_input.get()
    if message != '':
        chat_text.config(state=NORMAL)
        chat_text.insert(END, "You: " + message + "\n")
        chat_text.config(state=DISABLED)
        user_input.delete(0, END)

# Add a button to send the user input
send_button = Button(window, width=8, text="Send", fg="white", bg="#3232FF", command=send_message)
send_button.place(x=325, y=595)

# Add a text widget to display the conversation
chat_text = Text(chat_frame, width=54, height=35, fg="white", bg="#333333", font=("Arial", 10), wrap=WORD)
chat_text.pack(padx=10, pady=0)

backbutton=Button(window,text="Back",width=5,fg="#000000",bg="#FFFFFF",command=back)
backbutton.place(x=5,y=1)

# Add some initial messages to the chat
chat_text.insert(END, "\nDoctorG : Enter the symptom you are experiencing \n")

# Run the tkinter event loop
window.mainloop()
