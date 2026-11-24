from dataclasses import dataclass
import re
from typing import Optional

from .catalogo_codigos import CatalogoCodigos
from .enums import *
from .erros import ErroPlaca


# ============================================================
# CLASSE PLACA
# ============================================================

@dataclass
class Placa:

    # --------------------------------------------------------
    # Identificação
    # --------------------------------------------------------

    br: str
    snv: str
    tipo_placa: TipoPlaca
    codigo_placa: str

    # --------------------------------------------------------
    # Localização
    # --------------------------------------------------------

    velocidade: Optional[int]
    lado: Lado
    posicao: Posicao

    km: float
    latitude: float
    longitude: float

    detalhamento_pagina: Optional[int]

    # --------------------------------------------------------
    # Suporte
    # --------------------------------------------------------

    tipo_suporte: TipoSuporte
    quantidade_suporte: Optional[int]
    tipo_secao_suporte: TipoSecaoSuporte
    secao_suporte_mm: Optional[str]

    # --------------------------------------------------------
    # Substrato
    # --------------------------------------------------------

    tipo_substrato: str
    si_sinal_impresso: SimNao

    # --------------------------------------------------------
    # Película
    # --------------------------------------------------------

    tipo_pelicula_fundo: str
    cor_pelicula_fundo: str
    retrorrefletancia_fundo: Optional[float]

    tipo_pelicula_legenda_orla: str
    cor_pelicula_orla: str
    retrorrefletancia_legenda_orla: Optional[float]

    # --------------------------------------------------------
    # Dimensões
    # --------------------------------------------------------

    largura: float
    altura: Optional[float]
    area: float

    # --------------------------------------------------------
    # Solução
    # --------------------------------------------------------

    solucao: Solucao
    motivo: Optional[Motivo]

    
    # --------------------------------------------------------
    # Validação
    # --------------------------------------------------------

    def __post_init__(self):
        self._validar_identificacao()
        self._validar_codigo()
        self._validar_velocidade()
        self._validar_localizacao()
        self._validar_suporte()
        self._validar_substrato()
        self._validar_pelicula()
        self._validar_dimensoes()
        self._validar_solucao()

    # ========================================================
    # IDENTIFICAÇÃO
    # ========================================================

    def _validar_identificacao(self):
        if not re.fullmatch(r"BR-\d{3}", self.br):
            raise ErroPlaca(
                f"BR inválida: '{self.br}'. "
                "Utilize BR-XXX."
            )

        if not self.snv:
            raise ErroPlaca("SNV não pode ser vazio.")

        if not self.codigo_placa:
            raise ErroPlaca(
                "Código da placa não pode ser vazio."
            )

    # ========================================================
    # CÓDIGO
    # ========================================================

    def _validar_codigo(self):
        CatalogoCodigos.validar(
            codigo=self.codigo_placa,
            tipo_placa=self.tipo_placa,
            km=self.km,
        )

    # ========================================================
    # VELOCIDADE
    # ========================================================

    def _validar_velocidade(self):
        eh_r19 = self.codigo_placa == "R-19"

        if eh_r19:

            if self.velocidade is None:
                raise ErroPlaca(
                    "R-19 deve possuir velocidade."
                )

            if not isinstance(self.velocidade, int):
                raise ErroPlaca(
                    "Velocidade deve ser um número inteiro."
                )

            if self.velocidade <= 0:
                raise ErroPlaca(
                    "Velocidade deve ser maior que zero."
                )

        else:

            if self.velocidade is not None:
                raise ErroPlaca(
                    "Velocidade só pode ser preenchida para R-19."
                )

    # ========================================================
    # LOCALIZAÇÃO
    # ========================================================

    def _validar_localizacao(self):
        if self.km < 0:
            raise ErroPlaca(
                "KM não pode ser negativo."
            )

        if not -90 <= self.latitude <= 90:
            raise ErroPlaca(
                f"Latitude inválida: {self.latitude}"
            )

        if not -180 <= self.longitude <= 180:
            raise ErroPlaca(
                f"Longitude inválida: {self.longitude}"
            )

        if self.detalhamento_pagina is not None:
            if not isinstance(
                self.detalhamento_pagina,
                int
            ):
                raise ErroPlaca(
                    "Página deve ser um número inteiro."
                )

    # ========================================================
    # SUPORTE
    # ========================================================

    def _validar_suporte(self):
        if self.posicao == Posicao.AEREA:

            if self.lado != Lado.NAO_APLICAVEL:
                raise ErroPlaca(
                    "Placas aéreas devem possuir lado '-'."
                )

            if self.quantidade_suporte is not None:
                raise ErroPlaca(
                    "Placas aéreas não devem possuir quantidade de suporte."
                )

            if self.tipo_secao_suporte != (
                TipoSecaoSuporte.NAO_APLICAVEL
            ):
                raise ErroPlaca(
                    "Placas aéreas devem possuir tipo de seção '-'."
                )

            if self.secao_suporte_mm is not None:
                raise ErroPlaca(
                    "Placas aéreas devem possuir seção '-'."
                )
            
        else:
            if self.quantidade_suporte is None:
                raise ErroPlaca(
                    "Placas terrestres devem informar a quantidade de suportes."
                )

            if self.quantidade_suporte <= 0:
                raise ErroPlaca(
                    "Quantidade de suporte deve ser maior que zero."
                )

            if self.tipo_secao_suporte == (
                TipoSecaoSuporte.NAO_APLICAVEL
            ):
                raise ErroPlaca(
                    "Placas terrestres devem informar o tipo de seção."
                )

            if not self.secao_suporte_mm:
                raise ErroPlaca(
                    "Seção do suporte deve ser informada."
                )

        # Implantação não permite seção circular
        if (
            self.solucao == Solucao.IMPLANTAR
            and self.tipo_secao_suporte
            == TipoSecaoSuporte.CIRCULAR
        ):
            raise ErroPlaca(
                "Placas com solução 'Implantar' não podem utilizar seção circular."
            )

    # ========================================================
    # SUBSTRATO
    # ========================================================

    def _validar_substrato(self):
        if self.solucao == Solucao.IMPLANTAR:
            if self.tipo_substrato not in {
                "Aço",
                "ACM",
            }:
                raise ErroPlaca(
                    "Para 'Implantar', o substrato deve ser Aço ou ACM."
                )

    # ========================================================
    # PELÍCULA
    # ========================================================

    def _validar_pelicula(self):
        if self.solucao == Solucao.IMPLANTAR:
            if self.si_sinal_impresso != SimNao.SIM:
                raise ErroPlaca(
                    "Para 'Implantar', SI deve ser SIM."
                )

    # ========================================================
    # DIMENSÕES
    # ========================================================

    def _validar_dimensoes(self):
        if self.largura <= 0:
            raise ErroPlaca("Largura deve ser maior que zero.")

        # ----------------------------------------------------
        # Altura
        # ----------------------------------------------------

        if self.altura is not None:
            if self.altura <= 0:
                raise ErroPlaca("Altura deve ser maior que zero.")
            
            area_calculada = (
                self.largura * self.altura
            )

            if abs(
                self.area - area_calculada
            ) > 0.02:

                raise ErroPlaca(
                    f"Área inconsistente. "
                    f"Informada: {self.area:.2f}; "
                    f"calculada: {area_calculada:.2f}."
                )

        # ----------------------------------------------------
        # Área
        # ----------------------------------------------------

        if self.area <= 0:
            raise ErroPlaca(
                "Área deve ser maior que zero."
            )

    # ========================================================
    # SOLUÇÃO
    # ========================================================

    def _validar_solucao(self):

        if self.solucao in {
            Solucao.REMOVER,
            Solucao.SUBSTITUIR,
        }:

            if self.motivo is None:
                raise ErroPlaca(
                    f"A solução '{self.solucao.value}' exige um motivo."
                )

        else:

            if self.motivo is not None:
                raise ErroPlaca(
                    f"A solução '{self.solucao.value}' não deve possuir motivo."
                )

    
    def __str__(self) -> str:
        valores = ", ".join(
            f"{nome}={valor!r}" for nome, valor in vars(self).items()
        )
        return f"Placa({valores})"