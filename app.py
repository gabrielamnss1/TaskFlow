"""
================================================================================
MÓDULO: app.py - SERVIDOR WEB FLASK (FRONTEND WEB)
================================================================================
DESCRIÇÃO:
    Servidor web que fornece interface moderna e responsiva para o TaskFlow.
    Integra o backend existente com uma interface web profissional.

TECNOLOGIAS:
    - Flask: Framework web Python
    - Session: Gerenciamento de sessões de usuário
    - JSON: Comunicação com frontend via API REST

ROTAS:
    - / : Página inicial (login ou dashboard)
    - /login : Autenticação de usuário
    - /cadastro : Registro de novo usuário
    - /dashboard : Painel principal do usuário
    - /api/tarefas : CRUD de tarefas (GET, POST, PUT, DELETE)
    - /api/relatorios : Geração de relatórios
    - /logout : Encerrar sessão
================================================================================
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
import os

# Importa módulos existentes do sistema
from usuarios import (
    cadastrar_usuario, autenticar_usuario, logout, 
    get_usuario_logado, USUARIO_LOGADO
)
from tarefas import (
    criar_tarefa, listar_tarefas, editar_tarefa, 
    concluir_tarefa, excluir_tarefa, _carregar_tarefas, _encontrar_tarefa
)
from relatorios import (
    tarefas_concluidas, tarefas_pendentes, tarefas_atrasadas
)
import usuarios

app = Flask(__name__)
app.secret_key = 'taskflow-secret-key-2025'  # Chave para sessões

# ==================== FILTROS PERSONALIZADOS ====================

@app.template_filter('format_date')
def format_date(date_string):
    """Formata data para exibição"""
    try:
        dt = datetime.strptime(date_string, '%d/%m/%Y')
        return dt.strftime('%d/%m/%Y')
    except:
        return date_string

@app.template_filter('is_overdue')
def is_overdue(prazo, status):
    """Verifica se tarefa está atrasada"""
    if status == 'Concluída':
        return False
    try:
        prazo_dt = datetime.strptime(prazo, '%d/%m/%Y')
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return prazo_dt < hoje
    except:
        return False

# ==================== ROTAS DE PÁGINAS ====================

@app.route('/')
def index():
    """Página inicial - redireciona para login ou dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        login_input = request.form.get('login')
        senha = request.form.get('senha')
        
        # Autentica usando módulo existente
        usuario = autenticar_usuario(login_input, senha)
        
        if usuario:
            # Salva na sessão do Flask
            session['user_id'] = usuario['id']
            session['user_nome'] = usuario['nome']
            session['user_login'] = usuario['login']
            # Atualiza variável global para compatibilidade
            usuarios.USUARIO_LOGADO = usuario
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', erro='Login ou senha inválidos')
    
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """Página de cadastro de novo usuário"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        login_input = request.form.get('login')
        senha = request.form.get('senha')
        
        # Cadastra usando módulo existente
        if cadastrar_usuario(nome, email, login_input, senha):
            return render_template('cadastro.html', sucesso='Cadastro realizado! Faça login.')
        else:
            return render_template('cadastro.html', erro='Login já existe')
    
    return render_template('cadastro.html')

@app.route('/dashboard')
def dashboard():
    """Painel principal do usuário - requer autenticação"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Sincroniza USUARIO_LOGADO para compatibilidade
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    # Carrega tarefas do usuário
    tarefas = listar_tarefas(filtrar_por_responsavel=True)
    
    # Estatísticas
    total = len(tarefas)
    concluidas = len([t for t in tarefas if t['status'] == 'Concluída'])
    pendentes = len([t for t in tarefas if t['status'] == 'Pendente'])
    
    # Calcula atrasadas
    atrasadas = 0
    hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for t in tarefas:
        if t['status'] == 'Pendente':
            try:
                prazo_dt = datetime.strptime(t['prazo'], '%d/%m/%Y')
                if prazo_dt < hoje:
                    atrasadas += 1
            except:
                pass
    
    return render_template('dashboard.html', 
                         tarefas=tarefas,
                         stats={
                             'total': total,
                             'concluidas': concluidas,
                             'pendentes': pendentes,
                             'atrasadas': atrasadas
                         })

@app.route('/relatorios')
def relatorios():
    """Página de relatórios"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Sincroniza USUARIO_LOGADO
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    tipo = request.args.get('tipo', 'concluidas')
    
    if tipo == 'concluidas':
        todas = tarefas_concluidas()
    elif tipo == 'pendentes':
        todas = tarefas_pendentes()
    elif tipo == 'atrasadas':
        todas = tarefas_atrasadas()
    else:
        todas = []
    
    # Filtra apenas tarefas do usuário logado
    tarefas_filtradas = [t for t in todas if t['responsavel_id'] == session['user_id']]
    
    return render_template('relatorios.html', 
                         tarefas=tarefas_filtradas,
                         tipo=tipo)

@app.route('/perfil')
def perfil():
    """Página de perfil do usuário"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Carrega dados do usuário
    from usuarios import get_usuario_por_id
    usuario = get_usuario_por_id(session['user_id'])
    
    if not usuario:
        return redirect(url_for('logout_route'))
    
    return render_template('perfil.html', usuario=usuario)

@app.route('/api/perfil', methods=['PUT'])
def api_atualizar_perfil():
    """API: Atualiza informações do perfil"""
    if 'user_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    from usuarios import _carregar_usuarios, _salvar_usuarios
    
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    
    if not nome or not email:
        return jsonify({'erro': 'Nome e email são obrigatórios'}), 400
    
    usuarios_list = _carregar_usuarios()
    usuario = next((u for u in usuarios_list if u['id'] == session['user_id']), None)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    # Atualiza dados
    usuario['nome'] = nome
    usuario['email'] = email
    
    if _salvar_usuarios(usuarios_list):
        # Atualiza sessão
        session['user_nome'] = nome
        return jsonify({'sucesso': True, 'mensagem': 'Perfil atualizado'})
    else:
        return jsonify({'erro': 'Erro ao atualizar perfil'}), 500

@app.route('/logout')
def logout_route():
    """Encerra sessão do usuário"""
    logout()
    session.clear()
    return redirect(url_for('login'))

# ==================== API REST (JSON) ====================

@app.route('/api/tarefas', methods=['GET'])
def api_listar_tarefas():
    """API: Lista tarefas do usuário"""
    if 'user_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    # Sincroniza USUARIO_LOGADO
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    tarefas = listar_tarefas(filtrar_por_responsavel=True)
    return jsonify(tarefas)

@app.route('/api/tarefas', methods=['POST'])
def api_criar_tarefa():
    """API: Cria nova tarefa"""
    if 'user_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    # Sincroniza USUARIO_LOGADO
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    prazo = data.get('prazo')
    
    if not titulo or not descricao or not prazo:
        return jsonify({'erro': 'Dados incompletos'}), 400
    
    if criar_tarefa(titulo, descricao, prazo):
        return jsonify({'sucesso': True, 'mensagem': 'Tarefa criada'})
    else:
        return jsonify({'erro': 'Erro ao criar tarefa'}), 500

@app.route('/api/tarefas/<int:tarefa_id>', methods=['PUT'])
def api_editar_tarefa(tarefa_id):
    """API: Edita tarefa existente"""
    if 'user_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    # Sincroniza USUARIO_LOGADO
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    data = request.get_json()
    titulo = data.get('titulo')
    descricao = data.get('descricao')
    prazo = data.get('prazo')
    
    if editar_tarefa(tarefa_id, titulo, descricao, prazo):
        return jsonify({'sucesso': True, 'mensagem': 'Tarefa atualizada'})
    else:
        return jsonify({'erro': 'Erro ao editar tarefa'}), 500

@app.route('/api/tarefas/<int:tarefa_id>/concluir', methods=['POST'])
def api_concluir_tarefa(tarefa_id):
    """API: Marca tarefa como concluída"""
    if 'user_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    # Sincroniza USUARIO_LOGADO
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    if concluir_tarefa(tarefa_id):
        return jsonify({'sucesso': True, 'mensagem': 'Tarefa concluída'})
    else:
        return jsonify({'erro': 'Erro ao concluir tarefa'}), 500

@app.route('/api/tarefas/<int:tarefa_id>', methods=['DELETE'])
def api_excluir_tarefa(tarefa_id):
    """API: Exclui tarefa"""
    if 'user_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    # Sincroniza USUARIO_LOGADO
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    if excluir_tarefa(tarefa_id):
        return jsonify({'sucesso': True, 'mensagem': 'Tarefa excluída'})
    else:
        return jsonify({'erro': 'Erro ao excluir tarefa'}), 500

@app.route('/api/exportar/<tipo>/<formato>')
def api_exportar_relatorio(tipo, formato):
    """API: Exporta relatório em JSON ou CSV"""
    if 'user_id' not in session:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    # Sincroniza USUARIO_LOGADO
    if not usuarios.USUARIO_LOGADO or usuarios.USUARIO_LOGADO['id'] != session['user_id']:
        usuarios.USUARIO_LOGADO = {
            'id': session['user_id'],
            'nome': session['user_nome'],
            'login': session['user_login']
        }
    
    # Carrega tarefas
    if tipo == 'concluidas':
        todas = tarefas_concluidas()
    elif tipo == 'pendentes':
        todas = tarefas_pendentes()
    elif tipo == 'atrasadas':
        todas = tarefas_atrasadas()
    else:
        return jsonify({'erro': 'Tipo inválido'}), 400
    
    # Filtra por usuário
    tarefas_filtradas = [t for t in todas if t['responsavel_id'] == session['user_id']]
    
    if formato == 'json':
        from flask import make_response
        import json
        
        response = make_response(json.dumps(tarefas_filtradas, ensure_ascii=False, indent=2))
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=relatorio_{tipo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        return response
        
    elif formato == 'csv':
        from flask import make_response
        import csv
        from io import StringIO
        
        si = StringIO()
        writer = csv.writer(si)
        
        # Cabeçalho
        writer.writerow(['ID', 'Título', 'Descrição', 'Prazo', 'Status', 'Criação', 'Responsável'])
        
        # Dados
        for t in tarefas_filtradas:
            writer.writerow([
                t['id'],
                t['titulo'],
                t['descrição'],
                t['prazo'],
                t['status'],
                t['criacao'],
                t['responsavel_nome']
            ])
        
        output = si.getvalue()
        response = make_response(output)
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'
        response.headers['Content-Disposition'] = f'attachment; filename=relatorio_{tipo}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        return response
    
    return jsonify({'erro': 'Formato inválido'}), 400

# ==================== INICIALIZAÇÃO ====================

if __name__ == '__main__':
    # Cria pasta de templates se não existir
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("\n" + "="*60)
    print("TaskFlow - Interface Web Iniciando...")
    print("="*60)
    print("Acesse: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
