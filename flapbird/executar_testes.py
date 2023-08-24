from backend.geral.config import *
from backend.testes import *

# inserindo a aplicação em um contexto :-/
with app.app_context():

    TestarJogador.run()