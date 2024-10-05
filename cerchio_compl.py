import matplotlib.pyplot as plt
import numpy as np


def disegna_cerchio_di_completamento(
    percentuale, spessore=0.4, dimensione_figura=(6, 6)
):
    # Dati
    valori = [percentuale, 100 - percentuale]
    colori = ["#4CAF50", "#DDDDDD"]

    # Creazione del diagramma a torta con dimensione personalizzata
    fig, ax = plt.subplots(figsize=dimensione_figura)
    ax.pie(
        valori,
        colors=colori,
        startangle=90,
        counterclock=False,
        wedgeprops=dict(width=spessore),
    )

    # Rimuovi l'asse per avere un cerchio perfetto
    ax.axis("equal")
    ax.set_facecolor("none")
    fig.patch.set_visible(False)

    # Salva il diagramma come PNG con sfondo trasparente
    plt.savefig(
        "cerchio_di_completamento.png", dpi=300, bbox_inches="tight", transparent=True
    )
    plt.show()


# Usa la funzione con spessore e dimensione personalizzati
percentuale_completata = 79
disegna_cerchio_di_completamento(
    percentuale_completata, spessore=0.1, dimensione_figura=(8, 8)
)
