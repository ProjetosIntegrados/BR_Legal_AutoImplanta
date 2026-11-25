
from pathlib import Path

from src.brlegal.leitor_cadastro import LeitorCadastroVertical


def main():

    # Caminho da planilha
    caminho_planilha = (
        Path(__file__).resolve().parent
        / "21_Necessidades de Sinalização Vertical.xlsm"
    )

    if not caminho_planilha.exists():
        print("ERRO: Planilha não encontrada.")
        print(f"Caminho procurado: {caminho_planilha}")
        return

    print("=" * 60)
    print("BR LEGAL CAD - TESTE DE LEITURA DO CADASTRO")
    print("=" * 60)

    leitor = LeitorCadastroVertical(caminho_planilha)

    try:
        placas = leitor.ler()

        print(f"\nTotal de placas carregadas: {len(placas)}")

        print("\nPRIMEIRAS 5 PLACAS:")
        print("-" * 60)

        for placa in placas[:5]:

            print(f"Código: {placa.codigo_placa}")
            print(f"KM: {placa.km:.3f}")
            print(f"Lado: {placa.lado.value}")
            print(f"Latitude: {placa.latitude:.8f}")
            print(f"Longitude: {placa.longitude:.8f}")
            print(f"X UTM: {placa.x:.3f} m")
            print(f"Y UTM: {placa.y:.3f} m")
            print("-" * 60)

        print("\nTESTE FINALIZADO.")

    except Exception as erro:
        print(f"\nERRO DURANTE A LEITURA: {erro}")


if __name__ == "__main__":
    main()
