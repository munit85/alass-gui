from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Menu
import subprocess
from encoding_list import enc_list # TODO: tidy up that list
import terminals
import shutil
import sys
import webbrowser

filetypes = [('Subtitle file', '*.srt *.ass *.ssa *.idx *.sub')]
videotypes = [('Video file', '*.avi *.mkv *.mp4 *.m4a')]

def set_ref_file():
    path = filedialog.askopenfilename(filetypes=videotypes)
    if path != '':
        ref_file.set(path)

def set_inc_file():
    path = filedialog.askopenfilename(filetypes=filetypes)
    if path != '':
        inc_file.set(path)

def set_out_file():
    path = filedialog.asksaveasfilename(defaultextension='.srt')
    if path != '':
        out_file.set(path)

def choose_terminal():
    if sys.platform == 'win32':
        term_cb.config(state='disabled', values=terminals.term_win)
        term.set(terminals.term_win[0])
        return
    term_cb.config(values=terminals.term_linux)
    for t in terminals.term_linux:
        if shutil.which(t):
            term.set(t)
            break
    


def run():
    alasscmd = f'alass {ref_file.get()} {inc_file.get()} {out_file.get()} ' +\
    f'{"--disable-fps-guessing " if dfg.get() else ""}' +\
    f'{"--no-split " if no_split.get() else ""}' +\
    f'--encoding-inc {inc_enc.get()} ' +\
    f'--interval {interval.get()} ' +\
    f'--speed-optimization {optimize.get() } ' +\
    f'--split-penalty {split_penalty.get()} '

    if ref_file.get()[-4:] not in ('.srt', '.sub', '.ass', '.ssa', '.idx'):
        alasscmd += f'--audio-index {audio_index.get()} ' # we are using a video file as the reference
    else:
        alasscmd += f'--encoding-ref {ref_enc.get()} '
    
    print(alasscmd)


    # cmd.exe
    if term.get() == 'cmd.exe':
        p = subprocess.Popen([term.get(), '/K', f'.\\alass-cli {ref_file.get()} {inc_file.get()} {out_file.get()}'])
        return
    # gnome-terminal
    if term.get() == 'gnome-terminal':
        p = subprocess.Popen([term.get(), '--', 'sh', '-c', f'{alasscmd} ; echo Press \<Enter\> to close ; read'])
        return
    # urxvt, st, deepin-terminal, kitty, konsole, alacritty and xterm
    if term.get() in ('urxvt', 'st', 'xterm', 'io.elementary.terminal', 'deepin-terminal', 'kitty', 'konsole', 'alacritty'):
        p = subprocess.Popen([term.get(), '-e', 'sh', '-c', f'{alasscmd} ; echo Press \<Enter\> to close ; read'])
        return
    # terminator and terminolofy
    if term.get() in ('terminator', 'terminology'):
        p = subprocess.Popen([term.get(), '-e', f'sh -c {alasscmd} ; echo Press \<Enter\> to close ; read'])
        return
    # xfce4-terminal and lxterminal
    if term.get() in ('xfce4-terminal', 'lxterminal'):
        p = subprocess.Popen([term.get(), '-e', f'sh -c "{alasscmd} ; echo Press \<Enter\> to close ; read"'])
        return

def _quit():
    win.quit()
    win.destroy()
    exit()  

def _about():
    abt = Toplevel(win)
    abt.transient(win)
    abt.resizable(False, False)
    abt.title('About')
    lb = Label(abt, text='Automatic Language-Agnostic Subtitle Synchronization', padding=20)
    thes = Button(abt, text='How it works', command=lambda: webbrowser.open('https://github.com/kaegi/alass/raw/master/documentation/thesis.pdf'))
    alass = Button(abt, text='ALASS - Github page', command=lambda: webbrowser.open('https://github.com/kaegi/alass'))
    gui = Button(abt, text='ALASS GUI - Github page', command=lambda: webbrowser.open('https://github.com/0xclockwise/alass-gui/'))
    lb.grid(column=0, row=0, columnspan=3)
    thes.grid(column=0, row=1)
    alass.grid(column=1, row=1)
    gui.grid(column=2, row=1)


win = Tk()
win.title('ALASS - GUI')
win.resizable(False, False)

menu_bar = Menu(win)
win.config(menu=menu_bar)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Exit', command=_quit)
help_menu = Menu(menu_bar, tearoff=0)
help_menu.add_command(label='About', command=_about)
menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_cascade(label='Help', menu=help_menu)


ref_file = StringVar()
inc_file = StringVar()
out_file = StringVar()
ant = BooleanVar(value=False)
dfg = BooleanVar(value=False)
no_split = BooleanVar(value=False)
audio_index = IntVar(value=0)
ref_enc = StringVar(value='auto')
inc_enc = StringVar(value='auto')
term = StringVar()
interval = StringVar(value='1')
optimize = IntVar(value=1)
split_penalty = IntVar(value=7)


ref_lab = Label(win, text='Reference file: ')
ref_ent = Entry(win, textvariable=ref_file, width=40)
ref_btn = Button(win, text='...', command=set_ref_file, width=3)
inc_lab = Label(win, text='Incorrect subtitle: ')
inc_ent = Entry(win, textvariable=inc_file, width=40)
inc_btn = Button(win, text='...', command=set_inc_file, width=3)
out_lab = Label(win, text='Output file: ')
out_ent = Entry(win, textvariable=out_file, width=40)
out_btn = Button(win, text='...', command=set_out_file, width=3)

run_btn = Button(win, text='RUN!', command=run)

adv = LabelFrame(win, text='Advanced options')
ant_chk = Checkbutton(adv, text='Allow negative timestamps', variable=ant)
dfg_chk = Checkbutton(adv, text='Disable FPS guessing', variable=dfg)
no_split_chk = Checkbutton(adv, text='No split', variable=no_split)
ai_lab = Label(adv, text='Audio Index:')
audio_index_spn = Spinbox(adv, from_=0, to=20, increment=1, textvariable=audio_index)
ref_enc_lb = Label(adv, text='Reference encoding:')
ref_enc_cb = Combobox(adv, values=enc_list, state='readonly', textvariable=ref_enc)
inc_enc_lb = Label(adv, text='Incorrect encoding:')
inc_enc_cb = Combobox(adv, values=enc_list, state='readonly', textvariable=inc_enc)
term_lb = Label(adv, text='Terminal emulator:')
term_cb = Combobox(adv, state='readonly', textvariable=term)
choose_terminal()
interval_lb = Label(adv, text='Smallest recognized time interval (ms):')
interval_sb = Spinbox(adv, from_=1, to=2**32, increment=1, textvariable=interval)
optimize_cb = Checkbutton(adv, text='Speed optimization (less accurate)', variable=optimize)
split_penalty_lb = Label(adv, text='Split penalty:')
split_penalty_sb = Spinbox(adv, from_=0, to=1000, increment=1, textvariable=split_penalty)

ref_lab.grid(column=0, row=0, sticky='w')
ref_ent.grid(column=1, row=0)
ref_btn.grid(column=2, row=0)
inc_lab.grid(column=0, row=1, sticky='w')
inc_ent.grid(column=1, row=1)
inc_btn.grid(column=2, row=1)
out_lab.grid(column=0, row=2, sticky='w')
out_ent.grid(column=1, row=2)
out_btn.grid(column=2, row=2)

adv.grid(column=0, row=3, columnspan=3, padx=5)

ant_chk.grid(column=0, row=0, sticky='w')
dfg_chk.grid(column=0, row=1, sticky='w')
no_split_chk.grid(column=0, row=2, sticky='w')
ai_lab.grid(column=0, row=3, sticky='w')
audio_index_spn.grid(column=0, row=4, sticky='w')

ref_enc_lb.grid(column=0, row=5, sticky='w')
ref_enc_cb.grid(column=0, row=6, sticky='w')
inc_enc_lb.grid(column=0, row=7, sticky='w')
inc_enc_cb.grid(column=0, row=8, sticky='w')
term_lb.grid(column=0, row=9, sticky='w')
term_cb.grid(column=0, row=10, sticky='w')
interval_lb.grid(column=0, row=11, sticky='w')
interval_sb.grid(column=0, row=12, sticky='w')
optimize_cb.grid(column=0, row=14, sticky='w')
split_penalty_lb.grid(column=0, row=15, sticky='w')
split_penalty_sb.grid(column=0, row=16, sticky='w')

run_btn.grid(column=0, row=4, columnspan=3, sticky='nesw')

win.mainloop()
