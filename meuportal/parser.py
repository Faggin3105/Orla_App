import pandas as pd
import requests
import xml.etree.ElementTree as ET
from io import BytesIO

URL_XML = "https://integracao.arboimoveis.com/api/custom-xml/imobiliaria/b13d33183002d16470691a3fa052c08fb527b62743ac71834be7788fc84736acpfFv4ptPWLl3kr2Lwj8NyDfZhNYSYyHaK3pjzK82y9c=/imovelweb-xml"

def carregar_imoveis_xml():
    response = requests.get(URL_XML)
    root = ET.parse(BytesIO(response.content)).getroot()

    imoveis = []
    for imovel in root.findall("./Imovel"):
        try:
            imoveis.append({
                "tipo": imovel.findtext("TipoImovel", default="").strip(),
                "bairro": imovel.findtext("Bairro", default="").strip(),
                "cidade": imovel.findtext("Cidade", default="").strip(),
                "estado": imovel.findtext("UF", default="").strip(),
                "m2": float(imovel.findtext("AreaUtil", default="0")),
                "quartos": int(imovel.findtext("QtdDormitorios", default="0")),
                "banheiros": int(imovel.findtext("QtdBanheiros", default="0")),
                "garagem": int(imovel.findtext("QtdVagas", default="0")),
                "mobilia": "Sim" if imovel.findtext("Mobiliado", default="false").lower() == "true" else "Não",
                "valor": float(imovel.findtext("PrecoVenda", default="0"))
            })
        except Exception as e:
            print("Erro ao processar imóvel:", e)

    df = pd.DataFrame(imoveis)
    df = df[df["valor"] > 10000]  # Remove valores zerados ou fictícios
    df["valor_m2"] = df["valor"] / df["m2"]
    return df
