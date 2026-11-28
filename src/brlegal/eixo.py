
from dataclasses import dataclass
from math import hypot, atan2, degrees, isfinite
from pathlib import Path

import ezdxf


CAMADA_PADRAO_EIXO = "BRLEGAL_EIXO"


@dataclass
class ResultadoProjecao:
    x: float
    y: float
    distancia: float
    angulo_graus: float
    indice_segmento: int


class EixoRodoviario:
    """
    Lê um eixo rodoviário representado por uma única polilinha
    contínua em um arquivo DXF.

    Entidades aceitas:
    - LWPOLYLINE
    - POLYLINE 2D

    A geometria deve estar em metros e no mesmo sistema de
    coordenadas utilizado pelas placas (EPSG:31982).
    """

    def __init__(
        self,
        caminho_dxf: str,
        camada_eixo: str = CAMADA_PADRAO_EIXO,
    ):
        self.caminho_dxf = Path(caminho_dxf)
        self.camada_eixo = camada_eixo.strip() if camada_eixo else CAMADA_PADRAO_EIXO

        self.documento = None
        self.modelspace = None
        self.eixo = None
        self.pontos = []

        self._carregar_dxf()
        self._localizar_eixo()
        self._extrair_pontos()
        self._validar_pontos()

    def _carregar_dxf(self):
        if not self.caminho_dxf.exists():
            raise FileNotFoundError(
                f"Arquivo DXF não encontrado: {self.caminho_dxf}"
            )

        try:
            self.documento = ezdxf.readfile(self.caminho_dxf)
            self.modelspace = self.documento.modelspace()

        except ezdxf.DXFStructureError as erro:
            raise ValueError(
                f"O arquivo DXF está inválido ou corrompido: {erro}"
            ) from erro

    def _localizar_eixo(self):
        camadas_existentes = {
            camada.dxf.name
            for camada in self.documento.layers
        }

        if self.camada_eixo not in camadas_existentes:
            disponiveis = ", ".join(sorted(camadas_existentes))

            raise ValueError(
                f"A camada '{self.camada_eixo}' não existe no DXF.\n"
                f"Camadas disponíveis: {disponiveis}"
            )

        candidatos = []

        for entidade in self.modelspace:
            if entidade.dxf.layer != self.camada_eixo:
                continue

            if entidade.dxftype() == "LWPOLYLINE":
                candidatos.append(entidade)

            elif entidade.dxftype() == "POLYLINE":
                if entidade.is_2d_polyline:
                    candidatos.append(entidade)

        if len(candidatos) == 0:
            raise ValueError(
                f"Nenhuma polilinha 2D foi encontrada na camada "
                f"'{self.camada_eixo}'."
            )

        if len(candidatos) > 1:
            raise ValueError(
                f"Foram encontradas {len(candidatos)} polilinhas na camada "
                f"'{self.camada_eixo}'.\n"
                "O programa exige uma única polilinha contínua para "
                "representar o eixo rodoviário."
            )

        self.eixo = candidatos[0]

        if self.eixo.closed:
            raise ValueError(
                "O eixo rodoviário está configurado como polilinha fechada. "
                "Verifique a geometria do DXF."
            )

    def _extrair_pontos(self):
        if self.eixo.dxftype() == "LWPOLYLINE":
            coordenadas = [
                (float(ponto[0]), float(ponto[1]))
                for ponto in self.eixo.get_points("xy")
            ]

        else:
            coordenadas = [
                (float(vertice.dxf.location.x),
                 float(vertice.dxf.location.y))
                for vertice in self.eixo.vertices
            ]

        self.pontos = coordenadas

    def _validar_pontos(self):
        if len(self.pontos) < 2:
            raise ValueError(
                "A polilinha do eixo precisa ter pelo menos dois vértices."
            )

        for x, y in self.pontos:
            if not isfinite(x) or not isfinite(y):
                raise ValueError(
                    "O eixo contém coordenadas inválidas."
                )

        segmentos_validos = 0

        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i + 1]

            if hypot(x2 - x1, y2 - y1) > 0:
                segmentos_validos += 1

        if segmentos_validos == 0:
            raise ValueError(
                "A polilinha não possui segmentos válidos."
            )

    def projetar_ponto(self, x_placa: float, y_placa: float):
        """
        Encontra o ponto mais próximo do eixo para uma coordenada
        de placa e calcula a direção do segmento correspondente.

        Retorna:
        - Coordenada projetada X e Y;
        - Distância entre placa e eixo;
        - Ângulo do segmento em relação ao eixo X;
        - Índice do segmento.
        """

        x_placa = float(x_placa)
        y_placa = float(y_placa)

        if not isfinite(x_placa) or not isfinite(y_placa):
            raise ValueError("As coordenadas da placa são inválidas.")

        melhor_resultado = None
        menor_distancia = float("inf")

        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i + 1]

            dx = x2 - x1
            dy = y2 - y1

            comprimento_quadrado = dx ** 2 + dy ** 2

            if comprimento_quadrado == 0:
                continue

            t = (
                (x_placa - x1) * dx
                + (y_placa - y1) * dy
            ) / comprimento_quadrado

            t = max(0.0, min(1.0, t))

            x_projetado = x1 + t * dx
            y_projetado = y1 + t * dy

            distancia = hypot(
                x_placa - x_projetado,
                y_placa - y_projetado
            )

            if distancia < menor_distancia:
                menor_distancia = distancia

                angulo = degrees(atan2(dy, dx))

                melhor_resultado = ResultadoProjecao(
                    x=x_projetado,
                    y=y_projetado,
                    distancia=distancia,
                    angulo_graus=angulo,
                    indice_segmento=i
                )

        if melhor_resultado is None:
            raise ValueError(
                "Não foi possível projetar a coordenada sobre o eixo."
            )

        return melhor_resultado
