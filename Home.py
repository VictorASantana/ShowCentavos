#Interface desenvolvida para o jogo ShowDeCentavos da disciplina de PCS3635
#Nomes e NUSP:
#Pedro Henrique Rodrigues Viveiros - 11804035
#Pedro Vitor Bacic - 11806934
#Victor de Almeida Santana -11806718
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label

#Variáveis Globais:
global name
#Variáveis a serem passadas para a FPGA
global bitword
global bitname
#Variáveis usadas pela própria interface
counter = 0
score = 0
popup_wrong = Popup(title='Errado', content=Label(text='Resposta errada'), size_hint=(None, None), size=(400, 400))
popup_correct = Popup(title='Certo', content=Label(text='Resposta correta'), size_hint=(None, None),size=(400, 400))
#Variáveis recebidas pela FPGA
global correct
correct = 0
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

#Armazena as respostas da Alternativa A
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

#Armazena as respostas da Alternativa B
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

#Armazena as respostas da Alternativa C
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

#Armazena as respostas da Alternativa D
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

#Verifica se a resposta escolhida está correta
def verify():
    if correct == 1:
        global score
        score += 1

#Controle da tela de login
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

#Controle da tela de jogo
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
        if counter > 0:
            if correct == 0:
                popup_wrong.open()
            else:
                popup_correct.open()
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
        if counter > 0:
            if correct == 0:
                popup_wrong.open()
            else:
                popup_correct.open()
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
        if counter > 0:
            if correct == 0:
                popup_wrong.open()
            else:
                popup_correct.open()
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
        if counter > 0:
            if correct == 0:
                popup_wrong.open()
            else:
                popup_correct.open()
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



#Controle da tela de instruções
class Instructions(Screen):
    pass

#Controle da tela principal
class Main(Screen):
    pass

#Controle das telas
class Home(ScreenManager):
    pass

kv = Builder.load_file("parent.kv")


class ParentApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    ParentApp().run()




