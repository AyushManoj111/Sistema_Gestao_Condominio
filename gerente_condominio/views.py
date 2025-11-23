from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.views.decorators.http import require_POST
from .models import *
import json
import logging
from django.utils.crypto import get_random_string
from django.db import transaction
from .models import ManutencaoGeral, ManutencaoEspecifica, Empresa, Casa, Noticia

logger = logging.getLogger('gerente_condominio')

# --- Views de Autenticação e Navegação ---

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Credenciais inválidas.')
        else:
            messages.error(request, 'Credenciais inválidas.')
    else:
        form = AuthenticationForm()
    return render(request, 'gerente_condominio/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# --- Views de Visualização (Protegidas) ---

@login_required
def dashboard(request):
    """
    Exibe o dashboard do gerente com verificação de permissão
    e carrega as notícias mais recentes.
    """
    # 1. Verificação de Permissão
    if not request.user.groups.filter(name='Gerente').exists():
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
        # Redireciona para a página de login ou outra página segura
        return redirect('login') 
    
    # 2. Busca de Notícias
    try:
        # Busca as 3 notícias mais recentes, ordenadas pela data de publicação (descrescente)
        noticias_recentes = Noticia.objects.all().order_by('-data_publicacao')[:3]
    except Exception as e:
        # Lidar com erro se o modelo Noticia não existir ou houver problema com o DB
        noticias_recentes = []
        # Opcional: Logar o erro (print(e))
        messages.warning(request, 'Não foi possível carregar as notícias. Verifique o modelo Noticia.')

    # 3. Contexto e Renderização
    context = {
        'titulo_pagina': 'Dashboard',
        'noticias_recentes': noticias_recentes
    }
    
    return render(request, 'gerente_condominio/dashboard.html', context)

# @login_required # Proteger contra acesso não-autorizado
def gerenciar_noticias(request, pk=None, acao='lista'):
    # Inicializa variáveis
    noticia = None
    erros = {}
    
    # 1. TRATAÇÃO DE PK (ID da notícia)
    if pk:
        noticia = get_object_or_404(Noticia, pk=pk)

    # 2. LÓGICA DO POST (Adicionar, Editar ou Excluir)
    if request.method == 'POST':
        if acao == 'adicionar':
            titulo = request.POST.get('titulo')
            conteudo = request.POST.get('conteudo')
            
            # Validação Manual
            if not titulo or len(titulo.strip()) == 0:
                erros['titulo'] = "O Título é obrigatório."
            if not conteudo or len(conteudo.strip()) == 0:
                erros['conteudo'] = "O Conteúdo é obrigatório."
                
            if not erros:
                Noticia.objects.create(titulo=titulo, conteudo=conteudo)
                messages.success(request, f"Notícia '{titulo}' publicada com sucesso!")
                return redirect('gerenciar_noticias') # Volta para a lista
            
        elif acao == 'editar' and noticia:
            titulo = request.POST.get('titulo')
            conteudo = request.POST.get('conteudo')

            # Validação Manual
            if not titulo or len(titulo.strip()) == 0:
                erros['titulo'] = "O Título é obrigatório."
            if not conteudo or len(conteudo.strip()) == 0:
                erros['conteudo'] = "O Conteúdo é obrigatório."

            if not erros:
                noticia.titulo = titulo
                noticia.conteudo = conteudo
                noticia.save()
                messages.success(request, f"Notícia '{noticia.titulo}' atualizada com sucesso!")
                return redirect('gerenciar_noticias', pk=noticia.pk, acao='detalhe')
            
        elif acao == 'excluir' and noticia:
            titulo_excluido = noticia.titulo
            noticia.delete()
            messages.success(request, f"Notícia '{titulo_excluido}' excluída com sucesso.")
            return redirect('gerenciar_noticias') # Volta para a lista
        
        if erros:
            messages.error(request, f"Falha na ação '{acao}'. Verifique os erros.")


    # 3. LÓGICA DO GET (Exibir Formulários ou Lista)
    
    # Prepara o contexto para formulários (se houver erros ou for GET)
    titulo_input = request.POST.get('titulo')
    conteudo_input = request.POST.get('conteudo')
    
    if acao == 'editar' and noticia and not erros:
        # Preenche com dados da notícia se for GET
        titulo_input = noticia.titulo
        conteudo_input = noticia.conteudo
    
    # Define o título da página e carrega dados
    if acao == 'lista':
        titulo_pagina = "Todas as Notícias"
        noticias = Noticia.objects.all()
    elif acao == 'adicionar':
        titulo_pagina = "Adicionar Nova Notícia"
        noticias = Noticia.objects.all()[:5] # Apenas para referência lateral
    elif acao == 'detalhe' and noticia:
        titulo_pagina = noticia.titulo
    elif acao == 'editar' and noticia:
        titulo_pagina = f"Editar: {noticia.titulo}"
    elif acao == 'excluir' and noticia:
        titulo_pagina = f"Confirmar Exclusão: {noticia.titulo}"
    else:
        titulo_pagina = "Gerenciar Notícias"
        
    context = {
        'acao': acao,          # 'lista', 'adicionar', 'detalhe', 'editar', 'excluir'
        'pk': pk,              # ID da notícia atual
        'titulo_pagina': titulo_pagina,
        'noticia': noticia,    # Notícia específica (para detalhe, edição, exclusão)
        'noticias': noticias if acao == 'lista' else None, # Lista de notícias (só para 'lista')
        
        # Variáveis para o formulário (preenchimento automático e erros)
        'erros': erros,
        'titulo_input': titulo_input,
        'conteudo_input': conteudo_input,
    }
    
    return render(request, 'gerente_condominio/ver_noticias.html', context)

@login_required
def ver_inquilinos(request):
    if not request.user.groups.filter(name='Gerente').exists():
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
        return redirect('login')
    inquilinos = Inquilino.objects.all()
    casas = Casa.objects.all()
    return render(request, 'gerente_condominio/ver_inquilino.html', {'inquilinos': inquilinos, 'casas': casas})

@login_required
def ver_casas(request):
    if not request.user.groups.filter(name='Gerente').exists():
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
        return redirect('login')
    casas = Casa.objects.all()
    return render(request, 'gerente_condominio/ver_casa.html', {'casas': casas})

@login_required
def ver_contratos(request):
    if not request.user.groups.filter(name='Gerente').exists():
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
        return redirect('login')
    contratos = Contrato.objects.all()
    inquilinos = Inquilino.objects.all()
    casas = Casa.objects.all()
    available_casas = Casa.objects.filter(inquilino__isnull=True)
    return render(request, 'gerente_condominio/ver_contratos.html', {'contratos': contratos, 'inquilinos': inquilinos, 'casas': casas, 'available_casas': available_casas})


@login_required
def ver_empresas(request):
    if not request.user.groups.filter(name='Gerente').exists():
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
        return redirect('login')
    empresas = Empresa.objects.all()
    return render(request, 'gerente_condominio/ver_empresas.html', {'empresas': empresas})


# --- AJAX Views para CRUD de Inquilinos ---

def add_inquilino(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        contacto = request.POST.get('contacto')
        ramo = request.POST.get('ramo')
        inquilino = Inquilino.objects.create(nome=nome, email=email, contacto=contacto, ramo=ramo)

        # Create Django user for the inquilino
        username = email  # Use email as username
        password = 'password123'  # Default password, should be changed later
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': email, 'first_name': nome}
        )
        if created:
            user.set_password(password)
            user.save()
            # Add to Inquilino group
            inquilino_group, _ = Group.objects.get_or_create(name='Inquilino')
            user.groups.add(inquilino_group)

        messages.success(request, f'Inquilino adicionado com sucesso! Usuário criado: {username} (senha: {password})')
        return redirect('ver_inquilinos')
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def edit_inquilino(request, pk):
    inquilino = get_object_or_404(Inquilino, pk=pk)
    if request.method == 'POST':
        inquilino.nome = request.POST.get('nome')
        inquilino.email = request.POST.get('email')
        inquilino.contacto = request.POST.get('contacto')
        inquilino.ramo = request.POST.get('ramo')
        inquilino.save()
        messages.success(request, 'Inquilino editado com sucesso!')
        return redirect('ver_inquilinos')
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def delete_inquilino(request, pk):
    inquilino = get_object_or_404(Inquilino, pk=pk)
    # Remove inquilino from casa
    Casa.objects.filter(inquilino=inquilino).update(inquilino=None)
    inquilino.delete()
    messages.success(request, 'Inquilino deletado com sucesso!')
    return JsonResponse({'success': True})

# --- AJAX Views para CRUD de Casas ---

def add_casa(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        Casa.objects.create(numero=numero)
        messages.success(request, 'Casa adicionada com sucesso!')
        return redirect('/gerente/ver-casas/')
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
def edit_casa(request, pk):
    if not request.user.groups.filter(name='Gerente').exists():
        messages.error(request, 'Acesso negado. Você não tem permissão para acessar esta página.')
        return redirect('login')
    casa = get_object_or_404(Casa, pk=pk)
    if request.method == 'POST':
        casa.numero = request.POST.get('numero')
        casa.save()
        messages.success(request, 'Casa editada com sucesso!')
        return redirect('/gerente/ver-casas/')
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
@csrf_exempt
def delete_casa(request, pk):
    if not request.user.groups.filter(name='Gerente').exists():
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
    casa = get_object_or_404(Casa, pk=pk)
    casa.delete()
    messages.success(request, 'Casa deletada com sucesso!')
    return JsonResponse({'success': True})

# --- AJAX Views para CRUD de Contratos ---

@csrf_exempt
def add_contrato(request):
    if request.method == 'POST':
        inquilino_id = request.POST.get('inquilino')
        casa_id = request.POST.get('casa')
        duracao_meses = request.POST.get('duracao')
        valor_renda = request.POST.get('valor_renda')
        inquilino = get_object_or_404(Inquilino, pk=inquilino_id)
        casa = get_object_or_404(Casa, pk=casa_id)
        Contrato.objects.create(
            inquilino=inquilino,
            casa=casa,
            duracao_meses=duracao_meses,
            valor_renda=valor_renda
        )
        messages.success(request, 'Contrato adicionado com sucesso!')
        return redirect('ver_contratos')
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def edit_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    if request.method == 'POST':
        contrato.inquilino = get_object_or_404(Inquilino, pk=request.POST.get('inquilino'))
        contrato.casa = get_object_or_404(Casa, pk=request.POST.get('casa'))
        contrato.duracao_meses = request.POST.get('duracao')
        contrato.valor_renda = request.POST.get('valor_renda')
        contrato.save()
        messages.success(request, 'Contrato editado com sucesso!')
        return redirect('ver_contratos')
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@csrf_exempt
def delete_contrato(request, pk):
    contrato = get_object_or_404(Contrato, pk=pk)
    contrato.delete()
    messages.success(request, 'Contrato deletado com sucesso!')
    return redirect('ver_contratos')

# --- AJAX Views para CRUD de Manutenções ---

def ver_manutencoes(request):
    """
    Exibe a lista de manutenções gerais e específicas.
    Os dados necessários para os formulários de criação/edição são passados no contexto.
    """
    # Busca os dados para popular as tabelas e os selects do modal
    manutencoes_gerais = ManutencaoGeral.objects.all().order_by('-data_abertura')
    manutencoes_especificas = ManutencaoEspecifica.objects.all().order_by('-data_abertura')
    empresas = Empresa.objects.all()
    casas = Casa.objects.all()

    context = {
        'manutencoes_gerais': manutencoes_gerais,
        'manutencoes_especificas': manutencoes_especificas,
        'empresas': empresas,
        'casas': casas,
    }
    
    return render(request, 'gerente_condominio/ver_manutencoes.html', context)

def add_manutencao(request):
    """
    Adiciona uma nova Manutenção Geral ou Específica, incluindo o upload de arquivos.
    """
    if request.method == 'POST':
        with transaction.atomic():
            try:
                # 1. Captura os dados comuns
                classe_manutencao = request.POST.get('classe_manutencao') # 'geral' ou 'especifica'
                empresa_id = request.POST.get('empresa')
                descricao = request.POST.get('descricao')

                # NOVIDADE 1: Captura o arquivo da foto de evidência (campo único)
                foto_evidencia = request.FILES.get('foto_evidencia') 
                
                # Captura a lista de anexos genéricos (se o modelo AnexoManutencao estiver em uso)
                anexos_uploaaded = request.FILES.getlist('anexos') 

                # Validação básica de empresa
                if not empresa_id:
                    messages.error(request, "Selecione uma empresa executora.")
                    return redirect('ver_manutencoes')
                
                empresa = get_object_or_404(Empresa, id=empresa_id)
                nova_manutencao = None

                # 2. Lógica de Decisão e Criação da Manutenção
                # Adicionamos 'foto_evidencia' diretamente no .create() se a foto existir
                
                common_fields = {
                    'empresa': empresa,
                    'descricao': descricao,
                    'foto_evidencia': foto_evidencia if foto_evidencia else None # Passa o arquivo se existir
                }

                if classe_manutencao == 'geral':
                    # Captura campos específicos de GERAL
                    tipo_geral = request.POST.get('tipo_geral')
                    problema = request.POST.get('problema')
                    
                    # Cria o objeto Manutenção Geral
                    nova_manutencao = ManutencaoGeral.objects.create(
                        **common_fields,
                        tipo=tipo_geral,
                        problema=problema
                    )
                    messages.success(request, "Manutenção Geral criada com sucesso!")

                elif classe_manutencao == 'especifica':
                    # Captura campos específicos de ESPECÍFICA
                    casa_id = request.POST.get('casa')
                    tipo_especifico = request.POST.get('tipo_especifico')
                    componente = request.POST.get('componente')
                    local_afetado = request.POST.get('local_afetado')

                    if not casa_id:
                        messages.error(request, "Para manutenção específica, é necessário selecionar uma Casa.")
                        return redirect('ver_manutencoes')

                    casa = get_object_or_404(Casa, id=casa_id)

                    # Cria o objeto Manutenção Específica
                    nova_manutencao = ManutencaoEspecifica.objects.create(
                        **common_fields,
                        casa=casa,
                        tipo=tipo_especifico,
                        componente=componente,
                        local_afetado=local_afetado
                    )
                    messages.success(request, "Manutenção Específica criada com sucesso!")
                
                else:
                    messages.error(request, "Tipo de manutenção inválido.")
                    return redirect('ver_manutencoes')
                
                # 3. Lógica para Processar Anexos Genéricos (Se o modelo AnexoManutencao existir)
                # Esta lógica foi mantida do seu código original
                if nova_manutencao and anexos_uploaaded:
                    anexos_criados = 0
                    # Itere e crie AnexoManutencao (Assumindo que o modelo AnexoManutencao está definido)
                    # Exemplo:
                    # from .models import AnexoManutencao 
                    # for f in anexos_uploaaded:
                    #     AnexoManutencao.objects.create(manutencao=nova_manutencao, arquivo=f)
                    #     anexos_criados += 1
                    
                    if anexos_criados > 0:
                        messages.info(request, f"{anexos_criados} anexo(s) adicional(is) adicionado(s) com sucesso.")

            except Exception as e:
                messages.error(request, f"Erro ao criar manutenção ou anexar arquivos: {str(e)}. A operação foi cancelada.")
                
            return redirect('ver_manutencoes')

    # Se tentar acessar via GET, redireciona para a lista
    return redirect('ver_manutencoes')

# 1. API para buscar dados (GET) - Usada pelo JavaScript
def get_detalhes_manutencao(request, tipo, id):
    """
    Retorna os detalhes de uma manutenção em formato JSON.
    Inclui a URL da 'foto_evidencia' e outros anexos para exibição no modal de edição.
    """
    try:
        data = {}
        # 1. Determina o modelo e busca o objeto
        if tipo == 'geral':
            obj = get_object_or_404(ManutencaoGeral, id=id)
        elif tipo == 'especifica':
            obj = get_object_or_404(ManutencaoEspecifica, id=id)
        else:
            return JsonResponse({'error': 'Tipo de manutenção inválido'}, status=400)
        
        # 2. Lógica Comum para Serializar Anexos (Mantido do seu código original)
        anexos_data = []
        # if hasattr(obj, 'anexos'): # Verifica se existe o GenericRelation 'anexos'
        #     for anexo in obj.anexos.all():
        #         anexos_data.append({
        #             'nome': anexo.arquivo.name.split('/')[-1], 
        #             'url': anexo.arquivo.url, 
        #             'id': anexo.id, 
        #         })

        # NOVIDADE 2: Adiciona a URL da foto de evidência ao JSON
        foto_evidencia_url = obj.foto_evidencia.url if obj.foto_evidencia else None
        
        # 3. Adiciona os campos comuns da Manutenção ao 'data'
        data = {
            'id': obj.id,
            'codigo': obj.codigo,
            'empresa': obj.empresa.id,
            'descricao': obj.descricao,
            'estado': obj.estado, # Adicionado: é útil para edição
            'data_abertura': obj.data_abertura.strftime("%Y-%m-%d %H:%M"), # Adicionado: útil para exibição
            'tipo_manutencao': tipo,
            'foto_evidencia_url': foto_evidencia_url, # <-- CAMPO NOVO
            'anexos_existentes': anexos_data, 
        }
        
        # 4. Adiciona campos específicos por tipo
        if tipo == 'geral':
            data.update({
                'tipo_categoria': obj.tipo,
                'sub_item': obj.problema,
            })
        elif tipo == 'especifica':
            data.update({
                'casa': obj.casa.id,
                'local_afetado': obj.local_afetado,
                'tipo_categoria': obj.tipo,
                'sub_item': obj.componente,
            })

        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# 2. View para Salvar a Edição (POST)
def editar_manutencao(request, tipo, id):
    """
    Edita uma Manutenção Geral ou Específica.
    """
    if request.method == 'POST':
        with transaction.atomic():
            try:
                empresa = get_object_or_404(Empresa, id=request.POST.get('empresa'))
                descricao = request.POST.get('descricao')
                estado = request.POST.get('estado') # O estado é provavelmente atualizável
                
                # NOVIDADE 3: Captura o novo arquivo da foto de evidência
                nova_foto_evidencia = request.FILES.get('foto_evidencia') 
                
                # Captura a lista de novos anexos genéricos
                anexos_uploaaded = request.FILES.getlist('anexos') 
                
                manutencao = None

                if tipo == 'geral':
                    manutencao = get_object_or_404(ManutencaoGeral, id=id)
                    manutencao.tipo = request.POST.get('tipo_geral')
                    manutencao.problema = request.POST.get('problema')
                    messages.success(request, "Manutenção Geral atualizada!")

                elif tipo == 'especifica':
                    manutencao = get_object_or_404(ManutencaoEspecifica, id=id)
                    manutencao.casa_id = request.POST.get('casa')
                    manutencao.tipo = request.POST.get('tipo_especifico')
                    manutencao.componente = request.POST.get('componente')
                    manutencao.local_afetado = request.POST.get('local_afetado')
                    messages.success(request, "Manutenção Específica atualizada!")
                
                else:
                    messages.error(request, "Tipo de manutenção inválido.")
                    return redirect('ver_manutencoes')

                # Campos comuns atualizados
                manutencao.empresa = empresa
                manutencao.descricao = descricao
                manutencao.estado = estado # Atualiza o estado

                # NOVIDADE 4: Lógica para a foto de evidência
                if nova_foto_evidencia:
                    # Se um novo arquivo foi enviado, substitui o antigo
                    manutencao.foto_evidencia = nova_foto_evidencia
                
                # Se houver um campo para DELETAR a foto existente, a lógica entraria aqui. 
                # Por exemplo: if request.POST.get('apagar_foto_evidencia') == 'on': manutencao.foto_evidencia = None

                manutencao.save() # Salva as alterações, incluindo o novo arquivo, se houver.
                
                # Lógica para Processar NOVOS Anexos Genéricos (Mantido)
                if anexos_uploaaded:
                    anexos_criados = 0
                    # Itere e crie AnexoManutencao (Assumindo que o modelo AnexoManutencao está definido)
                    # for f in anexos_uploaaded:
                    #     AnexoManutencao.objects.create(manutencao=manutencao, arquivo=f)
                    #     anexos_criados += 1
                    
                    if anexos_criados > 0:
                        messages.info(request, f"Edição concluída! {anexos_criados} novo(s) anexo(s) adicionado(s).")
                
            except Exception as e:
                messages.error(request, f"Erro ao editar e/ou anexar arquivos: {str(e)}. A operação foi cancelada.")

        return redirect('ver_manutencoes')
    
    return redirect('ver_manutencoes')

@require_POST
def excluir_manutencao(request, tipo, id):
    """
    Exclui uma manutenção (Geral ou Específica) com base no tipo e ID.
    Requer requisição POST.
    """
    if tipo == 'geral':
        modelo = ManutencaoGeral
        nome_tipo = "Manutenção Geral"
    elif tipo == 'especifica':
        modelo = ManutencaoEspecifica
        nome_tipo = "Manutenção Específica"
    else:
        messages.error(request, "Tipo de manutenção inválido.")
        return redirect('ver_manutencoes')
    
    try:
        manutencao = get_object_or_404(modelo, id=id)
        
        # Salva o código antes de deletar para usar na mensagem
        codigo_manutencao = manutencao.codigo 
        
        manutencao.delete()
        messages.success(request, f"{nome_tipo} ({codigo_manutencao}) excluída com sucesso.")
    
    except Exception as e:
        messages.error(request, f"Erro ao excluir manutenção: {e}")

    return redirect('ver_manutencoes')

# --- AJAX Views para CRUD de Empresas (COM CORREÇÃO DE SEGURANÇA E ERRO) ---

@login_required
@csrf_exempt
def add_empresa(request):
    if not request.user.groups.filter(name='Gerente').exists():
        logger.warning(f"Tentativa de acesso não autorizado a add_empresa por {request.user.username}")
        return JsonResponse({'error': 'Acesso negado. Apenas Gerentes podem adicionar empresas.'}, status=403)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            Empresa.objects.create(
                nome=data['nome'],
                telefone=data.get('telefone', ''),
                email=data.get('email', ''),
                provincia=data.get('provincia', ''),
                endereco=data.get('endereco', ''),
                servicos=data.get('servicos', ''),
                observacoes=data.get('observacoes', '')
            )
            logger.info(f"Empresa '{data['nome']}' adicionada com sucesso.")
            return JsonResponse({'success': True, 'message': 'Empresa adicionada com sucesso!'})
        except Exception as e:
            # ESTE PODE SER O SEU PROBLEMA: um erro de banco de dados ou de JSON que não está sendo visto.
            logger.error(f"Erro crítico ao adicionar empresa (JSON/DB Error): {e}")
            return JsonResponse({'error': f'Erro interno ao salvar a empresa: {str(e)}'}, status=500)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
@csrf_exempt
def edit_empresa(request, pk):
    if not request.user.groups.filter(name='Gerente').exists():
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
        
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            empresa.nome = data['nome']
            empresa.telefone = data.get('telefone', '')
            empresa.email = data.get('email', '')
            empresa.provincia = data.get('provincia', '')
            empresa.endereco = data.get('endereco', '')
            empresa.servicos = data.get('servicos', '')
            empresa.observacoes = data.get('observacoes', '')
            empresa.save()
            logger.info(f"Empresa '{empresa.nome}' (ID: {pk}) editada com sucesso.")
            return JsonResponse({'success': True, 'message': 'Empresa editada com sucesso!'})
        except Exception as e:
            logger.error(f"Erro crítico ao editar empresa ID {pk}: {e}")
            return JsonResponse({'error': f'Erro interno ao salvar a empresa: {str(e)}'}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required
@csrf_exempt
def delete_empresa(request, pk):
    if not request.user.groups.filter(name='Gerente').exists():
        return JsonResponse({'error': 'Acesso negado.'}, status=403)
        
    empresa = get_object_or_404(Empresa, pk=pk)
    try:
        empresa.delete()
        logger.info(f"Empresa (ID: {pk}) deletada com sucesso.")
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Erro ao deletar empresa ID {pk}: {e}")
        return JsonResponse({'error': 'Erro ao deletar a empresa.'}, status=500)

# --- Views de Obtenção de Dados (AJAX) ---

def get_empresas(request):
    # Geralmente não precisa de login, mas se for para uso interno:
    # if not request.user.groups.filter(name='Gerente').exists():
    #     return JsonResponse({'error': 'Acesso negado.'}, status=403)
    empresas = list(Empresa.objects.values('id', 'nome', 'telefone', 'email', 'provincia', 'endereco', 'servicos', 'observacoes'))
    return JsonResponse({'empresas': empresas})

def get_condominios(request):
    condominios = list(Condominio.objects.values('id', 'nome'))
    return JsonResponse({'condominios': condominios})

def get_casas(request):
    condominio_id = request.GET.get('condominio_id')
    if condominio_id:
        casas = list(Casa.objects.filter(condominio_id=condominio_id).values('id', 'numero'))
    else:
        casas = list(Casa.objects.values('id', 'numero'))
    return JsonResponse({'casas': casas})

def get_inquilinos(request):
    inquilinos = list(Inquilino.objects.values('id', 'nome'))
    return JsonResponse({'inquilinos': inquilinos})

def get_historico_empresa(request, empresa_id):
    historicos = list(HistoricoEmpresa.objects.filter(empresa_id=empresa_id).values('data', 'servico', 'local', 'custo', 'estado'))
    return JsonResponse({'historico': historicos})

def welcome(request):
    logger.info(f"Request received: {request.method} {request.path}")
    return JsonResponse({'message': 'Welcome to the Condominium Management System!'})