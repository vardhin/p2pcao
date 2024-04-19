# Add necessary imports at the top
from tkinter import INSERT, SEL_FIRST, SEL_LAST, Toplevel

# Inside the root.mainloop() block, after creating the main_body_text and text_input

# Button for reactions
reaction_button = Button(root, text="😄", command=lambda: add_reaction("😄"))
reaction_button.pack(side=LEFT)

# Button for emoji picker
emoji_button = Button(root, text="Emoji", command=show_emoji_picker)
emoji_button.pack(side=LEFT)

# Define functions for reactions and emoji picker

def add_reaction(reaction):
    """Add a reaction to the current message."""
    selected_text = main_body_text.get(SEL_FIRST, SEL_LAST)
    if selected_text:
        main_body_text.insert(INSERT, reaction)
    else:
        text_input.insert(END, reaction)

def show_emoji_picker():
    """Display an emoji picker window."""
    emoji_picker = Toplevel(root)
    emoji_picker.title("Emoji Picker")
    emoji_picker.geometry("400x200")  # Adjust size as needed

    # Add emoji buttons
    emojis = ["😀", "😂", "😊", "😍", "😎", "👍", "👎", "❤️", "🔥", "🎉"]
    for emoji in emojis:
        emoji_button = Button(emoji_picker, text=emoji, command=lambda e=emoji: add_emoji(e))
        emoji_button.pack(side=LEFT)

def add_emoji(emoji):
    """Add an emoji to the input field."""
    text_input.insert(END, emoji)
