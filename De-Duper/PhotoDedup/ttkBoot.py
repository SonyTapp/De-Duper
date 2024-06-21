import ttkbootstrap as ttk
from ttkbootstrap.constants import *

#--------------------------------
def mainPage():
    window = ttk.Window(themename="darkly")
    window.title('De-Duper')
    window.geometry('400x520')

    #--------------------------------

    buttonWidth = 20   # 20 Characters   font='Arial', 25, 'bold')

    headingS = ttk.Style()
    headingS.configure('headingS.TLabel', font=('Arial', 16, 'bold','underline'), foreground='skyblue')

    titleS = ttk.Style()
    titleS.configure('titleS.TLabel', font=('Arial', 25, 'bold', 'underline'), foreground='skyblue')

#--------------------------------

    title = ttk.Label(window, text= 'De-Duper', style='titleS.TLabel')
    title.pack(pady = 10)

    sep = ttk.Separator(window, orient='horizontal')
    sep.pack(fill='x', padx=10, pady=10)

    label = ttk.Label(window, text= 'Paths', style='headingS.TLabel')
    label.pack(pady = 10)

    b1 = ttk.Button(window, text="Choose Path", bootstyle=(),width=buttonWidth)
    b1.pack(pady=10)

    b2 = ttk.Button(window, text="Current Path Info", bootstyle=(),width=buttonWidth, command=folder_Info)
    b2.pack(pady=10)

    sep = ttk.Separator(window, orient='horizontal')
    sep.pack(fill='x', padx=10, pady=10)

    label2 = ttk.Label(window, text= 'Process Images',style='headingS.TLabel')
    label2.pack(pady = 10)

    b3 = ttk.Button(window, text="Compare With SSIM", bootstyle=(),width=buttonWidth)
    b3.pack(pady=10)

    b4 = ttk.Button(window, text="Comapre With Hash", bootstyle=(),width=buttonWidth)
    b4.pack(pady=10)

    b5 = ttk.Button(window, text="Comapre Colour", bootstyle=(),width=buttonWidth)
    b5.pack(pady=10)

    sep = ttk.Separator(window, orient='horizontal')
    sep.pack(fill='x', padx=10, pady=10)

    b6 = ttk.Button(window, text="EXIT", bootstyle=(WARNING),width=buttonWidth)
    b6.pack(pady=10)

    window.mainloop()

#--------------------------------    

def folder_Info():
    windowInfo = ttk.Window(themename="darkly")
    windowInfo.title('De-Duper')
    windowInfo.geometry('300x100')

    label3 = ttk.Label(windowInfo, text='There are X Images in your Directory', font=('Arial', 12))
    label3.pack(pady=20)

    windowInfo.mainloop()

#--------------------------------

if __name__ == "__main__":
    mainPage()
