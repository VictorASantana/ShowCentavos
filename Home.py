#Tela principal do aplicativo
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

#Variáveis Globais:
global name
global bitword
global bitname
counter = 0
score = 0
global correct

#Armazena as perguntas, acessadas via contador
def questions(counter):
    questions = ["Qual bicho transmite Doença de Chagas?",
                 "Qual fruto é conhecido no Norte e Nordeste como 'jerimum'?",
                 "Qual é o coletivo de cães?",
                 "Qual é o triângulo que tem todos os lados diferentes?",
                 "Quem compôs o Hino da Independência?",
                 "Qual é o antônimo de 'malograr'?",
                 "Em que país nasceu Carmem Miranda?",
                 "Qual foi o último Presidente do período da ditadura militar no Brasil?",
                 "Seguindo a sequência do baralho, qual carta vem depois do dez?",
                 "O adjetivo 'venoso' está relacionado a:",
                 "Que nome se dá à purificação por meio da água?",
                 "Qual montanha se localiza entre a fronteira do Tibet com o Nepal?",
                 "Em que parte do corpo se encontra a epiglote?",
                 "A compensação por perda é chamada de...",
                 "Em que dia nasceu e em que dia foi registrado o Presidente Lula?",
                 "Qual profissão utiliza uma ferramenta chamada formão?"]
    return questions[counter]

def answerA(counter):
    answerA = ["Abelha",
                "Caju",
                "Matilha",
                "Equilátero",
                "Dom. Pedro I",
                "Perder",
                "Argentina",
                "Costa e Silva",
                "Rei",
                "Vela",
                "Abolição",
                "Monte Everest",
                "Estômago",
                "Déficit",
                "6 e 27 de outubro",
                "carpinteiro"]
    return answerA[counter]

def answerB(counter):
    answerB = ["Barata",
                "Abóbora",
                "Rebanho",
                "Isóceles",
                "Manuel Bandeira",
                "Fracassar",
                "Espanha",
                "João Figueiredo",
                "Valete",
                "Vento",
                "Abnegação",
                "Monte Carlo",
                "Pâncreas",
                "Indenização",
                "8 e 26 de outubro",
                "relojoeiro"]
    return answerB[counter]

def answerC(counter):
    answerC = ["Pulga",
                 "Chuchu",
                 "Alcateia",
                 "Escaleno",
                 "Castro Alves",
                 "Conseguir",
                 "Portugal",
                 "Ernesto Geisel",
                 "Nove",
                 "Vênia",
                 "Ablução",
                 "Monte Fuji",
                 "Rim",
                 "Indexação",
                 "9 e 26 de outubro",
                 "confeiteiro"]
    return answerC[counter]

def answerD(counter):
    answerD = ["Barbeiro",
                 "Coco",
                 "Manada",
                 "Trapézio",
                 "Carlos Gomes",
                 "Desprezar",
                 "Argentina",
                 "Emílio Médici",
                 "Ás",
                 "Veia",
                 "Abrupção",
                 "Monte Branco",
                 "Boca",
                 "Indébito",
                 "7 e 23 de outubro",
                 "bombeiro"]
    return answerD[counter]

def verify():
    if correct == 1:
        global score
        score += 1


class Login(Screen):
    username = ObjectProperty(None)
    def btn(self):
        name = self.username.text
        print("Olá, ", name)
        if name == "Victor":
            bitname = 0
        elif name == "Pedro":
            bitname = 1
        print(bitname)

class Game(Screen):
    content = StringProperty("Pressione qualquer botão para iniciar")
    contentA = StringProperty()
    contentB = StringProperty()
    contentC = StringProperty()
    contentD = StringProperty()

    def reset(self):
        global counter
        counter = 0
        self.content = "Pressione qualquer botão para iniciar"
        self.contentA = "Alternativa A"
        self.contentB = "Alternativa B"
        self.contentC = "Alternativa C"
        self.contentD = "Alternativa D"

    def btnA(self):
        bitword = "1000"
        print(bitword)
        global counter
        if counter < 16:
            self.content = str(questions(counter))
            self.contentA = str(answerA(counter))
            self.contentB = str(answerB(counter))
            self.contentC = str(answerC(counter))
            self.contentD = str(answerD(counter))
            counter += 1
        else:
            self.content = "Fim de jogo, pressione Voltar"
            self.contentA = "Alternativa A"
            self.contentB = "Alternativa B"
            self.contentC = "Alternativa C"
            self.contentD = "Alternativa D"



    def btnB(self):
        bitword = "0100"
        print(bitword)
        global counter
        if counter < 16:
            self.content = str(questions(counter))
            self.contentA = str(answerA(counter))
            self.contentB = str(answerB(counter))
            self.contentC = str(answerC(counter))
            self.contentD = str(answerD(counter))
            counter += 1
        else:
            self.content = "Fim de jogo, pressione Voltar"
            self.contentA = "Alternativa A"
            self.contentB = "Alternativa B"
            self.contentC = "Alternativa C"
            self.contentD = "Alternativa D"

    def btnC(self):
        bitword = "0010"
        print(bitword)
        global counter
        if counter < 16:
            self.content = str(questions(counter))
            self.contentA = str(answerA(counter))
            self.contentB = str(answerB(counter))
            self.contentC = str(answerC(counter))
            self.contentD = str(answerD(counter))
            counter += 1
        else:
            self.content = "Fim de jogo, pressione Voltar"
            self.contentA = "Alternativa A"
            self.contentB = "Alternativa B"
            self.contentC = "Alternativa C"
            self.contentD = "Alternativa D"


    def btnD(self):
        bitword = "0001"
        print(bitword)
        global counter
        if counter < 16:
            self.content = str(questions(counter))
            self.contentA = str(answerA(counter))
            self.contentB = str(answerB(counter))
            self.contentC = str(answerC(counter))
            self.contentD = str(answerD(counter))
            counter += 1
        else:
            self.content = "Fim de jogo, pressione Voltar"
            self.contentA = "Alternativa A"
            self.contentB = "Alternativa B"
            self.contentC = "Alternativa C"
            self.contentD = "Alternativa D"




class Instructions(Screen):
    pass

class Main(Screen):
    pass

class Home(ScreenManager):
    pass

kv = Builder.load_file("parent.kv")


class ParentApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    ParentApp().run()




