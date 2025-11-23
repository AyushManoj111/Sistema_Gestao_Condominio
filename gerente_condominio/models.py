from django.db import models
from datetime import date, timedelta
import datetime
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
# ... outras importações
# --- MODELOS DE BASE ---

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    # Você pode adicionar um campo para imagem de capa, se desejar
    # imagem_capa = models.ImageField(upload_to='noticias/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ['-data_publicacao'] # Para exibir as mais novas primeiro

    def __str__(self):
        return self.titulo

class Condominio(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Inquilino(models.Model):
    RAMO_CHOICES = [
        ("Comércio", "Comércio"),
        ("Serviços", "Serviços"),
        ("Outro", "Outro"),
    ]

    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contacto = models.CharField(max_length=20)
    ramo = models.CharField(max_length=20, choices=RAMO_CHOICES)

    def __str__(self):
        return self.nome


class Casa(models.Model):
    numero = models.CharField(max_length=20)
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, null=True, blank=True, related_name="casas")
    inquilino = models.OneToOneField(
        Inquilino,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="casa"
    )

    def __str__(self):
        if self.condominio:
            if self.inquilino:
                return f"{self.condominio.nome} - Casa {self.numero} ({self.inquilino.nome})"
            return f"{self.condominio.nome} - Casa {self.numero} (Vaga)"
        else:
            if self.inquilino:
                return f"Casa {self.numero} ({self.inquilino.nome})"
            return f"Casa {self.numero} (Vaga)"


class Empresa(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    provincia = models.CharField(max_length=50, blank=True)
    endereco = models.TextField(blank=True)
    servicos = models.TextField(blank=True)
    observacoes = models.TextField(blank=True)

    def __str__(self):
        return self.nome


class HistoricoEmpresa(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="historicos")
    data = models.DateField()
    servico = models.CharField(max_length=200)
    local = models.CharField(max_length=200)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=[
        ("Concluído", "Concluído"),
        ("Em Progresso", "Em Progresso"),
        ("Pendente", "Pendente"),
        ("Cancelado", "Cancelado"),
    ])

    def __str__(self):
        return f"{self.empresa.nome} - {self.servico}"


class ManutencaoBase(models.Model):
    ESTADO_CHOICES = [
        ("Pendente", "Pendente"),
        ("Em Progresso", "Em Progresso"),
        ("Concluído", "Concluído"),
        ("Cancelado", "Cancelado"),
    ]

    codigo = models.CharField(max_length=20, unique=True, blank=True, editable=False)
    descricao = models.TextField()
    empresa = models.ForeignKey(
        'Empresa', 
        on_delete=models.CASCADE, 
        related_name="%(class)s_manutencoes" 
    )
    foto_evidencia = models.ImageField(
        upload_to='manutencoes_evidencias/', 
        verbose_name='Foto de Evidência',
        null=True,  # Permite que o campo fique vazio
        blank=True
    )
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default="Pendente")
    data_abertura = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Só gera o código se ele ainda não existir (ou seja, na criação)
        if not self.codigo:
            year = datetime.date.today().year
            
            # Define o prefixo baseado na classe
            if isinstance(self, ManutencaoGeral):
                prefixo = "GER"
                classe_model = ManutencaoGeral
            else:
                prefixo = "ESP"
                classe_model = ManutencaoEspecifica
            
            # Conta quantos registros já existem para gerar o sequencial
            # Exemplo: Se já tem 5, o próximo será 6
            count = classe_model.objects.count() + 1
            
            # Formata: PREF-ANO-000X (Ex: GER-2024-0001)
            self.codigo = f"{prefixo}-{year}-{count:04d}"
            
        super().save(*args, **kwargs)


class ManutencaoGeral(ManutencaoBase):
    TIPO_GERAL_CHOICES = [
        ("equipamentos", "Equipamentos"),
        ("sistemas", "Sistemas"),
        ("estrutura-fisica", "Estrutura Física"),
    ]

    tipo = models.CharField(max_length=20, choices=TIPO_GERAL_CHOICES)
    problema = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Manutenção Geral"
        verbose_name_plural = "Manutenções Gerais"

    def __str__(self):
        return f"Geral - {self.codigo}"
    

class ManutencaoEspecifica(ManutencaoBase):
    TIPO_ESPECIFICO_CHOICES = [
        ("hidraulica", "Hidráulica"),
        ("eletrica", "Elétrica"),
        ("caixilharia", "Caixilharia"),
    ]

    # Campo CASA entra aqui, exclusivo para manutenção específica
    casa = models.ForeignKey(
        'Casa',
        on_delete=models.CASCADE,
        # Como não é herdado, podemos usar um nome fixo e claro
        related_name="manutencoes_especificas" 
    )
    
    tipo = models.CharField(max_length=20, choices=TIPO_ESPECIFICO_CHOICES)
    componente = models.CharField(max_length=50, null=True, blank=True)
    local_afetado = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Manutenção Específica"
        verbose_name_plural = "Manutenções Específicas"

    def __str__(self):
        return f"Específica - {self.casa} - {self.codigo}"


# --- MODELO PRINCIPAL DESTA PÁGINA ---

class Contrato(models.Model):
    DURATION_CHOICES = [
        (12, "12 meses"),
        (24, "24 meses"),
        (36, "36 meses"),
    ]

    inquilino = models.ForeignKey(Inquilino, on_delete=models.CASCADE, related_name="contratos")
    casa = models.ForeignKey(Casa, on_delete=models.CASCADE, related_name="contratos")
    data_inicio = models.DateField(default=date.today)
    duracao_meses = models.IntegerField(choices=DURATION_CHOICES)
    valor_renda = models.DecimalField(max_digits=10, decimal_places=2)

    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ["-data_criacao"]

    def __str__(self):
        return f"Contrato de {self.inquilino.nome} - Casa {self.casa.numero}"

    def save(self, *args, **kwargs):
        # Associar a casa ao inquilino quando o contrato é criado
        if not self.pk:  # Se é um novo contrato
            self.casa.inquilino = self.inquilino
            self.casa.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Desassociar a casa do inquilino quando o contrato é terminado
        self.casa.inquilino = None
        self.casa.save()
        super().delete(*args, **kwargs)

    # --- Métodos úteis para o template ---
    @property
    def data_fim(self):
        """Data final estimada do contrato"""
        return self.data_inicio + timedelta(days=self.duracao_meses * 30)

    @property
    def duracao_restante(self):
        """Duração restante em meses"""
        meses_restantes = (self.data_fim.year - date.today().year) * 12 + (self.data_fim.month - date.today().month)
        return max(0, meses_restantes)
