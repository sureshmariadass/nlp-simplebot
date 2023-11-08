import random
import string
import nltk
import os

import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only


#Reading in the corpus
with open('src/chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#Tokenisation
sentence_tokens = nltk.sent_tokenize(raw)# converts raw text to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts raw text to list of words

# Preprocessing
lemmatizer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmatizer.lemmatize(token) for token in tokens]


def LemNormalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello",]

def is_a_greeting(sentence):
    """If user's input is a is_a_greeting, return a is_a_greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response
def get_bot_response(user_input):
    bot_response = ''

    if(is_a_greeting(user_input)!=None):
        bot_response = is_a_greeting(user_input)
    else:
        sentence_tokens.append(user_input)
        tfidf_vectorizer = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = tfidf_vectorizer.fit_transform(sentence_tokens)
        cosine_sim_matrix = cosine_similarity(tfidf[-1], tfidf)
        idx = cosine_sim_matrix.argsort()[0][-2]
        cosine_sim_flattened = cosine_sim_matrix.flatten()
        cosine_sim_flattened.sort()
        req_tfidf = cosine_sim_flattened[-2]
        if(req_tfidf==0):
            bot_response = "I am sorry! I don't think I can help you with that at the moment..."
        else:
            bot_response = sentence_tokens[idx]
        sentence_tokens.remove(user_input)
    return bot_response


def create_and_insert_user_frame(user_input):
  userFrame = Frame(chatWindow, bg="#d0ffff")
  Label(
      userFrame,
      text=user_input,
      font=("Arial", 11),
      bg="#d0ffff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      userFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#d0ffff"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-right')
  chatWindow.window_create('end', window=userFrame)


def create_and_insert_bot_frame(bot_response):
  botFrame = Frame(chatWindow, bg="#ffffd0")
  Label(
      botFrame,
      text=bot_response,
      font=("Arial", 11),
      bg="#ffffd0",
      wraplength=400,
      justify='left'
  ).grid(row=0, column=0, sticky="w", padx=5, pady=5)
  Label(
      botFrame,
      text=datetime.now().strftime("%H:%M"),
      font=("Arial", 7),
      bg="#ffffd0"
  ).grid(row=1, column=0, sticky="w")

  chatWindow.insert('end', '\n ', 'tag-left')
  chatWindow.window_create('end', window=botFrame)
  chatWindow.insert(END, "\n\n" + "")


def send(event):
    chatWindow.tag_configure('tag-left', justify='left')
    chatWindow.tag_configure('tag-right', justify='right')
    chatWindow.config(state=NORMAL)


    user_input = userEntryBox.get("1.0",'end-2c')
    bot_response = ""
    while user_input[-1] in "!.":
      user_input = user_input[:-1]
    bot_response = get_bot_response(user_input) 

    create_and_insert_user_frame(user_input)
    create_and_insert_bot_frame(bot_response)

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
  
    # Saving the converted audio in a mp3 file
    myobj.save("audio/response.mp3")
  
    # Playing the converted file
    os.system("mpg321 audio/welcome.mp3")

    chatWindow.config(state=DISABLED)
    userEntryBox.delete("1.0","end")
    chatWindow.see('end')


baseWindow = Tk()
baseWindow.title("Chat To Speech Bot")
baseWindow.geometry("500x300")
baseWindow.bind('<Return>', send)

chatWindow = tks.ScrolledText(baseWindow, font="Arial")
chatWindow.config(state=DISABLED)

sendButton = Button(
    baseWindow,
    font=("Verdana", 12, 'bold'),
    text="Send",
    bg="#fd94b4",
    activebackground="#ff467e",
    fg='#ffffff',
    command=send)
sendButton.bind("<Button-1>", send)

userEntryBox = Text(baseWindow, bd=1, bg="white", width=38, font="Arial")

chatWindow.place(x=1, y=1, height=270, width=500)
userEntryBox.place(x=3, y=272, height=27)
sendButton.place(x=430, y=270)

create_and_insert_bot_frame("Hi, I'm Chatbot Charlie! What would you like to know?")


baseWindow.mainloop()        