from pathlib import Path

from brlegal.leitor_cadastro import LeitorCadastroVertical


def main() -> None:
    caminho_planilha = (
        Path(__file__).resolve().parents[2]
        / "21_Necessidades de Sinalização Vertical.xlsm"
    )
    leitor = LeitorCadastroVertical(caminho_planilha)

    placas = leitor.ler()

    for placa in placas:
        # print(placa)
        print()

    print(f"Total de placas lidas: {len(placas)}")

if __name__ == "__main__":
    main()


# E-2.dxf