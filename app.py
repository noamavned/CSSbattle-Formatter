from tkinter import *


def copy(rt: Tk) -> None:
    """Copy content of element

    Args:
        rt (Tk): root of application
    """
    rt.clipboard_clear()
    rt.clipboard_append(txtarea2.get("1.0", END))
    rt.update()
    rt.after(100, rt.update())

def insertDisabled(element: Text, index: int, text: str) -> None:
    """Insert into a disabled element

    Args:
        element (Text): Text element to insert into
        index (int): index to insert to
        text (str): text to insert
    """
    element.config(state=NORMAL)
    element.insert(index, text)
    element.config(state=DISABLED)

def insertStr(s: str, index: int, t: str) -> str:
    """Insert string into string in index

    Args:
        s (str): original string
        index (int): index
        t (str): text to insert

    Returns:
        str: new string
    """
    return s[:index] + t + s[index:]

def generate(element: Text, element2: Text) -> None:
    """Format  text for HTML/CSS

    Args:
        element (Text): input element
        element2 (Text): output element
    """
    txt = element.get("1.0", "end-1c")
    styleloc = txt.index("<style>")
    txt = insertStr(txt, styleloc, '\n')
    txt = insertStr(txt, styleloc + 8, '\n\t')

    formatted_txt = ""
    for char in txt:
        if char == '{':
            formatted_txt += ' {\n\t\t'
        elif char == ':':
            formatted_txt += ': '
        elif char == ';':
            formatted_txt += ';\n\t\t'
        elif char == '}':
            formatted_txt += '\n\t}\n\t'
        elif char == ',':
            formatted_txt += ', '
        else:
            formatted_txt += char

    insertDisabled(element2, 1.0, formatted_txt)


# initialize root
root = Tk()
root.title("Html Formatter")

# input elements
lblinp = Label(root, text="input")
lblinp.grid()
txtarea = Text(root, height=20, width=70)
txtarea.grid(row=1, column=0)

# output elements
lblout = Label(root, text="output")
lblout.grid(row=0, column=1)
txtarea2 = Text(root, height=20, width=70, state=DISABLED)
txtarea2.grid(row=1, column=1)

# buttons
copybtn = Button(root, text="generate", command=lambda: generate(txtarea, txtarea2))
copybtn.grid(row=2, column=0)
copybtn = Button(root, text="copy", command=lambda: copy(root))
copybtn.grid(row=2, column=1)

root.mainloop()
