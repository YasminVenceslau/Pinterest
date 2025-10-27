# Pinterest Clone

Projeto clone do Pinterest feito com **Django**.

## Funcionalidades

- Cadastro e login de usuários  
- Criação e edição de perfil  
- Upload de imagens (pins)  
- Curtir e salvar pins  
- Organização de pins em coleções  

## Tecnologias

- **Backend:** Django  
- **Banco de Dados:** SQLite 

## Como Rodar

### Backend
```bash
cd backend
python -m venv env
source env/bin/activate  # ou env\Scripts\activate no Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
