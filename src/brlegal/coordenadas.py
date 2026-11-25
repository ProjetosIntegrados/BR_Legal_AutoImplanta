
from math import isfinite
from pyproj import Transformer


class ConversorCoordenadas:
    """
    Converte coordenadas geográficas SIRGAS 2000
    para coordenadas projetadas SIRGAS 2000 / UTM 22S.
    """

    EPSG_ORIGEM = "EPSG:4674"
    EPSG_DESTINO = "EPSG:31982"

    _transformador = Transformer.from_crs(
        EPSG_ORIGEM,
        EPSG_DESTINO,
        always_xy=True,
    )

    @classmethod
    def converter(
        cls,
        latitude: float,
        longitude: float,
    ) -> tuple[float, float]:
        """
        Retorna X e Y em metros.

        A entrada deve ser fornecida em graus decimais.
        """

        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (TypeError, ValueError):
            raise ValueError(
                "Latitude e longitude devem ser valores numéricos."
            )

        if not isfinite(latitude) or not isfinite(longitude):
            raise ValueError(
                "Latitude e longitude devem ser valores finitos."
            )

        if not -90 <= latitude <= 90:
            raise ValueError(f"Latitude inválida: {latitude}")

        if not -180 <= longitude <= 180:
            raise ValueError(f"Longitude inválida: {longitude}")

        x, y = cls._transformador.transform(
            longitude,
            latitude,
        )

        if not isfinite(x) or not isfinite(y):
            raise ValueError(
                "Não foi possível converter as coordenadas."
            )

        return x, y
