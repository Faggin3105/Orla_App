import pandas as pd
import requests
import xml.etree.ElementTree as ET

def carregar_imoveis_xml():
    print("Carregando dados do XML...")
    url = "https://integracao.arboimoveis.com/api/custom-xml/imobiliaria/b13d33183002d16470691a3fa052c08fb527b62743ac71834be7788fc84736acpfFv4ptPWLl3kr2Lwj8NyDfZhNYSYyHaK3pjzK82y9c=/imovelweb-xml"
    response = requests.get(url)
    tree = ET.fromstring(response.content)

    imoveis = []
    imoveis_tag = tree.find("Imoveis")
    if imoveis_tag is not None:
        for imovel in imoveis_tag.findall("Imovel"):
            imoveis.append({
                "estado": imovel.findtext("UF", default="GO"),
                "cidade": imovel.findtext("Cidade"),
                "bairro": imovel.findtext("Bairro"),
                "tipo": imovel.findtext("TipoImovel"),
                "m2": float(imovel.findtext("AreaUtil", default="0")),
                "quartos": int(imovel.findtext("QtdDormitorios", default="0")),
                "banheiros": int(imovel.findtext("QtdBanheiros", default="0")),
                "garagem": int(imovel.findtext("QtdVagas", default="0")),
                "mobilia": imovel.findtext("Mobiliado", default="Nao"),
                "ano": 2020,
                "valor": float(imovel.findtext("PrecoVenda", default="0"))
            })

    df = pd.DataFrame(imoveis)
    print("Colunas disponíveis no DataFrame:")
    print(df.columns)
    print(df.head())
    return df
