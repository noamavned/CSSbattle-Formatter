from tkinter import *
import re
import datetime
from github import Github
from github import Auth
from tkinter import messagebox


def createTitle() -> str:
    """Create GitHub title

    Returns:
        str: title
    """
    t = datetime.datetime.now()
    d = t.strftime("%d")
    m = t.strftime("%m")
    if m[0] == "0":
        m = m[1]
    if d[0] == "0":
        d = d[1]
    title = f'{d}-{m}-{t.strftime("%Y")}.html'
    return title

def sort_file_paths_by_date(file_paths) -> list:
    def extract_date(file_path) -> list:
        date_part = file_path.split('.')[0]
        d = date_part.split('-')
        if len(d[0]) == 1:
            d[0] = "0"+d[0]
        if len(d[1]) == 1:
            d[1] = "0"+d[1]
        date_part = '-'.join(d)
        return datetime.datetime.strptime(date_part, "%d-%m-%Y")
    sorted_file_paths = sorted(file_paths, key=extract_date)
    return sorted_file_paths

def publish(t: str) -> None:
    title = createTitle()
    auth = Auth.Token("Your TOKEN")
    g = Github(auth=auth)
    repo = g.get_repo(824887772)
    l = 0
    conts = []
    contents = repo.get_contents("")
    while len(contents) > 1:
        l += 1
        file_content = contents.pop(0)
        conts.append(file_content)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
    contents = sort_file_paths_by_date(list(map(lambda x: x.path, conts)))
    if l >= 50:
        l -= 49
        for i in range(l):
            file_content = repo.get_contents(contents[i])
            repo.delete_file(contents[i], f"Delete {contents[i]}", file_content.sha)
    repo.create_file(title, f"Create {title}", t)
    messagebox.showinfo("Done", f"Deleted {l} files.\nAdded 1 file")

def copy(rt: Tk) -> None:
    """Copy content of element

    Args:
        rt (Tk): root of application
    """
    rt.clipboard_clear()
    rt.clipboard_append(txtarea2.get("1.0", END))
    rt.update()
    rt.after(100, rt.update())

def insertTxt(element: Text, index: int, text: str) -> None:
    """Insert into an element

    Args:
        element (Text): Text element to insert into
        index (int): index to insert to
        text (str): text to insert
    """
    element.delete('1.0', END)
    element.insert(index, text)

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
    lst = [m.end() for m in re.finditer('solid', txt)]
    for i in lst:
        txt = insertStr(txt, i, " ")

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

    insertTxt(element2, 1.0, formatted_txt)


# initialize root
root = Tk()
root.title("Html Formatter")

# input elements
lblinp = Label(root, text="input", background="grey", foreground="white")
lblinp.grid(columnspan=1, sticky="nsew")
txtarea = Text(root, height=20, width=70)
txtarea.grid(row=1, column=0)

# output elements
lblout = Label(root, text="output", background="grey", foreground="white")
lblout.grid(row=0, column=1, columnspan=3, sticky="nsew")
txtarea2 = Text(root, height=20, width=70)
txtarea2.grid(row=1, column=1)

# buttons
genbtn = Button(root, text="generate", background="grey", foreground="white", command=lambda: generate(txtarea, txtarea2))
genbtn.grid(row=2, column=0, columnspan=1, sticky="nsew")
copybtn = Button(root, text="copy", background="grey", foreground="white", command=lambda: copy(root))
copybtn.grid(row=2, column=1, columnspan=3, sticky="nsew")
publishbtn = Button(root, text="publish", background="grey", foreground="white", command=lambda: publish(txtarea2.get(1.0, END)))
publishbtn.grid(row=3, column=0, columnspan=3, sticky="nsew")

root.mainloop()
