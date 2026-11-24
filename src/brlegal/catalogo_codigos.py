import re
from typing import Optional

from .enums import TipoPlaca
from .erros import ErroPlaca


class CatalogoCodigos:
    """
    Regras do dicionário de códigos das placas.

    Os códigos são classificados em:
        - Manual: código definido pelo Manual Brasileiro.
        - Sequencial: número crescente de implantação.
        - Quilometrico: código derivado do KM.
    """

    REGRAS = {
        "R": {"tipo": TipoPlaca.REGULAMENTACAO, "subgrupo": "Simples", "padrao": r"R-\d+[A-Za-z]?", "categoria": "manual"},
        "RM": {"tipo": TipoPlaca.REGULAMENTACAO, "subgrupo": "Compostas", "padrao": r"RM-\d+", "categoria": "sequencial"},
        "A": {"tipo": TipoPlaca.ADVERTENCIA, "subgrupo": "Simples", "padrao": r"A-\d+[A-Za-z]?", "categoria": "manual"},
        "AM": {"tipo": TipoPlaca.ADVERTENCIA, "subgrupo": "Compostas", "padrao": r"AM-\d+", "categoria": "sequencial"},
        "MA": {"tipo": TipoPlaca.ADVERTENCIA, "subgrupo": "Marcador de alinhamento (delineador)", "padrao": r"MA-\d+", "categoria": "sequencial"},
        "MO": {"tipo": TipoPlaca.ADVERTENCIA, "subgrupo": "Marcador de obstáculo", "padrao": r"MO-\d+", "categoria": "sequencial"},
        "MP": {"tipo": TipoPlaca.ADVERTENCIA, "subgrupo": "Marcador de perigo", "padrao": r"MP-\d+", "categoria": "sequencial"},
        "I": {"tipo": TipoPlaca.INDICACAO, "subgrupo": "Distância, sentido", "padrao": r"I-\d+", "categoria": "sequencial"},
        "S": {"tipo": TipoPlaca.INDICACAO, "subgrupo": "Serviços auxiliares", "padrao": r"S-\d+", "categoria": "sequencial"},
        "T": {"tipo": TipoPlaca.INDICACAO, "subgrupo": "Turística", "padrao": r"T-\d+", "categoria": "sequencial"},
        "E": {"tipo": TipoPlaca.INDICACAO, "subgrupo": "Educativa", "padrao": r"E-\d+", "categoria": "sequencial"},
        "MQ": {"tipo": TipoPlaca.INDICACAO, "subgrupo": "Marco quilométrico", "padrao": r"MQ-\d+", "categoria": "quilometrico"},
        "PI": {"tipo": TipoPlaca.INDICACAO, "subgrupo": "Placa institucional", "padrao": r"PI-\d+", "categoria": "sequencial"},
        "B": {"tipo": TipoPlaca.INDICACAO, "subgrupo": "Brasão de rodovia", "padrao": r"B-\d+", "categoria": "sequencial"},
    }

    @classmethod
    def obter_prefixo(cls, codigo: str) -> str:
        if "-" not in codigo:
            raise ErroPlaca(f"Código inválido: '{codigo}'.")
        return codigo.split("-")[0]

    @classmethod
    def obter_regra(cls, codigo: str) -> dict:
        prefixo = cls.obter_prefixo(codigo)
        if prefixo not in cls.REGRAS:
            raise ErroPlaca(f"Prefixo de placa não reconhecido: '{prefixo}'.")
        return cls.REGRAS[prefixo]

    @classmethod
    def validar(cls, codigo: str, tipo_placa: TipoPlaca, km: Optional[float] = None):
        regra = cls.obter_regra(codigo)

        if regra["tipo"] != tipo_placa:
            raise ErroPlaca(
                f"O código '{codigo}' não pertence ao tipo '{tipo_placa.value}'."
            )

        if not re.fullmatch(regra["padrao"], codigo):
            raise ErroPlaca(f"Código '{codigo}' não possui o formato esperado.")

        if regra["categoria"] == "quilometrico":
            if km is None:
                raise ErroPlaca("Código MQ requer o KM da placa.")

            km_inteiro = int(round(km))
            codigo_esperado = f"MQ-{km_inteiro}"
            if codigo != codigo_esperado:
                raise ErroPlaca(
                    f"Código de marco quilométrico inválido. "
                    f"Para KM {km:.2f}, o código esperado é '{codigo_esperado}'."
                )
