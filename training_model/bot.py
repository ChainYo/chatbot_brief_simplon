import json
from keras.models import load_model
import nltk
from nltk.stem import  WordNetLemmatizer
import numpy as np
import random
from traitment_corpus import traitment_intents
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("french")

class bot:

    def __init__(self):
        
        self.lemmatizer = WordNetLemmatizer
        self.classes = traitment_intents().read_file("classes")
        self.words_list = traitment_intents().read_file("words")
        self.intents_files = json.loads(open("C:/Users/Shadow/Documents/chatbot_brief_simplon/model/ressources/intents/intents3.json",encoding='utf-8').read())
        self.model = load_model('C:/Users/Shadow/Documents/final_chat_bot/chatbot_brief_simplon/backend/app/model/model/chatbot_model.h5')
        self.stop_words = set(stopwords.words('french','english')) 
        self.sent_tokenize = nltk.data.load('tokenizers/punkt/french.pickle')
        
    
    def clean_sentences(self,sentence):

        self.new_sentence = []
        #je tokenise le pattern et split les mots en array
        self.sentences_words = nltk.word_tokenize(sentence)
        for word in self.sentences_words:
            print(word)
            self.new_sentence.extend(traitment_intents.preprocess_word(self,word))
        #print(self.sentences_words)
        #Je réduis chaque mot à sa forme de base
        self.final_sentences_words = [self.lemmatizer().lemmatize(word.lower()) for word in self.new_sentence]
        print(self.final_sentences_words)
        return self.final_sentences_words

    #Cette fonction va retourner un sac de mot sous forme d'array(0 ou 1 pour les mots existant dans la phrase)
    def bag_of_words(self,sentence,world_list,show_details=True):
        #Je tokenise les patterns
        self.sentences_words = bot().clean_sentences(sentence)
        #sac de mots matrice de vocabulaire
        bag = [0]*len(self.words_list)
        for sentence in self.sentences_words:
            for i, words in enumerate(self.words_list):
                if words == sentence:
                    #j'assigne 1 si le mot est dans le vocabulaire
                    bag[i] = 1
                    if show_details:
                        print("trouvé dans le sac: %s" % words)
        return(np.array(bag))

    def predict(self,sentence):
        #seuil de prediction
        p = bot.bag_of_words(self,sentence,self.words_list,show_details=False)
        print(p.shape)
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.2
        results = [[i,r] for i,r in enumerate(res) if r> ERROR_THRESHOLD]
        #probabilité de force de tri
        results.sort(key=lambda x: x[1],reverse=True)
        return_list = []
        [return_list.append({"intents":self.classes[r[0]], "probabilty":str([r[1]])}) for r in results]
        return return_list
    
    def get_reponse(self,ints):

        tag = ints[0]['intents']
        list_of_intents = self.intents_files['intents']
        for i in list_of_intents:
            if(i['tag'] == tag):
                result = random.choice(i['responses'])
                print(ints)
                print("classe correspondante:",tag)
                print(result)
                break
        return result

exit = ["bye", "a plus", "ciao", "au revoir", "a bientôt"]
x = ""

while x not in exit:
    x = input("posez-votre question:" )
    result = bot().predict(x)
    bot().get_reponse(result)
    x= x.lower()




