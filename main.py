import tkinter as tk
import random
from pathlib import Path

countries=[]
score=0
question_queue=[]
question_index=0
total_questions=10
current_question=None
mode_choice='mix up'
current_mode='mix up'
image_cache={}


def find_base_folder():
    try:
        first_try=Path(__file__).resolve().parent
    except Exception:
        first_try=Path.cwd()
    spots=[first_try,Path.cwd()]
    good=None
    i=0
    while i<len(spots):
        place=spots[i]
        data_path=place/'data'
        fact_path=place/'facts'
        if data_path.exists() and fact_path.exists():
            good=place
            break
        i+=1
    if not good:
        good=spots[0]
    return good


# pick a folder that actually has the data/facts
resource_base=find_base_folder()
print('looking for data in '+str(resource_base))

FACT_FILES={
'United States':'facts/US.txt',
'Japan':'facts/JP.txt',
'United Kingdom':'facts/GB.txt',
'Mexico':'facts/MX.txt',
'Canada':'facts/CA.txt',
'India':'facts/IN.txt',
'France':'facts/FR.txt',
'Turkey':'facts/TR.txt',
'China':'facts/CN.txt',
'Saudi Arabia':'facts/SA.txt',
'Argentina':'facts/AR.txt',
'Belgium':'facts/BE.txt',
'South Africa':'facts/ZA.txt',
'Cuba':'facts/CU.txt',
'New Zealand':'facts/NZ.txt',
'Niger':'facts/NE.txt',
'Greece':'facts/GR.txt',
'Iraq':'',
'Bangladesh':'facts/BD.txt',
'Hong Kong':'facts/HK.txt',
'Angola':'facts/AO.txt',
'Bahamas':'facts/BS.txt',
'Montenegro':'facts/ME.txt',
'United Arab Emirates':'facts/AE.txt',
'Jordan':'facts/JO.txt',
'Nicaragua':'facts/NI.txt'
}

FLAG_IMAGES={
'United States':'data/easy/US.png',
'Japan':'data/easy/JP.png',
'United Kingdom':'data/easy/GB.png',
'Mexico':'data/easy/MX.png',
'Canada':'data/easy/CA.png',
'India':'data/easy/IN.png',
'France':'data/easy/FR.png',
'Turkey':'data/standard/TR.png',
'China':'data/standard/CN.png',
'Saudi Arabia':'data/standard/SA.png',
'Argentina':'data/standard/AR.png',
'Belgium':'data/standard/BE.png',
'South Africa':'data/standard/ZA.png',
'Cuba':'data/advanced/CU.png',
'New Zealand':'data/advanced/NZ.png',
'Niger':'data/advanced/NE.png',
'Greece':'data/advanced/GR.png',
'Iraq':'data/advanced/IQ.png',
'Bangladesh':'data/advanced/BD.png',
'Hong Kong':'data/advanced/HK.png',
'Angola':'data/expert/AO.png',
'Bahamas':'data/expert/BS.png',
'Montenegro':'data/expert/ME.png',
'United Arab Emirates':'data/expert/AE.png',
'Jordan':'data/expert/JO.png',
'Nicaragua':'data/expert/NI.png'
}

EASY=['United States','Japan','United Kingdom','Mexico','Canada','India','France']
STANDARD=['Turkey','China','Saudi Arabia','Argentina','Belgium','South Africa']
ADVANCED=['Cuba','New Zealand','Niger','Greece','Iraq','Bangladesh','Hong Kong']
EXPERT=['Angola','Bahamas','Montenegro','United Arab Emirates','Jordan','Nicaragua']
MODE_GROUPS={
'mix up':EASY+STANDARD+ADVANCED+EXPERT,
'easy':EASY,
'standard':STANDARD,
'advanced':ADVANCED,
'expert':EXPERT
}

def read_fact(path):
    if not path:
        return ''
    file_path=resource_base/path
    if not file_path.exists():
        print('missing fact file at '+str(file_path))
        return ''
    try:
        with file_path.open('r') as file:
            data=file.read().strip()
    except Exception:
        data=''
    return data


def load_data(choice):
    global countries
    if choice in MODE_GROUPS:
        base=MODE_GROUPS[choice]
    else:
        base=MODE_GROUPS['mix up']
    countries=[]
    i=0
    while i<len(base):
        name=base[i]
        fact_path=FACT_FILES.get(name,'')
        if name=='Iraq':
            fact_text=''
        else:
            if fact_path:
                fact_text=read_fact(fact_path)
            else:
                fact_text=''
        countries.append({'country':name,'fact':fact_text})
        i+=1



def show_screen(screen):
    screen.tkraise()


def update_score():
    global score
    score+=1
    score_label.config(text='Score: '+str(score))




def handle_answer(answer):
    global current_question,question_index
    if not current_question:
        return
    text='Correct answer: '+current_question['country']
    fact=current_question['fact']
    if answer:
        guess=str(answer).strip().lower()
    else:
        guess=''
    actual=current_question['country'].lower()
    if guess and guess==actual:
        update_score()
        message='Nice job!\n\n'+text+'\n\n'+fact
    else:
        message='Not quite.\n\n'+text+'\n\n'+fact
    question_index+=1
    show_fact_screen(message)
    current_question=None


def go_back_to_quiz():
    show_screen(quiz_screen)
    ask_question()


def finish_game():
    if question_queue:
        total=len(question_queue)
    else:
        total=total_questions
    if total<=0:
        total=total_questions
    result_label.config(text='Final Score: '+str(score)+'/'+str(total))
    show_screen(result_screen)



def start_game():
    global score,question_index,current_question,question_queue,mode_choice,current_mode,image_cache
    if mode_choice in MODE_GROUPS:
        choice=mode_choice
    else:
        choice='mix up'
    current_mode=choice
    load_data(choice)
    score=0
    question_index=0
    current_question=None
    image_cache={}
    sample=min(total_questions,len(countries))
    if sample>0:
        question_queue=random.sample(countries,sample)
    else:
        question_queue=[]
    score_label.config(text='Score: 0')
    question_label.config(text='Question 0')
    show_screen(quiz_screen)
    ask_question()


def show_flag_picture(name):
    path=FLAG_IMAGES.get(name,'')
    if path=='':
        picture_label.config(image='',text='[flag image here]')
        picture_label.image=None
        return
    image_path=resource_base/path
    if not image_path.exists():
        print('missing flag file at '+str(image_path))
        picture_label.config(image='',text='[flag image missing]')
        picture_label.image=None
        return
    if name not in image_cache:
        try:
            image_cache[name]=tk.PhotoImage(file=str(image_path),master=window)
        except tk.TclError as error:
            print('Error loading flag for '+str(name)+': '+str(error))
            picture_label.config(image='',text='[flag image unavailable]')
            picture_label.image=None
            return
    photo=image_cache[name]
    picture_label.config(image=photo,text='')
    picture_label.image=photo



def show_fact_screen(text):
    fact_message.config(text=text)
    show_screen(fact_screen)


def ask_question():
    global current_question,question_index
    if question_queue:
        total=len(question_queue)
    else:
        total=total_questions
    if question_index>=total:
        finish_game()
        return
    if not question_queue:
        finish_game()
        return
    current_question=question_queue[question_index]
    question_label.config(text='Question '+str(question_index+1)+'/'+str(total))
    if current_mode in ('advanced','expert'):
        i=0
        while i<len(option_buttons):
            option_buttons[i].pack_forget()
            i+=1
        answer_entry.delete(0,tk.END)
        answer_entry.pack(pady=5)
        submit_button.pack(pady=5)
    else:
        answer_entry.pack_forget()
        submit_button.pack_forget()
        i=0
        while i<len(option_buttons):
            option_buttons[i].pack(pady=5)
            i+=1
        choices=[current_question['country']]
        remaining=[]
        i=0
        while i<len(countries):
            entry=countries[i]
            if entry['country']!=current_question['country']:
                remaining.append(entry['country'])
            i+=1
        random.shuffle(remaining)
        while len(choices)<4 and remaining:
            choices.append(remaining.pop())
        while len(choices)<4:
            choices.append('')
        random.shuffle(choices)
        i=0
        while i<len(option_buttons) and i<len(choices):
            btn=option_buttons[i]
            name=choices[i]
            if name=='':
                btn.config(text='',state='disabled',command=lambda: None)
            else:
                btn.config(text=name,state='normal',command=lambda value=name:handle_answer(value))
            i+=1
    show_flag_picture(current_question['country'])




def go_home():
    show_screen(start_screen)

def submit_typing():
    text=answer_entry.get().strip()
    answer_entry.delete(0,tk.END)
    handle_answer(text)


def build_window():
    global window,start_screen,quiz_screen,fact_screen,result_screen
    global question_label,picture_label,option_buttons,score_label,fact_message,result_label
    global answer_entry,submit_button
    window=tk.Tk()
    window.title('Flag-Find Frenzy')
    window.geometry('1000x800')

    start_screen=tk.Frame(window)
    quiz_screen=tk.Frame(window)
    fact_screen=tk.Frame(window)
    result_screen=tk.Frame(window)
    window.rowconfigure(0,weight=1)
    window.columnconfigure(0,weight=1)
    frames=(start_screen,quiz_screen,fact_screen,result_screen)
    i=0
    while i<len(frames):
        frames[i].grid(row=0,column=0,sticky='nsew')
        i+=1

    title=tk.Label(start_screen,text='Flag-Find Frenzy',font=('Arial',24))
    title.pack(pady=20)
    names=tk.Label(start_screen,text='Group: Hudson McEntire, Yuval Dinodia, Aarush Yelimeli')
    names.pack(pady=10)

    mode_label=tk.Label(start_screen,text='Type Mode (mix up, easy, standard, advanced, expert)')
    mode_label.pack()
    mode_entry=tk.Entry(start_screen,width=20)
    mode_entry.insert(0,'mix up')
    mode_entry.pack(pady=6)

    picture_label=tk.Label(quiz_screen,text='[flag image here]')
    picture_label.pack(pady=12)
    question_label=tk.Label(quiz_screen,text='Question 0',font=('Arial',16))
    question_label.pack(pady=10)



    button_frame=tk.Frame(quiz_screen)
    button_frame.pack(pady=15)
    option_buttons=[]
    i=0
    while i<4:
        btn=tk.Button(button_frame,text='',width=30)
        btn.pack(pady=5)
        option_buttons.append(btn)
        i+=1
    answer_entry=tk.Entry(quiz_screen,width=30)
    submit_button=tk.Button(quiz_screen,text='Submit',command=submit_typing)

    score_label=tk.Label(quiz_screen,text='Score: 0',font=('Arial',14))
    score_label.pack(pady=8)

    fact_title=tk.Label(fact_screen,text='Fun Fact',font=('Arial',18))
    fact_title.pack(pady=10)
    fact_message=tk.Label(fact_screen,text='',wraplength=500,justify='left')
    fact_message.pack(padx=20,pady=15)
    tk.Button(fact_screen,text='Next Question',command=go_back_to_quiz).pack(pady=8)

    result_label=tk.Label(result_screen,text='',font=('Arial',18))
    result_label.pack(pady=15)
    tk.Button(result_screen,text='Play Again',command=go_home).pack(pady=8)

    def set_mode_and_start():
        global mode_choice
        entry_text=mode_entry.get().strip().lower()
        if entry_text in MODE_GROUPS:
            mode_choice=entry_text
        else:
            mode_choice='mix up'
        start_game()

    tk.Button(start_screen,text='Start',width=20,command=set_mode_and_start).pack(pady=12)
    tk.Button(start_screen,text='Quit',width=20,command=window.destroy).pack(pady=4)

    show_screen(start_screen)
    window.mainloop()


build_window()
