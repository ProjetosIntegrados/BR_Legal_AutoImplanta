from pathlib import Path
from typing import Any, Optional
from .coordenadas import ConversorCoordenadas

from openpyxl import load_workbook

from .enums import *
from .placa import Placa


class LeitorCadastroVertical:
    """Lê arquivos de cadastro e de necessidades de sinalização vertical."""

    LINHA_CABECALHO = 2
    PRIMEIRA_LINHA_DADOS = 3

    def __init__(self, caminho: str):
        self.caminho = Path(caminho)

    def ler(self) -> list[Placa]:
        """Retorna as placas cadastradas na planilha ativa do workbook."""

        placas: list[Placa] = []

        # Abre a planilha em modo de leitura somente para ler os dados sem alterar o arquivo.
        # A opção data_only=True garante que valores calculados sejam lidos como seus resultados finais.
        workbook = load_workbook(
            self.caminho,
            read_only=True,
            data_only=True,
            keep_vba=True,
        )

        try:
            # Usa a primeira aba ativa do workbook como fonte de dados do cadastro.
            planilha = workbook.active
            # Mapeia nome da coluna para sua posição na linha de cabeçalho.
            indices = self._obter_indices(planilha)

            # Itera sobre todas as linhas de dados, começando na primeira linha útil.
            linhas_planilha = planilha.iter_rows(
                min_row=self.PRIMEIRA_LINHA_DADOS,
                values_only=True,
            )

            # Cada item da iteração representa uma linha da planilha com os valores das colunas.
            for numero_linha, valores in enumerate(linhas_planilha,start=self.PRIMEIRA_LINHA_DADOS,):
                try:
                    # Converte a linha em um objeto Placa, validando campos antes de adicionar.
                    placas.append(self._criar_placa(valores, indices))
                except (KeyError, TypeError, ValueError) as erro:
                    # Exibe apenas o problema da linha para não interromper a leitura do restante do arquivo.
                    print(f"Linha {numero_linha} ignorada: {erro}")
        finally:
            # Fecha o workbook para liberar o arquivo.
            workbook.close()

        return placas

    def _obter_indices(self, planilha) -> dict[str, int]:
        # Lê a linha de cabeçalho para identificar em que coluna cada campo está localizado.
        cabecalhos = next(
                planilha.iter_rows(
                min_row=self.LINHA_CABECALHO,
                max_row=self.LINHA_CABECALHO,
                values_only=True,
            )
        )

        # Cria um dicionário do formato: nome_da_coluna -> indice_da_coluna.
        por_nome = {}
        for indice, valor in enumerate(cabecalhos):
            por_nome[valor] = indice

        return por_nome

    def _criar_placa(self, valores, indices) -> Placa:
        # O lambda centraliza a leitura de cada campo pela chave do cabeçalho correspondente.
        valor = lambda campo: self._valor(valores, indices, campo)
        
        solucao = self._solucao_ou_padrao(valor("Solução"))
        motivo = self._motivo_ou_none(valor("Motivo"))
        posicao = Posicao(valor("Posição"))
        lado = Lado(valor("Lado"))
        quantidade_suporte = self._inteiro_ou_none(valor("Quantidade de Suporte"))
        tipo_secao_suporte = TipoSecaoSuporte(valor("Tipo de Seção de Suporte"))
        secao_suporte_mm = self._texto_ou_none(valor("Seção do Suporte (mm)")
)

        # Em placas aéreas, alguns campos deixam de ter sentido e são normalizados para valores não aplicáveis.
        if posicao == Posicao.AEREA:
            lado = Lado.NAO_APLICAVEL
            quantidade_suporte = None
            tipo_secao_suporte = TipoSecaoSuporte.NAO_APLICAVEL
            secao_suporte_mm = None

       
        km = float(valor("Km"))
        codigo_placa = str(valor("Código da Placa"))

        # Para placas do tipo MQ, o código é reconstruído
        # com base na quilometragem da instalação.
        if codigo_placa.startswith("MQ-"):
            codigo_placa = f"MQ-{round(km)}"

        # Leitura das coordenadas geográficas
        latitude = float(valor("Latitude"))
        longitude = float(valor("Longitude"))

        # Conversão para SIRGAS 2000 / UTM 22S
        x, y = ConversorCoordenadas.converter(
            latitude=latitude,
            longitude=longitude,
        )

        return Placa(
            br=str(valor("BR")),
            snv=str(valor("SNV")),
            tipo_placa=TipoPlaca(valor("Tipo de Placa")),
            codigo_placa=codigo_placa,
            velocidade=self._inteiro_ou_none(valor("Velocidade (km/h)")),
            lado=lado,
            posicao=posicao,
            km=km,
            latitude=latitude,
            longitude=longitude,
            x=x,
            y=y,
            detalhamento_pagina=self._inteiro_ou_none(valor("Detalhamento (página)")),
            tipo_suporte=TipoSuporte(valor("Tipo de Suporte")),
            quantidade_suporte=quantidade_suporte,
            tipo_secao_suporte=tipo_secao_suporte,
            secao_suporte_mm=secao_suporte_mm,
            tipo_substrato=str(valor("Tipo de Substrato")),
            si_sinal_impresso=SimNao(valor("SI (Sinal Impresso)")),
            tipo_pelicula_fundo=str(valor("Tipo (película fundo)")),
            cor_pelicula_fundo=str(valor("Cor (película fundo)")),
            retrorrefletancia_fundo=self._numero_ou_none(valor("Retrorrefletância (película fundo) (cd.lux/m-2)")),
            tipo_pelicula_legenda_orla=str(valor("Tipo (película legenda/orla)")),
            cor_pelicula_orla=str(valor("Cor (película/orla)")),
            retrorrefletancia_legenda_orla=self._numero_ou_none(valor("Retrorrefletância (película legenda/orla) (cd.lux/m-2)")),
            largura=float(valor("Largura (m)")),
            altura=self._numero_ou_none(valor("Altura (m)")),
            area=float(valor("Área (m²)")),
            solucao=solucao,
            motivo=motivo,
        )

    @staticmethod
    def _valor(valores, indices, campo):
        return valores[indices[campo]]

    @classmethod
    def _solucao_ou_padrao(cls, valor) -> Solucao:
        return Solucao.MANTER if cls._vazio(valor) else Solucao(valor)

    @staticmethod
    def _vazio(valor: Any) -> bool:
        return valor is None or str(valor).strip() in {"", "-"}

    @classmethod
    def _numero_ou_none(cls, valor: Any) -> Optional[float]:
        return None if cls._vazio(valor) else float(valor)

    @classmethod
    def _inteiro_ou_none(cls, valor: Any) -> Optional[int]:
        return None if cls._vazio(valor) else int(str(valor).replace("´", ""))

    @classmethod
    def _texto_ou_none(cls, valor: Any) -> Optional[str]:
        return None if cls._vazio(valor) else str(valor)

    @classmethod
    def _motivo_ou_none(cls, valor: Any) -> Optional[Motivo]:
        return None if cls._vazio(valor) else Motivo(int(valor))
