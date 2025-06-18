from flask import Blueprint, request, jsonify
from db import buscarNoBanco, mexerNoBanco
from flask_cors import CORS

proj = Blueprint('projetos', __name__)
CORS(proj)

def get_usuario_logado():
    return 1  # Substitua por lógica real de autenticação
#----------------------------------------------------------------------------------------------------------------
@proj.route('/projetos', methods=['GET'])
def listar_projetos():
    try:
        # 1. Buscar projetos e nome do criador
        projetos = buscarNoBanco("""
            SELECT p.*, u.nome AS nome_criador
            FROM projetos p
            JOIN usuarios u ON p.usuario_criador_id = u.id
        """)

        # 2. Buscar equipe de todos os projetos
        equipes = buscarNoBanco("""
            SELECT e.projeto_id, e.usuario_id, u.nome AS nome_usuario, e.cargo
            FROM equipe_projeto e
            JOIN usuarios u ON u.id = e.usuario_id
        """)

        # 3. Buscar ambientes + técnico
        ambientes = buscarNoBanco("""
            SELECT a.*, u.nome AS tecnico_nome
            FROM ambientes_projeto a
            LEFT JOIN usuarios u ON u.id = a.usuario_id
        """)

        # 4. Buscar materiais dos ambientes
        materiais = buscarNoBanco("""
            SELECT am.ambiente_id, m.*, am.espessura_mm
            FROM ambientes_materiais am
            JOIN materiais m ON am.material_id = m.id
        """)

        # 5. Buscar mobiliários dos ambientes
        mobiliarios = buscarNoBanco("""
            SELECT am.ambiente_id, mob.*, am.quantidade
            FROM ambientes_mobiliario am
            JOIN mobiliario mob ON am.mobiliario_id = mob.id
        """)

        # --------- Montagem dos dados ---------

        # Organizar equipe por projeto
        equipe_por_projeto = {}
        for e in equipes:
            equipe_por_projeto.setdefault(e['projeto_id'], []).append({
                'usuario_id': e['usuario_id'],
                'nome': e['nome_usuario'],
                'cargo': e['cargo']
            })

        # Organizar materiais por ambiente
        materiais_por_ambiente = {}
        for m in materiais:
            materiais_por_ambiente.setdefault(m['ambiente_id'], []).append({
                'id': m['id'],
                'nome': m['nome'],
                'imagem': m['imagem'],
                'espessura_mm': m['espessura_mm']
            })

        # Organizar mobiliarios por ambiente
        mobiliarios_por_ambiente = {}
        for m in mobiliarios:
            mobiliarios_por_ambiente.setdefault(m['ambiente_id'], []).append({
                'id': m['id'],
                'nome': m['nome'],
                'imagem': m['imagem'],
                'quantidade': m['quantidade']
            })

        # Organizar ambientes por projeto
        ambientes_por_projeto = {}
        for a in ambientes:
            ambiente = {
                'id': a['id'],
                'nome_ambiente': a['nome_ambiente'],
                'tecnico_responsavel_id': a['usuario_id'],
                'tecnico_nome': a['tecnico_nome'],
                'materiais': materiais_por_ambiente.get(a['id'], []),
                'mobiliarios': mobiliarios_por_ambiente.get(a['id'], [])
            }
            ambientes_por_projeto.setdefault(a['projeto_id'], []).append(ambiente)

        # Montar o JSON final dos projetos
        for projeto in projetos:
            projeto['equipe'] = equipe_por_projeto.get(projeto['id'], [])
            projeto['ambientes'] = ambientes_por_projeto.get(projeto['id'], [])

        return jsonify(projetos)

    except Exception as e:
        return jsonify({'mensagem': f'Erro ao listar projetos: {e}'}), 500

# -----------------------------------------------------------------------------------------------------
@proj.route('/projetos/<int:id>', methods=['GET'])
def obter_projeto(id):
    try:
        projeto = buscarNoBanco("""
            SELECT p.*, u.nome AS nome_criador
            FROM projetos p
            JOIN usuarios u ON p.usuario_criador_id = u.id
            WHERE p.id = %s
        """, (id,))

        if not projeto:
            return jsonify({"mensagem": "Projeto não encontrado"}), 404

        projeto = projeto[0]

        # Buscar equipe do projeto
        projeto['equipe'] = buscarNoBanco("""
            SELECT e.usuario_id, u.nome, e.cargo
            FROM equipe_projeto e
            JOIN usuarios u ON u.id = e.usuario_id
            WHERE e.projeto_id = %s
        """, (id,))

        # Buscar ambientes do projeto
        ambientes = buscarNoBanco("""
            SELECT a.*, u.nome AS tecnico_nome
            FROM ambientes_projeto a
            LEFT JOIN usuarios u ON u.id = a.usuario_id
            WHERE a.projeto_id = %s
        """, (id,))

        for ambiente in ambientes:
            ambiente_id = ambiente['id']

            # Materiais do ambiente
            ambiente['materiais'] = buscarNoBanco("""
                SELECT m.*, am.espessura_mm
                FROM ambientes_materiais am
                JOIN materiais m ON am.material_id = m.id
                WHERE am.ambiente_id = %s
            """, (ambiente_id,))

            # Mobiliários do ambiente
            ambiente['mobiliarios'] = buscarNoBanco("""
                SELECT mob.*, am.quantidade
                FROM ambientes_mobiliario am
                JOIN mobiliario mob ON am.mobiliario_id = mob.id
                WHERE am.ambiente_id = %s
            """, (ambiente_id,))

        projeto['ambientes'] = ambientes

        return jsonify(projeto)

    except Exception as e:
        return jsonify({'mensagem': f'Erro ao obter projeto: {e}'}), 500
#--------------------------------------------------------------------------------------------------
@proj.route('/projetos', methods=['POST'])
def criar_projeto():
    try:
        data = request.get_json()
        usuario_id = get_usuario_logado()

        nome_cliente = data.get('nome_cliente')
        nome_arquiteto = data.get('nome_arquiteto')
        equipe = data.get('equipe', [])
        ambientes = data.get('ambientes', [])

        if not nome_cliente or not nome_arquiteto:
            return jsonify({"mensagem": "Dados obrigatórios ausentes"}), 400

        projeto_id = mexerNoBanco("""
            INSERT INTO projetos (nome_cliente, nome_arquiteto, usuario_criador_id)
            VALUES (%s, %s, %s)
        """, (nome_cliente, nome_arquiteto, usuario_id))

        for membro in equipe:
            mexerNoBanco("""
                INSERT INTO equipe_projeto (projeto_id, usuario_id, cargo)
                VALUES (%s, %s, %s)
            """, (projeto_id, membro['usuario_id'], membro['cargo']))

        for amb in ambientes:
            ambiente_id = mexerNoBanco("""
                INSERT INTO ambientes_projeto (projeto_id, nome_ambiente, tecnico_responsavel_id)
                VALUES (%s, %s, %s)
            """, (projeto_id, amb['nome_ambiente'], amb.get('tecnico_responsavel_id')))

            for mat in amb.get('materiais', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_materiais (ambiente_id, material_id, espessura_mm)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mat['material_id'], mat['espessura_mm']))

            for mob in amb.get('mobiliarios', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_mobiliario (ambiente_id, mobiliario_id, quantidade)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mob['mobiliario_id'], mob.get('quantidade', 1)))

        return jsonify({'mensagem': 'Projeto criado com sucesso', 'projeto_id': projeto_id}), 201

    except Exception as e:
        return jsonify({"mensagem": f"Erro ao criar projeto: {e}"}), 500

# ----------------------------------------------------------------------------------------------
@proj.route('/projetos/<int:projeto_id>', methods=['PUT'])
def atualizar_projeto(projeto_id):
    try:
        data = request.get_json()
        nome_cliente = data.get('nome_cliente')
        nome_arquiteto = data.get('nome_arquiteto')
        novo_criador_id = data.get('usuario_criador_id')
        equipe = data.get('equipe', [])
        ambientes = data.get('ambientes', [])

        if not nome_cliente or not nome_arquiteto or not novo_criador_id:
            return jsonify({"mensagem": "Dados obrigatórios ausentes"}), 400

        mexerNoBanco("""
            UPDATE projetos
            SET nome_cliente = %s, nome_arquiteto = %s, usuario_criador_id = %s
            WHERE id = %s
        """, (nome_cliente, nome_arquiteto, novo_criador_id, projeto_id))

        mexerNoBanco("DELETE FROM equipe_projeto WHERE projeto_id = %s", (projeto_id,))
        for membro in equipe:
            mexerNoBanco("""
                INSERT INTO equipe_projeto (projeto_id, usuario_id, cargo)
                VALUES (%s, %s, %s)
            """, (projeto_id, membro['usuario_id'], membro['cargo']))

        mexerNoBanco("DELETE FROM ambientes_projeto WHERE projeto_id = %s", (projeto_id,))
        for amb in ambientes:
            ambiente_id = mexerNoBanco("""
                INSERT INTO ambientes_projeto (projeto_id, nome_ambiente, tecnico_responsavel_id)
                VALUES (%s, %s, %s)
            """, (projeto_id, amb['nome_ambiente'], amb.get('tecnico_responsavel_id')))

            for mat in amb.get('materiais', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_materiais (ambiente_id, material_id, espessura_mm)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mat['material_id'], mat['espessura_mm']))

            for mob in amb.get('mobiliarios', []):
                mexerNoBanco("""
                    INSERT INTO ambientes_mobiliario (ambiente_id, mobiliario_id, quantidade)
                    VALUES (%s, %s, %s)
                """, (ambiente_id, mob['mobiliario_id'], mob.get('quantidade', 1)))

        return jsonify({'mensagem': 'Projeto atualizado com sucesso'}), 200

    except Exception as e:
        return jsonify({'mensagem': f'Erro ao atualizar projeto: {e}'}), 500

# ----------------------------------------------------------------------------------------------
@proj.route('/projetos/<int:projeto_id>', methods=['DELETE'])
def deletar_projeto(projeto_id):
    try:
        mexerNoBanco("DELETE FROM projetos WHERE id = %s", (projeto_id,))
        return jsonify({'mensagem': 'Projeto deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'mensagem': f'Erro ao deletar projeto: {e}'}), 500


