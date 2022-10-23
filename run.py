import speech_recognition as sr
from nltk import word_tokenize, corpus
import json 

class Lucy:
    def __init__(self):
        self.keepListening = True
        self.LANGUAGE = 'portuguese'
        self.stopwords = set(corpus.stopwords.words(self.LANGUAGE))
       
        with open('movies.json', "r") as movies_file:
            file_read = json.load(movies_file)
            self.movies = file_read['movies']
            movies_file.close()

        with open('config.json', "r") as config_file:
            config = json.load(config_file)

            self.assistant_name = config["name"]
            self.actions = config["actions"]

            config_file.close()
            
    def main(self):
        print(self.movies, self.actions)
        while self.keepListening:
            try:
                command = self.get_speech()
                
                if command:
                    action, object = self.get_token(self,command)
                    isValid = self.command_validation(self, action , object)

                    if isValid:
                        self.command_exec(self, action)
                    else:
                        print("Não entendi o que você falou!")
            except KeyboardInterrupt:
                print('bye')
                self.keepListening = False
    
    @staticmethod
    def get_speech():
        command = None
        recognizer = sr.Recognizer()
            
        with sr.Microphone() as audio_src:
            recognizer.adjust_for_ambient_noise(audio_src)
            
            print('Diga alguma coisa... ')
            speech = recognizer.listen(audio_src, timeout=5,)
            
            try:
                command = recognizer.recognize_google(speech, language='pt-BR')
                
                print('Comando: ', command)
            except sr.UnknownValueError:
                print('Alguma coisa deu errado')
        
        return command

    @staticmethod
    def remove_stopwords(self, tokens):
        filtered_tokens = []

        for token in tokens:
            if token not in self.stopwords:
                filtered_tokens.append(token)

        return filtered_tokens
    
    @staticmethod
    def get_token(self, command):
        action = None
        object = None
        
        tokens = word_tokenize(command, self.LANGUAGE)
        if tokens:
            tokens = self.remove_stopwords(self,tokens)
            
        print("token >>> " + str(tokens))
                
        if len(tokens) >= 3:
            for name in self.assistant_name:
                if name == tokens[0].lower():
                    action = tokens[1].lower()
                    object = tokens[len(tokens) - 1].lower()   
        return action, object

    @staticmethod
    def command_validation(self, action, object):        
        isValid = False
        
        if action and object:
            for registered_action in self.actions:
                if action == registered_action["name"]:
                    if object in registered_action["objects"]:
                        isValid = True
                    break
        
        return isValid
    
    @staticmethod
    def point_movies(self):
        print("Qual a categoria do filme?")

        try:
            command = self.get_speech()
            movies = []
            for movie in self.movies:
                if movie['gender'] == command.lower():
                    movies.append(movie['name'])

            if len(movies) == 0: 
                print('Nenhum filme encontrado com essa categoria')
                return None

            print (f'Os filmes de {command} que eu encontrei são {movies}')
        except:
            print('ocorreu um erro')

    @staticmethod
    def get_movies_in_theater(self):
        try:
            movies = []
            for movie in self.movies:
                if movie['inTheaters'] == True:
                    movies.append(movie['name'])

            if len(movies) == 0: 
                print('Nenhum filme em cartaz')
                return None
            
            print (f'Os filmes que estão em cartaz são {movies}')
        except:
            print('ocorreu um erro')

    @staticmethod
    def get_synopsis(self):
        print("Qual o filme?")

        try:
            command = self.get_speech()
            synopsis = ''
            for movie in self.movies:
                if movie['name'].lower() == command.lower():
                    synopsis = movie['synopsis']
            if synopsis == '': 
                print('Não foi possivel encontrar a sinopse desse filme')
                return None
            
            print (f'A sinopse do filme {command} é {synopsis}')
        except:
            print('ocorreu um erro')
    
    @staticmethod
    def command_exec(self, action):
        if action == 'listar':
            self.get_movies_in_theater(self)
                
        if action == 'indicar':
            self.point_movies(self)

        if action == 'mostrar':
            self.get_synopsis(self)
            
        if action == 'parar':
            print('bye')
        
            self.keepListening = False
        
lu = Lucy()

lu.main()