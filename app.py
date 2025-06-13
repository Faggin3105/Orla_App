from flask import Flask, render_template, request
import pandas as pd
import joblib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from meuportal import carregar_imoveis_xml

app = Flask(__name__)

modelo = joblib.load("models/modelo_avaliacao.joblib")
le_dict = joblib.load("models/label_encoders.joblib")
colunas_modelo = joblib.load("models/colunas_modelo.joblib")

# Carrega dados do XML e gera lista de bairros
df_bairros = carregar_imoveis_xml()
lista_bairros = sorteddf_bairros['bairro'].dropna().unique().tolist()

# Restrito a Goiás, Goiânia
estados_cidades_bairros = {
    "Goiás": {
        "Goiânia": lista_bairros
    }
}

@app.route("/", methods=["GET", "POST"])
def avaliacao():
    estado = request.form.get("estado") or "Goiás"
    cidade = request.form.get("cidade") or "Goiânia"
    bairro = request.form.get("bairro") or lista_bairros[0]

    cidades = list(estados_cidades_bairros.get(estado, {}).keys())
    bairros = estados_cidades_bairros.get(estado, {}).get(cidade, [])

    tipos = le_dict['tipo'].classes_
    mobilias = le_dict['mobilia'].classes_

    valor_estimado = None
    valor_m2 = None
    grafico_path = None

    if request.method == "POST" and "avaliar" in request.form:
        try:
            entrada = pd.DataFrame([{
                'estado': le_dict['estado'].transform([estado])[0],
                'cidade': le_dict['cidade'].transform([cidade])[0],
                'bairro': le_dict['bairro'].transform([bairro])[0],
                'tipo': le_dict['tipo'].transform([request.form["tipo"]])[0],
                'm2': int(request.form["m2"]),
                'quartos': int(request.form["quartos"]),
                'banheiros': int(request.form["banheiros"]),
                'garagem': int(request.form["garagem"]),
                'ano': int(request.form["ano"]),
                'mobilia': le_dict['mobilia'].transform([request.form["mobilia"]])[0]
            }])[colunas_modelo]

            valor_estimado = modelo.predict(entrada)[0]
            valor_m2 = valor_estimado / int(request.form["m2"])

            df = carregar_imoveis_xml()
            df['faixa'] = pd.cut(df['valor'], bins=[0,200000,400000,600000,800000,1000000,1500000],
                                  labels=["Até 200k", "200k-400k", "400k-600k", "600k-800k", "800k-1M", "1M+"])
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.set_style("darkgrid")
            sns.countplot(data=df, x='faixa', palette=["#954810"], ax=ax)
            ax.set_facecolor('black')
            fig.patch.set_facecolor('black')
            ax.set_title("Distribuição de Imóveis por Faixa de Preço", fontsize=14, fontweight='bold', color='gold')
            ax.set_xlabel("Faixa de Preço", color='gold')
            ax.set_ylabel("Quantidade", color='gold')
            ax.tick_params(colors='gold')
            for container in ax.containers:
                ax.bar_label(container, fmt='%d', label_type='edge', fontsize=10, color='gold')

            grafico_path = "plot.png"
            fig.savefig(f"static/{grafico_path}", facecolor='black')
            plt.close(fig)
        except Exception as e:
            print("Erro na avaliação:", e)

    return render_template("avaliacao.html",
                           estados=estados_cidades_bairros.keys(),
                           cidades=cidades,
                           bairros=bairros,
                           estado=estado,
                           cidade=cidade,
                           bairro=bairro,
                           tipos=tipos,
                           mobilias=mobilias,
                           valor_estimado=valor_estimado,
                           valor_m2=valor_m2,
                           grafico_path=grafico_path)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")