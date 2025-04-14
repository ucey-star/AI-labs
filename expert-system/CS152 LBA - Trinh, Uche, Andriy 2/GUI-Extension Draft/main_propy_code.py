# The code here will ask the user for input based on the askables. It will only ask the user where necessary.

# Import necessary packages
import tempfile
import numpy as np
from pyswip.prolog import Prolog
from pyswip.easy import *
from tkinter import *
import re
import pylcs
import nltk 


prolog = Prolog() # Global handle to interpreter
prolog.consult("expert_system.pl")

retractall = Functor("retractall")
known = Functor("known",3)

responses = {'yongkang_street': "Yongkang street: https://goo.gl/maps/FuvJmag1fDuon3yZ7",
             'taipei101': "Taipei 101: https://goo.gl/maps/5uFYd1T1DnWyeinj7",
             'raohe_market': "Raohe Market: https://goo.gl/maps/HxueeHweQKqSpQer6",
             'zhongshan_street': "Zhongshan Street: https://goo.gl/maps/pBAUduvuDccmwkLv9",
             'dihua_street': "Dihua Street: https://goo.gl/maps/RkEwL6picyg4U5Wf9",
             'taipei_fine_art_museum': "Taipei Fine Arts Museum: https://goo.gl/maps/ZoCKihpggAxrGTSW9",
             'national_palace_museum': "National Palace Museum: https://goo.gl/maps/fqf11Kq3rcDGJfuB9",
             'chiang_shek_memorial_hall': "Chiang Kai-Shek Memorial Hall: https://goo.gl/maps/AnfcieZFnvhpiScZ8",
             'huashan_creative_park': "Huashan 1914 Creative Park: https://goo.gl/maps/psRLb7XZYHxbZkzT9",
             'eslite_bookstore_taipei101': "Eslite Bookstore Taipei101: https://goo.gl/maps/RHD2NT5b3ZwZnuVH7",
             'elephant_mountain': "Elephant Mountain: https://goo.gl/maps/VQXRm5UZMkHEtrv99",
             'daan_park': "Daan Forest Park: https://goo.gl/maps/tVKErFBuhqdwfQU49",
             'songshan_creative_park': "Songshan Creative Park: https://goo.gl/maps/Z3EgqF8NRLYGAaW28",
             'jiufen': "Jiufen: https://goo.gl/maps/9ibSr6LszsTN6BsR8",
             'gongguan_market': "Gongguan Market: https://goo.gl/maps/LriJznxCXsJCqnPE8"
            }

# Define foreign functions for getting user input and writing to the screen
def write_py(X):
    print(str(X))
    sys.stdout.flush()
    return True

def read_py(A,V,Y):
    if isinstance(Y, Variable):
        response = input("Confirm that your " + str(A) + " is " + str(V).capitalize() + "? (type yes/no)")
        Y.unify(response)
        return True
    else:
        return False


def classify_input(response_input, Menu):
    try:
        # if users input an integer
        if int(response_input) in range(1, len(Menu) + 1):
            return int(response_input)
        else:
            return False
    except ValueError:
        # if users input a non-integer string
        response = find_answer(Menu, response_input)
        if len(response_input) ==0:
            return False
        return response + 1
    return False
           
def read_menu_py(A, Y, Menu):
    Menu = [atom.value for atom in Menu]
    if isinstance(Y, Variable):
        menu_questions = "" + str(A) + "\n"
        for i in range(len(Menu)):
            menu_questions += f"{i+1}. {str(Menu[i])} \n"
        print(menu_questions)
        while True:
            try:
                response_input = input("Previous input: ".format(len(Menu)))
                response_input = classify_input(response_input,Menu) 
                #print(response_input)
                if response_input is False:
                    raise ValueError
                break
            except ValueError:
                print("Invalid input. Please try again.\n")
        response = str(Menu[int(response_input) - 1])
        Y.unify(response)
        return True
    else:
        return False


#Reference: https://www.geeksforgeeks.org/normalizing-textual-data-with-python/
def normalize_text(text):
    # ensure its lowercase
    text = text.lower()
    # remove numbers
    text = re.sub(r'\d+', '', text)
    # remove punctuations
    text = re.sub(r'[^\w\s]','',text) 
    # remove 's from the end of words
    text = re.sub(r'\b(\w+)(\'s)\b', r'\1', text)  
    # remove spaces
    text = re.sub(r'\s+', ' ', text)
    # remove stopwords 
    #stopwords = set(nltk.corpus.stopwords.words('english'))
    #text = ''.join([word for word in text.split() if word not in stopwords])
    text = ''.join([word for word in text.split()])
    # return the normalized text
    return text.strip()
    
def find_answer(list_options, response):
    """
    Using lcs to match patterns"""
    #normalize data
    list_texts = []
    length = []
    for i in list_options:
        text_normalized = normalize_text(i)
        list_texts.append(text_normalized)
    response = normalize_text(response)
    lcs_list = pylcs.lcs_of_list(response, list_options)
    for option in list_texts:
        length.append(len(option))
    similar_rate = np.array(lcs_list)/np.array(length)
    # find option with highest similarity rate
    answer_idx= np.array(similar_rate).argmax()
    
    #if the similarity rate between the possible 
    #response and the user response is less than 0.2
    #it is likely to be a coincidence
    if similar_rate[answer_idx] < 0.2:
        return False
    return int(answer_idx)
    
write_py.arity = 1
read_py.arity = 3
read_menu_py.arity = 3


registerForeign(read_py)
registerForeign(read_menu_py)
registerForeign(write_py)

# Create a temporary file with the KB in it
(FD, name) = tempfile.mkstemp(suffix='.pl', text = "True")
with os.fdopen(FD, "w") as text_file:
    text_file.write(KB)
prolog.consult(name) # open the KB for consulting
os.unlink(name) # Remove the temporary file

call(retractall(known))
place = [s for s in prolog.query("place(X).", maxresult=1)]

if place and place[0]['X'] != 'ask_others':
    print("Your recommendation is " + responses[place[0]['X']] + ".")
elif place and place[0]['X'] == 'ask_others':
    print("Sorry, we don't have any recommendations based on your preferences, but you can ask others for suggestions.")
else:
    print("Sorry, we don't have any recommendations based on your preferences, but you can ask others for suggestions.")

def send_input():
    user_input = input_box.get()
    # Send input to Prolog engine for processing
    response = prolog.query("classify_input({}, Response)".format(user_input))
    # Get response from Prolog engine and update display
    for solution in response:
        output_box.insert(END, "Bot -> {}\n".format(solution["Response"]))
        break

# Create GUI window
window = Tk()
window.title("Expert System")

# Create input box
input_box = Entry(window)
input_box.pack()

# Create send button
send_button = Button(window, text="Send", command=send_input)
send_button.pack()

# Create output box
output_box = Text(window)
output_box.pack()

window.mainloop()
