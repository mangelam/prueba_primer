from flask import Flask, render_template, request

app = Flask(__name__)

# Función para calcular facings
def calcular_facings(ventas_semana, tiempo_reposicion_dias, unidades_por_cara, buffer_semanas=0.3, minimo_caras=1):
    cobertura_semanas = (tiempo_reposicion_dias / 7) + buffer_semanas
    unidades_necesarias = ventas_semana * cobertura_semanas
    facings = unidades_necesarias / unidades_por_cara

    # Redondear hacia arriba
    facings_redondeado = int(facings) if facings == int(facings) else int(facings) + 1

    # Aplicar mínimo de caras
    return max(facings_redondeado, minimo_caras)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        try:
            ventas_semana = float(request.form["ventas_semana"])
            tiempo_reposicion = int(request.form["tiempo_reposicion"])
            unidades_por_cara = int(request.form["unidades_por_cara"])
            buffer_semanas = float(request.form.get("buffer", 0.3))
            minimo_caras = int(request.form.get("minimo", 1))

            resultado = calcular_facings(
                ventas_semana,
                tiempo_reposicion,
                unidades_por_cara,
                buffer_semanas,
                minimo_caras
            )
        except ValueError:
            resultado = "⚠️ Error: Por favor ingresa valores numéricos válidos."

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
