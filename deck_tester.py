import pyautogui
import os
from datetime import datetime
import time

time_format = "%d-%m-%Y %H:%M:%S"
user_=os.getlogin()
caminho=f'C:\\Users\\{user_}\\AppData\\Roaming\\Forge'

def get_last_line():
        with open(caminho+'\\forge.log', 'r') as f:
            return f.read().strip().split('\n')[-1]

def x_at_the_end():
        with open(caminho+'\\forge.log', 'r') as f:
            return f.read().strip()[-1]=='X'

def addx():
    with open(caminho+'\\forge.log', 'a') as f:
        f.write('\nX')

def get_match_result():
    with open(caminho+'\\forge.log', 'r') as f:
        return f.read().strip().split('\n')[-3]

def playmatch(deck_1, deck_2, num_games):
    addx()
    os.system(f'forge.exe sim -d "{deck_1}.dck" "{deck_2}.dck" -n {num_games} -q')
    while x_at_the_end():
        time.sleep(1)
    i=1
    wins_1=0
    wins_2=0
    while i<=num_games:
        last_line=get_last_line()
        if f'Game Result: Game {i}' in last_line:
            if ')-'+deck_1+' has won!' in last_line:
                winner=deck_1
                wins_1+=1
            else:
                winner=deck_2
                wins_2+=1
            print(f'Game {i}: {winner}')
            i+=1
    return wins_1,wins_2

def calculatewins(wins_1,wins_2, start_, deck_1, deck_2):
    end_=datetime.now()-start_
    winrate_1=(wins_1*100)/(wins_1+wins_2)
    winrate_2=(wins_2*100)/(wins_1+wins_2)
    mensagem=f'\nTempo de execução: {end_}\n'
    if winrate_1>=winrate_2:
        mensagem+=f'\n{winrate_1:.2f}% de vitória para {deck_1} ({wins_1} vitória(s)).\n'
        mensagem+=f'{winrate_2:.2f}% de vitória para {deck_2} ({wins_2} vitória(s)).\n'
    else:
        mensagem+=f'\n{winrate_2:.2f}% de vitória para {deck_2} ({wins_2} vitória(s)).\n'
        mensagem+=f'{winrate_1:.2f}% de vitória para {deck_1} ({wins_1} vitória(s)).\n'
    
    mensagem=f'''{mensagem}\n#################\n'''
    
    print(mensagem)
    return mensagem+'\n'

def salvarlog(mensagem):
    time=datetime.now()

    time=datetime.strftime(time, time_format)

    with open('resultados.log','a', encoding='utf8') as f:
        log=f'[{time}]\n'+mensagem
        f.write(log)

def main():
    deck_1=input('Digite o nome do primeiro deck: ').strip().replace('.dck','')
    while deck_1+'.dck' not in os.listdir(caminho+'\\decks\\'):
        print(f'Deck inexistente! Certifique-se que seu deck esteja salvo como [nome_do_deck].dck em {caminho}\\decks')
        deck_1=input('Digite o nome do primeiro deck: ').strip().replace('.dck','')

    deck_2=input('Digite o nome do segundo deck: ').strip().replace('.dck','')
    while deck_1+'.dck' not in os.listdir(caminho+'\\decks\\'):
        print(f'Deck inexistente! Certifique-se que seu deck esteja salvo como [nome_do_deck].dck em {caminho}\\decks')
        deck_2=input('Digite o nome do segundo deck: ').strip().replace('.dck','')

    num_games=int(input('Digite a quantidade de partidas: '))
    print()

    start_=datetime.now()
    wins_1,wins_2=playmatch(deck_1, deck_2, num_games)
    salvarlog(calculatewins(wins_1,wins_2, start_, deck_1, deck_2))

if __name__=='__main__':
    while True:
        main()
