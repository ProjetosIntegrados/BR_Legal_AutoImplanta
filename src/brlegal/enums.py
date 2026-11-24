from enum import Enum


class TipoPlaca(str, Enum):
    REGULAMENTACAO = "Regulamentação"
    ADVERTENCIA = "Advertência"
    INDICACAO = "Indicação"


class SubgrupoPlaca(str, Enum):
    # Regulamentação
    REGULAMENTACAO_SIMPLES = "Simples"
    REGULAMENTACAO_COMPOSTA = "Compostas"

    # Advertência
    ADVERTENCIA_SIMPLES = "Simples"
    ADVERTENCIA_COMPOSTA = "Compostas"
    MARCADOR_ALINHAMENTO = "Marcador de alinhamento (delineador)"
    MARCADOR_OBSTACULO = "Marcador de obstáculo"
    MARCADOR_PERIGO = "Marcador de perigo"

    # Indicação
    DISTANCIA_SENTIDO = "Distância, sentido"
    SERVICOS_AUXILIARES = "Serviços auxiliares"
    TURISTICA = "Turística"
    EDUCATIVA = "Educativa"
    MARCO_QUILOMETRICO = "Marco quilométrico"
    PLACA_INSTITUCIONAL = "Placa institucional"
    BRASAO_RODOVIA = "Brasão de rodovia"


class Lado(str, Enum):
    DIREITO = "D"
    ESQUERDO = "E"
    NAO_APLICAVEL = "-"


class Posicao(str, Enum):
    TERRESTRE = "Terrestre"
    AEREA = "Aérea"


class TipoSuporte(str, Enum):
    MADEIRA = "Madeira"
    POLIMERICO = "Polimérico"
    METALICO = "Metálico"
    PORTICO = "Pórtico"
    SEMIPORTICO = "Semipórtico"
    BRACO_PROJETADO = "Braço projetado"
    FIXADA_EM = "Placas fixadas em (viaduto, passarela, poste e outros)"


class TipoSecaoSuporte(str, Enum):
    PERFIL_C = "Perfil C"
    CIRCULAR = "Circular"
    RETANGULAR = "Retangular"
    QUADRADA = "Quadrada"
    NAO_APLICAVEL = "-"


class SimNao(str, Enum):
    SIM = "SIM"
    NAO = "NÃO"


class Solucao(str, Enum):
    MANTER = "Manter"
    REMOVER = "Remover"
    IMPLANTAR = "Implantar"
    SUBSTITUIR = "Substituir"


class Motivo(int, Enum):
    PLACA_NAO_RETRORREFLETIVA = 1
    DIAGRAMACAO_INCORRETA = 2
    PLACA_DANIFICADA = 3
    SUPORTE_DANIFICADO = 4
    LOCAL_IMPROPRIO = 5
    ADEQUACAO_IMEDIATA = 6
