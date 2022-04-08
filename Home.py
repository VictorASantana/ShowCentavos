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
import paho.mqtt.client as mqtt
import time

#Variáveis Globais:
global name
global bitword

#Variáveis de comunicação com a FPGA
global bitname
global ledAceso
ledAceso = 0
global correct
correct = -1
global qualJogadorResponde
qualJogadorResponde = ""
global quemGanhou
quemGanhou = ""

#Variáveis usadas pela própria interface
counter = 0
score = 0
popup_wrong = Popup(title='Errado', content=Label(text='Resposta errada'), size_hint=(None, None), size=(400, 400))
popup_correct = Popup(title='Certo', content=Label(text='Resposta correta'), size_hint=(None, None), size=(400, 400))
popup_player1 = Popup(title='Vitória do jogador 1', content=Label(text='Victor venceu o jogo'), size_hint=(None, None), size=(400, 400))
popup_player2 = Popup(title='Vitória do jogador 2', content=Label(text='Pedro venceu o jogo'), size_hint=(None, None), size=(400, 400))
popup_draw = Popup(title='Empate', content=Label(text='O jogo terminou em empate'), size_hint=(None, None), size=(400, 400))

global enable
enable = 0

# Login no MQTT
user = "grupo1-bancadaA3"
passwd = "L@Bdygy1A3"
Broker = "labdigi.wiseful.com.br"
Port = 80
KeepAlive = 60

# MQTT (Callback de conexao)
def on_connect(client, userdata, flags, rc):
    print("Conectado com codigo " + str(rc))
    client.subscribe(user+"/E0", qos=0) # Resposta A
    client.subscribe(user+"/E1", qos=0) # Resposta B
    client.subscribe(user+"/E2", qos=0) # Resposta C
    client.subscribe(user+"/E3", qos=0) # Resposta D
    client.subscribe(user+"/E4", qos=0) # Jogar
    client.subscribe(user+"/E5", qos=0) # Reset
    #client.subscribe(user+"/E6", qos=0) # Botao Jogador 1
    #client.subscribe(user+"/E7", qos=0) # Botao Jogador 2
    #client.subscribe(user+"/RX", qos=0) # Sobra
    client.subscribe(user+"/S0", qos=0) # Led Jogador 1
    client.subscribe(user+"/S1", qos=0) # Led Jogador 2
    client.subscribe(user+"/S2", qos=0) # Acertou Pergunta
    client.subscribe(user+"/S3", qos=0) # Vitoria Jogador 1
    client.subscribe(user+"/S4", qos=0) # Vitoria Jogador 2
    client.subscribe(user+"/S5", qos=0) # Empate
    #client.subscribe(user+"/S6", qos=0) # Sobra
    #client.subscribe(user+"/S7", qos=0) # Sobra
    #client.subscribe(user+"/TX", qos=0) # Sobra

# MQTT (Callback de mensagem)
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload)) # Printa no terminal o topico alterado
    
    global correct
    global ledAceso
    global qualJogadorResponde
    global quemGanhou
    
    if str(msg.topic+" "+str(msg.payload)) == user+"/S0 b'1'" :
        ledAceso = 1
        qualJogadorResponde = 0
    elif str(msg.topic+" "+str(msg.payload)) == user+"/S1 b'1'" :
        ledAceso = 1
        qualJogadorResponde = 1
    elif ((str(msg.topic+" "+str(msg.payload)) == user+"/S2 b'1'") and 
          (ledAceso == 1)) :
        correct = 1
    elif (((str(msg.topic+" "+str(msg.payload)) == user+"/S0 b'0'") or 
           (str(msg.topic+" "+str(msg.payload)) == user+"/S1 b'0'")) and
           (correct == -1)) :
        correct = 0
        ledAceso = 0
    elif str(msg.topic+" "+str(msg.payload)) == user+"/S3 b'1'" :
        quemGanhou = "jogador 1"
    elif str(msg.topic+" "+str(msg.payload)) == user+"/S4 b'1'" :
        quemGanhou = "jogador 2"
    elif str(msg.topic+" "+str(msg.payload)) == user+"/S5 b'1'" :
        quemGanhou = "Empate"

# MQTT Cria cliente
client = mqtt.Client()
client.on_connect = on_connect      
client.on_message = on_message  
client.username_pw_set(user, passwd)

def zeraResposta():
    client.publish(user+"/E0", payload="0", qos=0, retain=False)
    client.publish(user+"/E1", payload="0", qos=0, retain=False)
    client.publish(user+"/E2", payload="0", qos=0, retain=False)
    client.publish(user+"/E3", payload="0", qos=0, retain=False)
    

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
        global bitname
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
    player = StringProperty("Esperando resposta. ")

    def reset(self):
        global counter
        counter = 0
        self.content = "Pressione qualquer botão para iniciar"
        self.contentA = "Alternativa A"
        self.contentB = "Alternativa B"
        self.contentC = "Alternativa C"
        self.contentD = "Alternativa D"
        client.publish(user+"/E5", payload="1", qos=0, retain=False)
        time.sleep(1)
        client.publish(user+"/E5", payload="0", qos=0, retain=False)
        zeraResposta()
        global quemGanhou
        quemGanhou = ""
        global qualJogadorResponde
        qualJogadorResponde = ""

    def first(self):
        global counter
        if counter < 16:
            global bitname
            print(bitname)

    def btnA(self):
        bitword = "1000"
        # print(bitword)
        
        global quemGanhou
        global qualJogadorResponde
        global bitname
        global correct
        correct = -1
        
        # Responde a pergunta
        if bitname == qualJogadorResponde :
            self.player = "Jogador 1 responde a pergunta."
            client.publish(user+"/E0", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E0", payload="0", qos=0, retain=False)
        # Ativa o botão jogar, serve para a parte do aperte qualquer botão para iniciar
        elif qualJogadorResponde == "" :
            self.player = "Jogador 2 responde a pergunta."
            client.publish(user+"/E4", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E4", payload="0", qos=0, retain=False)
            time.sleep(0.1)

        global counter
        if 0 < counter < 16:
            while correct == -1:
                time.sleep(0.1)

            # Só considera certo se você pediu para apertar a resposta primeiro
            if correct == 1 and qualJogadorResponde == bitname:
                popup_correct.open()
            else:
                popup_wrong.open()
            
            qualJogadorResponde = -1
            
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
            if quemGanhou == "jogador 1" :
                popup_player1.open()
            elif quemGanhou == "jogador 2" :
                popup_player2.open()
            elif quemGanhou == "Empate" :
                popup_draw.open()


    def btnB(self):
        bitword = "0100"
        # print(bitword)
        
        global quemGanhou
        global qualJogadorResponde
        global bitname
        global correct
        correct = -1
        
        # Responde a pergunta
        if bitname == qualJogadorResponde :
            client.publish(user+"/E1", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E1", payload="0", qos=0, retain=False)
        # Ativa o botão jogar, serve para a parte do aperte qualquer botão para iniciar
        elif qualJogadorResponde == "" :
            client.publish(user+"/E4", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E4", payload="0", qos=0, retain=False)
            time.sleep(0.1)

        global counter
        if 0 < counter < 16:
            while correct == -1:
                time.sleep(0.1)
                
            if correct == 1 and qualJogadorResponde == bitname:
                popup_correct.open()
            else:
                popup_wrong.open()
                
            qualJogadorResponde = -1
            
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
            if quemGanhou == "jogador 1" :
                popup_player1.open()
            elif quemGanhou == "jogador 2" :
                popup_player2.open()
            elif quemGanhou == "Empate" :
                popup_draw.open()

    def btnC(self):
        bitword = "0010"
        # print(bitword)
        
        # Ativa o botão jogar, serve para a parte do aperte qualquer botão para iniciar
        client.publish(user+"/E4", payload="1", qos=0, retain=False)
        
        global quemGanhou
        global qualJogadorResponde
        global bitname
        global correct
        correct = -1
        
        # Responde a pergunta
        if bitname == qualJogadorResponde :
            client.publish(user+"/E2", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E2", payload="0", qos=0, retain=False)
        # Ativa o botão jogar, serve para a parte do aperte qualquer botão para iniciar
        elif qualJogadorResponde == "" :
            client.publish(user+"/E4", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E4", payload="0", qos=0, retain=False)
            time.sleep(0.1)
            
        global counter
        if 0 < counter < 16:
            while correct == -1:
                time.sleep(0.1)
                
            if correct == 1 and qualJogadorResponde == bitname:
                popup_correct.open()
            else:
                popup_wrong.open()
            
            qualJogadorResponde = -1
            
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
            if quemGanhou == "jogador 1" :
                popup_player1.open()
            elif quemGanhou == "jogador 2" :
                popup_player2.open()
            elif quemGanhou == "Empate" :
                popup_draw.open()


    def btnD(self):
        bitword = "0001"
        # print(bitword)
        
        global quemGanhou
        global qualJogadorResponde
        global bitname
        global correct
        correct = -1
        
        # Responde a pergunta
        if bitname == qualJogadorResponde :
            client.publish(user+"/E3", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E3", payload="0", qos=0, retain=False)
        # Ativa o botão jogar, serve para a parte do aperte qualquer botão para iniciar
        elif qualJogadorResponde == "" :
            client.publish(user+"/E4", payload="1", qos=0, retain=False)
            time.sleep(1)
            client.publish(user+"/E4", payload="0", qos=0, retain=False)
            time.sleep(0.1)
        
        global counter
        if 0 < counter < 16:
            while correct == -1:
                time.sleep(0.1)
                
            if correct == 1 and qualJogadorResponde == bitname:
                popup_correct.open()
            else:
                popup_wrong.open()
            
            qualJogadorResponde = -1
            
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
            if quemGanhou == "jogador 1" :
                popup_player1.open()
            elif quemGanhou == "jogador 2" :
                popup_player2.open()
            elif quemGanhou == "Empate" :
                popup_draw.open()



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
    client.connect(Broker, Port, KeepAlive)
    client.loop_start()
    
    zeraResposta()
    
    ParentApp().run()
    
    client.loop_stop()
    client.disconnect()

