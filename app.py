from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, make_response
from io import StringIO
import csv
import sqlite3
import os
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(
    __name__, static_folder='static')
app.secret_key = 'sua_chave_secreta_aqui'

# Configurações para upload de arquivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

usuarios = {
    'admin': {
        'senha': 'senha123',
        'tipo': 'admin'
    },
    'funcionario': {
        'senha': 'senha456',
        'tipo': 'funcionario'
    }
}
def allowed_file(filename):
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS

def criar_banco_de_dados():
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                nome_social TEXT,
                prontuario TEXT,
                situacao_cadastro TEXT,
                data_entrada_saida TEXT,
                cpf TEXT,
                rg TEXT,
                data_emissao_rg TEXT,
                cartao_nascimento TEXT,
                livro_folha TEXT,
                cartorio TEXT,
                naturalidade TEXT,
                sexo TEXT,
                data_nascimento TEXT,
                ocupacao TEXT,
                carteira_pcd TEXT,
                cartao_nis TEXT,
                cartao_sus TEXT,
                raca_cor TEXT,
                mobilidade TEXT,
                tipo_deficiencia TEXT,
                transtornos TEXT,
                cid10 TEXT,
                cid10_opcional1 TEXT,
                cid10_opcional2 TEXT,
                cid11 TEXT,
                area TEXT,
                cep TEXT,
                endereco TEXT,
                numero TEXT,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                uf TEXT,
                email TEXT,
                telefone_residencial TEXT,
                telefone_recados TEXT,
                pessoa_contato TEXT,
                mae_nome TEXT,
                mae_cpf TEXT,
                mae_telefone TEXT,
                mae_email TEXT,
                mae_ocupacao TEXT,
                pai_nome TEXT,
                pai_cpf TEXT,
                pai_telefone TEXT,
                pai_email TEXT,
                pai_ocupacao TEXT,
                medicamento TEXT,
                qual_medicamento TEXT,
                alergia TEXT,
                qual_alergia TEXT,
                comorbidade TEXT,
                qual_comorbidade TEXT,
                convenio TEXT,
                qual_convenio TEXT,
                atividade_fisica TEXT,
                data_liberacao TEXT,
                uso_imagem TEXT,
                transporte_ida TEXT,
                transporte_volta TEXT,
                observacoes TEXT,
                notificacao_whatsapp TEXT,
                laudo_nome TEXT,
                laudo_caminho TEXT,
                data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER,
                usuario_nome TEXT,
                tipo TEXT NOT NULL,
                mensagem TEXT NOT NULL,
                data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pendente',
                resposta TEXT,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                tipo_consulta TEXT NOT NULL,
                preferencia_data TEXT,
                preferencia_horario TEXT,
                mensagem TEXT,
                status TEXT DEFAULT 'pendente',
                data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_confirmacao TIMESTAMP,
                responsavel TEXT
            )
        ''')

        conn.commit()
        print("Banco de dados criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario' not in session:
            flash('Por favor, faça login para acessar esta página', 'danger')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('tipo_usuario') != 'admin':
            flash('Acesso restrito a administradores', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/agendamento', methods=['GET', 'POST'])
@login_required
def agendamento():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip()
        telefone = request.form.get('telefone', '').strip()
        tipo_consulta = request.form.get('tipo_consulta', '').strip()
        preferencia_data = request.form.get('preferencia_data', '').strip()
        preferencia_horario = request.form.get('preferencia_horario', '').strip()
        mensagem = request.form.get('mensagem', '').strip()

        if not nome or not email or not telefone or not tipo_consulta:
            flash('Por favor, preencha todos os campos obrigatórios', 'danger')
            return redirect(url_for('agendamento'))

        try:
            with sqlite3.connect('usuarios.db') as conn:
                cursor = conn.cursor()
                cursor.execute('''
                            INSERT INTO agendamentos
                            (nome, email, telefone, tipo_consulta, preferencia_data, preferencia_horario, mensagem)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', (nome, email, telefone, tipo_consulta, preferencia_data, preferencia_horario, mensagem))
                conn.commit()

            flash('Solicitação de agendamento enviada com sucesso! Entraremos em contato em breve.', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Erro ao enviar solicitação: {str(e)}', 'danger')
            return redirect(url_for('agendamento'))

    return render_template('agendamento.html')

@app.route('/admin/agendamentos')
@admin_required
def listar_agendamentos():
    status = request.args.get('status', 'pendente')
    with sqlite3.connect('usuarios.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        query = "SELECT * FROM agendamentos"
        params = []
        if status != 'todos':
            query += " WHERE status = ?"
            params.append(status)
        query += " ORDER BY data_solicitacao DESC"
        cursor.execute(query, params)
        agendamentos = cursor.fetchall()
    return render_template('admin/agendamentos.html', agendamentos=agendamentos, status=status)

@app.route('/admin/agendamento/<int:id>/editar', methods=['POST'])
@admin_required
def editar_agendamento(id):
    novo_status = request.form['status']
    responsavel = request.form.get('responsavel', '').strip()
    mensagem = request.form.get('mensagem', '').strip()
    try:
        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            if novo_status == 'confirmado':
                cursor.execute('''
                            UPDATE agendamentos
                            SET status = ?, responsavel = ?, data_confirmacao = CURRENT_TIMESTAMP
                            WHERE id = ?
                            ''', (novo_status, responsavel, id))
            else:
                cursor.execute('''
                            UPDATE agendamentos
                            SET status = ?, responsavel = ?, mensagem = ?
                            WHERE id = ?
                            ''', (novo_status, responsavel, mensagem, id))
            conn.commit()
        flash('Agendamento atualizado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao atualizar agendamento: {str(e)}', 'danger')
    return redirect(url_for('listar_agendamentos'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()
        if not usuario or not senha:
            flash('Preencha todos os campos', 'danger')
            return redirect(url_for('login'))
        if usuario in usuarios and usuarios[usuario]['senha'] == senha:
            session['usuario'] = usuario
            session['nome_usuario'] = usuario.capitalize()
            session['tipo_usuario'] = usuarios[usuario]['tipo']
            flash(f'Bem-vindo, {usuario.capitalize()}!', 'success')
            return redirect(url_for('home'))
        flash('Usuário ou senha incorretos', 'danger')
        return redirect(url_for('login'))
    if 'usuario' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email:
            flash('Por favor, informe seu e-mail', 'danger')
            return redirect(url_for('esqueci_senha'))
        flash('Se o e-mail estiver cadastrado, enviaremos instruções para recuperação', 'info')
        return redirect(url_for('login'))
    return render_template('esqueci_senha.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('nome_usuario', None)
    session.pop('tipo_usuario', None)
    flash('Você saiu do sistema', 'info')
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro():
    if request.method == 'POST':
        try:
            laudo_nome = ''
            laudo_caminho = ''

            file = request.files.get('laudo')
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                laudo_nome = filename
                laudo_caminho = filepath

            dados = request.form.to_dict(flat=False)
            dados_limpos = {
                chave: ','.join(valor) if isinstance(valor, list) else valor
                for chave, valor in dados.items()
            }

            campos = [
                'nome', 'nome_social', 'prontuario', 'situacao_cadastro', 'data_entrada_saida',
                'cpf', 'rg', 'data_emissao_rg', 'cartao_nascimento', 'livro_folha', 'cartorio',
                'naturalidade', 'sexo', 'data_nascimento', 'ocupacao', 'carteira_pcd', 'cartao_nis',
                'cartao_sus', 'raca_cor', 'mobilidade', 'tipo_deficiencia', 'transtornos',
                'cid10', 'cid10_opcional1', 'cid10_opcional2', 'cid11', 'area', 'cep', 'endereco',
                'numero', 'complemento', 'bairro', 'cidade', 'uf', 'email', 'telefone_residencial',
                'telefone_recados', 'pessoa_contato', 'mae_nome', 'mae_cpf', 'mae_telefone',
                'mae_email', 'mae_ocupacao', 'pai_nome', 'pai_cpf', 'pai_telefone', 'pai_email',
                'pai_ocupacao', 'medicamento', 'qual_medicamento', 'alergia', 'qual_alergia',
                'comorbidade', 'qual_comorbidade', 'convenio', 'qual_convenio', 'atividade_fisica',
                'data_liberacao', 'uso_imagem', 'transporte_ida', 'transporte_volta',
                'observacoes', 'notificacao_whatsapp', 'laudo_nome', 'laudo_caminho'
            ]

            valores = [dados_limpos.get(campo, '') for campo in campos[:-2]]
            valores.extend([laudo_nome, laudo_caminho])

            with sqlite3.connect('usuarios.db') as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    INSERT INTO usuarios ({','.join(campos)})
                    VALUES ({','.join(['?'] * len(campos))})
                ''', valores)
                conn.commit()

            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

@app.route('/feedback', methods=['GET', 'POST'])
@login_required
def feedback():
    if request.method == 'POST':
        tipo = request.form.get('tipo')
        mensagem = request.form.get('mensagem', '').strip()

        if not mensagem:
            flash('Por favor, escreva sua mensagem', 'danger')
            return redirect(url_for('feedback'))

        try:
            with sqlite3.connect('usuarios.db') as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM usuarios WHERE nome = ?", (session['nome_usuario'],))
                usuario = cursor.fetchone()
                usuario_id = usuario[0] if usuario else None

                cursor.execute('''
                            INSERT INTO feedbacks (usuario_id, usuario_nome, tipo, mensagem)
                            VALUES (?, ?, ?, ?)
                            ''', (usuario_id, session['usuario'], tipo, mensagem))

                conn.commit()

            flash('Feedback enviado com sucesso! Obrigado pela contribuição.', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            flash(f'Erro ao enviar feedback: {str(e)}', 'danger')
            return redirect(url_for('feedback'))

    return render_template('feedback.html')

@app.route('/admin/feedback/<int:id>/excluir', methods=['POST'])
@admin_required
def excluir_feedback(id):
    try:
        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM feedbacks WHERE id = ?", (id,))
        flash('Feedback excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir feedback: {str(e)}', 'danger')
    return redirect(url_for('listar_feedbacks'))

@app.route('/admin/feedbacks')
@admin_required
def listar_feedbacks():
    status = request.args.get('status', 'pendente')
    try:
        with sqlite3.connect('usuarios.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            query = "SELECT * FROM feedbacks"
            params = []
            if status != 'todos':
                query += " WHERE status = ?"
                params.append(status)
            query += " ORDER BY data_envio DESC"
            cursor.execute(query, params)
            feedbacks = cursor.fetchall()
    except Exception as e:
        flash(f'Erro ao listar feedbacks: {str(e)}', 'danger')
        feedbacks = []
    return render_template('admin/feedbacks.html', feedbacks=feedbacks, status=status)

@app.route('/admin/feedback/<int:id>/responder', methods=['POST'])
@admin_required
def responder_feedback(id):
    resposta = request.form.get('resposta', '').strip()
    novo_status = request.form.get('status')
    if not resposta:
        flash('Por favor, escreva uma resposta', 'danger')
        return redirect(url_for('listar_feedbacks'))
    try:
        with sqlite3.connect('usuarios.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                        UPDATE feedbacks
                        SET resposta = ?, status = ?
                        WHERE id = ?
                        ''', (resposta, novo_status, id))
            conn.commit()
        flash('Resposta enviada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao responder feedback: {str(e)}', 'danger')
    return redirect(url_for('listar_feedbacks'))


@app.route('/exportar/usuarios_csv')
@login_required
def exportar_usuarios_csv():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]
    conn.close()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(colunas)
    writer.writerows(usuarios)
    output.seek(0)

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=usuarios_apae.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


@app.route('/usuario/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
            laudo_nome = ''
            laudo_caminho = ''
            if 'laudo' in request.files:
                file = request.files['laudo']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    laudo_nome = filename
                    laudo_caminho = filepath

            dados = request.form.to_dict(flat=False)
            dados_limpos = {}
            for chave, valor in dados.items():
                dados_limpos[chave] = ','.join(valor) if isinstance(valor, list) else valor

            campos = [
                'nome', 'nome_social', 'prontuario', 'situacao_cadastro', 'data_entrada_saida',
                'cpf', 'rg', 'data_emissao_rg', 'cartao_nascimento', 'livro_folha', 'cartorio',
                'naturalidade', 'sexo', 'data_nascimento', 'ocupacao', 'carteira_pcd', 'cartao_nis',
                'cartao_sus', 'raca_cor', 'mobilidade', 'tipo_deficiencia', 'transtornos',
                'cid10', 'cid10_opcional1', 'cid10_opcional2', 'cid11', 'area', 'cep', 'endereco',
                'numero', 'complemento', 'bairro', 'cidade', 'uf', 'email', 'telefone_residencial',
                'telefone_recados', 'pessoa_contato', 'mae_nome', 'mae_cpf', 'mae_telefone',
                'mae_email', 'mae_ocupacao', 'pai_nome', 'pai_cpf', 'pai_telefone', 'pai_email',
                'pai_ocupacao', 'medicamento', 'qual_medicamento', 'alergia', 'qual_alergia',
                'comorbidade', 'qual_comorbidade', 'convenio', 'qual_convenio', 'atividade_fisica',
                'data_liberacao', 'uso_imagem', 'transporte_ida', 'transporte_volta',
                'observacoes', 'notificacao_whatsapp'
            ]

            if laudo_nome and laudo_caminho:
                campos.extend(['laudo_nome', 'laudo_caminho'])

            set_clause = ', '.join([f"{campo} = ?" for campo in campos])
            valores = [dados_limpos.get(campo, '') for campo in campos]

            valores.append(id)

            cursor.execute(f'''
                UPDATE usuarios 
                SET {set_clause}
                WHERE id = ?
            ''', valores)

            conn.commit()
            conn.close()

            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('visualizar_usuario', id=id))

        except Exception as e:
            conn.rollback()
            conn.close()
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
            return redirect(url_for('editar_usuario', id=id))

    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)

@app.route('/download/laudo/<int:user_id>')
@login_required
def download_laudo(user_id):
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT laudo_nome, laudo_caminho FROM usuarios WHERE id = ?", (user_id,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario or not usuario['laudo_caminho']:
        flash('Laudo não encontrado', 'danger')
        return redirect(url_for('visualizar_usuario', id=user_id))

    return send_from_directory(
        os.path.dirname(usuario['laudo_caminho']),
        os.path.basename(usuario['laudo_caminho']),
        as_attachment=True,
        download_name=usuario['laudo_nome']
    )


@app.route('/usuario/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_usuario(id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("SELECT laudo_caminho FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()

    if usuario and usuario[0]:
        try:
            os.remove(usuario[0])
        except OSError:
            pass

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('listar_usuarios'))

@app.route('/usuarios')
@login_required
def listar_usuarios():
    situacao = request.args.get('situacao')
    busca = request.args.get('busca')

    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT id, nome, cpf, situacao_cadastro, data_cadastro FROM usuarios"
    conditions = []
    params = []

    if situacao and situacao != 'todos':
        conditions.append("situacao_cadastro = ?")
        params.append(situacao)

    if busca:
        conditions.append("(nome LIKE ? OR cpf LIKE ?)")
        params.extend([f"%{busca}%", f"%{busca}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY nome ASC"

    cursor.execute(query, params)
    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios, situacao=situacao, busca=busca)


@app.route('/usuario/<int:id>')
@login_required
def visualizar_usuario(id):
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('listar_usuarios'))

    return render_template('visualizar_usuario.html', usuario=usuario)


@app.route('/dashboard')
@admin_required
def dashboard():
    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM usuarios")
    total_usuarios = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as ativos FROM usuarios WHERE situacao_cadastro = 'ativo'")
    ativos = cursor.fetchone()['ativos']

    cursor.execute("SELECT COUNT(*) as inativos FROM usuarios WHERE situacao_cadastro = 'inativo'")
    inativos = cursor.fetchone()['inativos']

    cursor.execute("SELECT COUNT(*) as suspensos FROM usuarios WHERE situacao_cadastro = 'suspenso'")
    suspensos = cursor.fetchone()['suspensos']

    areas = {}
    for area in ['assistencia', 'saude', 'educacao', 'social']:
        cursor.execute("SELECT COUNT(*) as count FROM usuarios WHERE area LIKE ?", (f'%{area}%',))
        areas[area] = cursor.fetchone()['count']

    cursor.execute("SELECT nome, data_cadastro FROM usuarios ORDER BY data_cadastro DESC LIMIT 5")
    ultimos_cadastros = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html',
                        total_usuarios=total_usuarios,
                        ativos=ativos,
                        inativos=inativos,
                        suspensos=suspensos,
                        areas=areas,
                        ultimos_cadastros=ultimos_cadastros)


@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

def inicializar():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    criar_banco_de_dados()

inicializar()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
