from backend.geral.config import *
from backend.modelo.jogador import Jogador

def run():
    print("TESTE DE JOGADOR")
    
    j1 = Jogador(pontos = 0)
    db.session.add(j1)
    db.session.commit()
    print(j1)
    print(j1.json())