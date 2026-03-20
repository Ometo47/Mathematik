"""
Dreiecksrechner mit Zeichnung – Streamlit-Oberfläche.
"""

import math

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import streamlit as st

from triangle_solver import TriangleResult, solve_triangle

st.set_page_config(page_title="Dreiecksrechner", layout="wide")
st.title("Dreiecksrechner mit Zeichnung")

st.markdown(
    "Gib mindestens drei Größen ein (Seiten a, b, c und/oder Winkel α, β, γ). "
    "Leere Felder werden berechnet. Notation: Seite a liegt gegenüber Eckpunkt A (Winkel α), usw."
)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Seiten (Längen)")
    a_in = st.number_input("a", min_value=0.0, value=None, format="%.4f", placeholder="z.B. 5")
    b_in = st.number_input("b", min_value=0.0, value=None, format="%.4f", placeholder="z.B. 4")
    c_in = st.number_input("c", min_value=0.0, value=None, format="%.4f", placeholder="z.B. 3")

with col2:
    st.subheader("Winkel (Grad)")
    alpha_in = st.number_input("α (°)", min_value=0.0, max_value=180.0, value=None, format="%.2f", placeholder="z.B. 90")
    beta_in = st.number_input("β (°)", min_value=0.0, max_value=180.0, value=None, format="%.2f", placeholder="z.B. 53.13")
    gamma_in = st.number_input("γ (°)", min_value=0.0, max_value=180.0, value=None, format="%.2f", placeholder="z.B. 36.87")

a = None if a_in is None else float(a_in) if a_in > 0 else None
b = None if b_in is None else float(b_in) if b_in > 0 else None
c = None if c_in is None else float(c_in) if c_in > 0 else None
alpha = None if alpha_in is None else float(alpha_in) if 0 < alpha_in < 180 else None
beta = None if beta_in is None else float(beta_in) if 0 < beta_in < 180 else None
gamma = None if gamma_in is None else float(gamma_in) if 0 < gamma_in < 180 else None

status, results = solve_triangle(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma)

st.info(f"**Status:** {status}")

if results:
    if len(results) > 1:
        idx = st.radio("Lösung wählen", [f"Dreieck {i+1}" for i in range(len(results))], horizontal=True)
        sel = results[int(idx.split()[1]) - 1]
    else:
        sel = results[0]

    def draw_triangle(t: TriangleResult):
        cx_val = (t.b ** 2 - t.a ** 2 + t.c ** 2) / (2 * t.c)
        cy_val = math.sqrt(max(0, t.b ** 2 - cx_val ** 2))

        ax, ay = 0, 0
        bx, by = t.c, 0
        cx, cy = cx_val, cy_val

        fig, ax_plt = plt.subplots(figsize=(6, 5))
        ax_plt.set_aspect("equal")
        ax_plt.plot([ax, bx, cx, ax], [ay, by, cy, ay], "k-", lw=2)
        ax_plt.scatter([ax, bx, cx], [ay, by, cy], s=60, c="black", zorder=5)

        # Skalierung: Offsets proportional zur Dreiecksgröße
        scale = 0.06 * max(t.a, t.b, t.c)
        side_offset = scale * 1.8  # Größerer Abstand für Seitenbeschriftungen
        r = min(0.2, 0.12 * min(t.a, t.b, t.c))  # Arc-Radius skaliert mit kleinster Seite

        def mid(p, q):
            return ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2)

        def norm(v):
            d = math.hypot(v[0], v[1])
            return (v[0] / d, v[1] / d) if d > 1e-9 else (0, 0)

        # Eckpunkt-Labels: feste Richtung (unten für A/B, oben für C), getrennt von Winkel-Labels
        pad = scale * 0.8
        ax_plt.text(ax, ay - pad, "A", fontsize=14, ha="center", va="top")
        ax_plt.text(bx, by - pad, "B", fontsize=14, ha="center", va="top")
        ax_plt.text(cx, cy + pad, "C", fontsize=14, ha="center", va="bottom")

        # Seitenbeschriftungen: senkrecht zur Seite, deutlicher Abstand
        mc = mid((ax, ay), (bx, by))
        n_c = (0, -1)
        ax_plt.text(mc[0] + n_c[0] * side_offset, mc[1] + n_c[1] * side_offset, f"c = {t.c:.2f}", fontsize=11, ha="center", va="center")

        ma = mid((bx, by), (cx, cy))
        bc_vec = (cx - bx, cy - by)
        n_a = norm((bc_vec[1], -bc_vec[0]))
        if n_a[0] * (ax - ma[0]) + n_a[1] * (ay - ma[1]) > 0:
            n_a = (-n_a[0], -n_a[1])
        ax_plt.text(ma[0] + n_a[0] * side_offset, ma[1] + n_a[1] * side_offset, f"a = {t.a:.2f}", fontsize=11, ha="center", va="center")

        mb = mid((cx, cy), (ax, ay))
        ca_vec = (ax - cx, ay - cy)
        n_b = norm((ca_vec[1], -ca_vec[0]))
        if n_b[0] * (bx - mb[0]) + n_b[1] * (by - mb[1]) > 0:
            n_b = (-n_b[0], -n_b[1])
        ax_plt.text(mb[0] + n_b[0] * side_offset, mb[1] + n_b[1] * side_offset, f"b = {t.b:.2f}", fontsize=11, ha="center", va="center")

        # Winkelbögen: Start an einer Seite, Spannweite = Innenwinkel
        ang_ab, ang_ac = 0, math.degrees(math.atan2(cy, cx))
        ang_bc = math.degrees(math.atan2(cy, cx - bx))
        ang_ca = math.degrees(math.atan2(ay - cy, ax - cx))

        ax_plt.add_patch(mpatches.Arc((ax, ay), 2 * r, 2 * r, angle=0, theta1=ang_ab, theta2=ang_ac))
        ax_plt.add_patch(mpatches.Arc((bx, by), 2 * r, 2 * r, angle=0, theta1=ang_bc, theta2=ang_bc + math.degrees(t.beta)))
        ax_plt.add_patch(mpatches.Arc((cx, cy), 2 * r, 2 * r, angle=0, theta1=ang_ca, theta2=ang_ca + math.degrees(t.gamma)))

        # Winkelbeschriftungen: entlang Winkelhalbierender, außerhalb des Dreiecks
        centroid = ((ax + bx + cx) / 3, (ay + by + cy) / 3)
        bisect_alpha = norm((ax - centroid[0], ay - centroid[1]))
        bisect_beta = norm((bx - centroid[0], by - centroid[1]))
        bisect_gamma = norm((cx - centroid[0], cy - centroid[1]))
        label_dist = scale * 3.5  # Weiter weg, damit nicht mit Eckpunkt-Label kollidiert

        ax_plt.text(ax + bisect_alpha[0] * label_dist, ay + bisect_alpha[1] * label_dist, f"α = {math.degrees(t.alpha):.1f}°", fontsize=10, ha="center", va="center")
        ax_plt.text(bx + bisect_beta[0] * label_dist, by + bisect_beta[1] * label_dist, f"β = {math.degrees(t.beta):.1f}°", fontsize=10, ha="center", va="center")
        ax_plt.text(cx + bisect_gamma[0] * label_dist, cy + bisect_gamma[1] * label_dist, f"γ = {math.degrees(t.gamma):.1f}°", fontsize=10, ha="center", va="center")

        ax_plt.axis("off")
        ax_plt.margins(0.3)
        plt.tight_layout()
        return fig

    fig = draw_triangle(sel)
    st.pyplot(fig)
    plt.close(fig)

    st.subheader("Alle Werte")
    d = sel.to_dict()
    st.dataframe(
        [{"Größe": k, "Wert": v} for k, v in d.items()],
        use_container_width=True,
        hide_index=True,
    )
