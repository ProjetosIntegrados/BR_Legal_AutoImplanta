
from src.brlegal.eixo import EixoRodoviario

CAMINHO_DXF = r"C:\Users\nicol\OneDrive\Documentos\UFRGS - Engenharia Civil\Projetos Integrados III\Lote 01 - BR-392 - teste.dxf"

try:
    eixo = EixoRodoviario(CAMINHO_DXF)

    print("\nBR LEGAL CAD - TESTE DO EIXO")
    print("-" * 40)

    print("Arquivo:", CAMINHO_DXF)
    print("Camada:", eixo.camada_eixo)
    print("Tipo:", eixo.eixo.dxftype())
    print("Quantidade de vértices:", len(eixo.pontos))

    print("\nPrimeiros vértices:")
    for ponto in eixo.pontos[:5]:
        print(ponto)

    print("\nEixo carregado com sucesso!")

except Exception as erro:
    print("\nERRO AO CARREGAR O EIXO:")
    print(erro)
