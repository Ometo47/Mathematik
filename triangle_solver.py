"""
Dreiecksberechnung nach den Gesetzen der Trigonometrie.
Notation: Eckpunkte A, B, C; Seiten a, b, c gegenüber α, β, γ.
"""

import math
from dataclasses import dataclass
from typing import Optional

TOL = 1e-6


@dataclass
class TriangleResult:
    """Vollständig berechnetes Dreieck."""
    a: float
    b: float
    c: float
    alpha: float
    beta: float
    gamma: float
    perimeter: float
    area: float

    def to_dict(self) -> dict:
        return {
            "a": round(self.a, 6),
            "b": round(self.b, 6),
            "c": round(self.c, 6),
            "α (°)": round(math.degrees(self.alpha), 4),
            "β (°)": round(math.degrees(self.beta), 4),
            "γ (°)": round(math.degrees(self.gamma), 4),
            "Umfang": round(self.perimeter, 6),
            "Fläche": round(self.area, 6),
        }


def _rad(deg: float) -> float:
    return math.radians(deg)


def _deg(rad: float) -> float:
    return math.degrees(rad)


def _valid_side(x: Optional[float]) -> bool:
    return x is not None and x > TOL


def _valid_angle(x: Optional[float]) -> bool:
    return x is not None and TOL < x < 180 - TOL


def _triangle_inequality(a: float, b: float, c: float) -> bool:
    return a + b > c and b + c > a and c + a > b


def _angle_sum_ok(alpha: float, beta: float, gamma: float) -> bool:
    s = alpha + beta + gamma
    return abs(s - math.pi) < TOL


def solve_triangle(
    a: Optional[float] = None,
    b: Optional[float] = None,
    c: Optional[float] = None,
    alpha: Optional[float] = None,
    beta: Optional[float] = None,
    gamma: Optional[float] = None,
) -> tuple[str, list[TriangleResult]]:
    """
    Berechnet fehlende Dreiecksgrößen.
    Winkel werden in Grad übergeben; intern in Radiant gerechnet.
    Returns: (status_message, list_of_results)
    """
    known_sides = sum(1 for x in (a, b, c) if _valid_side(x))
    known_angles = sum(1 for x in (alpha, beta, gamma) if _valid_angle(x))

    if known_sides + known_angles < 3:
        return "Noch mindestens 3 Größen nötig (Seiten und/oder Winkel).", []

    if known_sides == 3 and known_angles == 0:
        return _solve_sss(a, b, c)
    if known_sides == 2 and known_angles == 1:
        return _solve_sas_or_ssa(a, b, c, alpha, beta, gamma)
    if known_sides == 1 and known_angles == 2:
        return _solve_asa_or_aas(a, b, c, alpha, beta, gamma)
    if known_sides == 0 and known_angles == 3:
        return "Mindestens eine Seite nötig.", []

    return "Diese Kombination wird nicht unterstützt.", []


def _solve_sss(a: float, b: float, c: float) -> tuple[str, list[TriangleResult]]:
    if not _triangle_inequality(a, b, c):
        return "Dreiecksungleichung verletzt: Keine Lösung.", []
    alpha = math.acos((b * b + c * c - a * a) / (2 * b * c))
    beta = math.acos((a * a + c * c - b * b) / (2 * a * c))
    gamma = math.pi - alpha - beta
    if gamma <= 0 or gamma >= math.pi:
        return "Widerspruch in den Winkeln.", []
    t = _build_result(a, b, c, alpha, beta, gamma)
    return "Eindeutig lösbar (SSS).", [t]


def _solve_sas_or_ssa(
    a: Optional[float],
    b: Optional[float],
    c: Optional[float],
    alpha: Optional[float],
    beta: Optional[float],
    gamma: Optional[float],
) -> tuple[str, list[TriangleResult]]:
    sides = [(a, "a", alpha, "α"), (b, "b", beta, "β"), (c, "c", gamma, "γ")]
    known_s = [(v, n, ang, ang_n) for v, n, ang, ang_n in sides if _valid_side(v)]
    known_a = [(ang, ang_n, v, n) for v, n, ang, ang_n in sides if _valid_angle(ang)]

    if len(known_s) != 2 or len(known_a) != 1:
        return "SAS/SSA: Genau 2 Seiten und 1 Winkel nötig.", []

    s1, s1n, a1, a1n = known_s[0]
    s2, s2n, a2, a2n = known_s[1]
    ang, ang_n, _, _ = known_a[0]
    ang_rad = _rad(ang)

    included = False
    if (s1n == "a" and a1n == "α") or (s1n == "b" and a1n == "β") or (s1n == "c" and a1n == "γ"):
        if (s2n == "b" and a2n == "β") or (s2n == "c" and a2n == "γ") or (s2n == "a" and a2n == "α"):
            included = (s1n, s2n, ang_n) in [
                ("a", "b", "γ"), ("b", "a", "γ"),
                ("b", "c", "α"), ("c", "b", "α"),
                ("c", "a", "β"), ("a", "c", "β"),
            ]
    if included:
        return _solve_sas(s1, s2, ang_rad, s1n, s2n, ang_n)

    return _solve_ssa(s1, s2, ang_rad, s1n, s2n, ang_n)


def _solve_sas(
    s1: float, s2: float, ang_rad: float,
    n1: str, n2: str, ang_n: str,
) -> tuple[str, list[TriangleResult]]:
    if ang_n == "γ":
        c = math.sqrt(s1 * s1 + s2 * s2 - 2 * s1 * s2 * math.cos(ang_rad))
        a, b = (s1, s2) if n1 == "a" else (s2, s1)
    elif ang_n == "α":
        a = math.sqrt(s1 * s1 + s2 * s2 - 2 * s1 * s2 * math.cos(ang_rad))
        b, c = (s1, s2) if n2 == "b" else (s2, s1)
    else:
        b = math.sqrt(s1 * s1 + s2 * s2 - 2 * s1 * s2 * math.cos(ang_rad))
        a, c = (s1, s2) if n1 == "a" else (s2, s1)

    return _solve_sss(a, b, c)


def _solve_ssa(
    s1: float, s2: float, ang_rad: float,
    n1: str, n2: str, ang_n: str,
) -> tuple[str, list[TriangleResult]]:
    opposite_side = s1 if n1 == _side_opposite(ang_n) else s2
    other_side = s2 if n1 == _side_opposite(ang_n) else s1

    h = other_side * math.sin(ang_rad)
    results = []

    if opposite_side < h - TOL:
        return "Keine Lösung (SSA): Seite gegenüber dem Winkel zu kurz.", []
    if abs(opposite_side - h) < TOL:
        gamma_alt = math.pi / 2
        third_side = math.sqrt(opposite_side ** 2 - h ** 2) if opposite_side > h else 0
        if third_side < TOL:
            third_side = math.sqrt(other_side ** 2 - h ** 2)
        t = _reconstruct_from_ssa(opposite_side, other_side, ang_rad, ang_n, third_side, 1)
        if t:
            results.append(t)
        return "Eine Lösung (SSA, rechtwinklig).", results
    if opposite_side < other_side - TOL:
        third_1 = other_side * math.cos(ang_rad) - math.sqrt(opposite_side ** 2 - h ** 2)
        third_2 = other_side * math.cos(ang_rad) + math.sqrt(opposite_side ** 2 - h ** 2)
        t1 = _reconstruct_from_ssa(opposite_side, other_side, ang_rad, ang_n, third_1, 1)
        t2 = _reconstruct_from_ssa(opposite_side, other_side, ang_rad, ang_n, third_2, 2)
        if t1 and t2 and abs(t1.a - t2.a) > TOL:
            return "Zwei mögliche Dreiecke (SSA).", [t1, t2]

    third = other_side * math.cos(ang_rad) + math.sqrt(opposite_side ** 2 - h ** 2)
    if third < TOL:
        third = other_side * math.cos(ang_rad) - math.sqrt(opposite_side ** 2 - h ** 2)
    t = _reconstruct_from_ssa(opposite_side, other_side, ang_rad, ang_n, third, 1)
    if t:
        results.append(t)
    return "Eindeutig lösbar (SSA).", results


def _side_opposite(ang: str) -> str:
    return {"α": "a", "β": "b", "γ": "c"}[ang]


def _reconstruct_from_ssa(
    opp: float, adj: float, ang_rad: float, ang_n: str,
    third: float, which: int,
) -> Optional[TriangleResult]:
    if third <= TOL:
        return None
    if ang_n == "α":
        a, b, c = opp, adj, third
        beta = math.asin(b * math.sin(ang_rad) / a)
        if which == 2:
            beta = math.pi - beta
        gamma = math.pi - ang_rad - beta
    elif ang_n == "β":
        a, b, c = adj, opp, third
        alpha = math.asin(a * math.sin(ang_rad) / b)
        if which == 2:
            alpha = math.pi - alpha
        gamma = math.pi - ang_rad - alpha
    else:
        a, b, c = adj, third, opp
        alpha = math.asin(a * math.sin(ang_rad) / c)
        if which == 2:
            alpha = math.pi - alpha
        beta = math.pi - ang_rad - alpha

    if alpha <= 0 or beta <= 0 or gamma <= 0 or alpha >= math.pi or beta >= math.pi or gamma >= math.pi:
        return None
    if not _triangle_inequality(a, b, c):
        return None
    return _build_result(a, b, c, alpha, beta, gamma)


def _solve_asa_or_aas(
    a: Optional[float],
    b: Optional[float],
    c: Optional[float],
    alpha: Optional[float],
    beta: Optional[float],
    gamma: Optional[float],
) -> tuple[str, list[TriangleResult]]:
    known_sides: list[tuple[str, float]] = []
    if _valid_side(a):
        known_sides.append(("a", a))
    if _valid_side(b):
        known_sides.append(("b", b))
    if _valid_side(c):
        known_sides.append(("c", c))

    known_angles: list[tuple[str, float]] = []
    if _valid_angle(alpha):
        known_angles.append(("α", _rad(alpha)))
    if _valid_angle(beta):
        known_angles.append(("β", _rad(beta)))
    if _valid_angle(gamma):
        known_angles.append(("γ", _rad(gamma)))

    if len(known_sides) != 1 or len(known_angles) != 2:
        return "ASA/AAS: Genau 1 Seite und 2 Winkel nötig.", []

    side_name, side_val = known_sides[0]
    ang_dict = {"α": None, "β": None, "γ": None}
    for n, v in known_angles:
        ang_dict[n] = v

    third = math.pi - sum(v for v in ang_dict.values() if v is not None)
    for k in ang_dict:
        if ang_dict[k] is None:
            ang_dict[k] = third
            break

    alpha_r, beta_r, gamma_r = ang_dict["α"], ang_dict["β"], ang_dict["γ"]
    if not _angle_sum_ok(alpha_r, beta_r, gamma_r):
        return "Winkelsumme ≠ 180°.", []

    k = side_val / {"a": math.sin(alpha_r), "b": math.sin(beta_r), "c": math.sin(gamma_r)}[side_name]
    a_val = k * math.sin(alpha_r)
    b_val = k * math.sin(beta_r)
    c_val = k * math.sin(gamma_r)

    if not _triangle_inequality(a_val, b_val, c_val):
        return "Keine gültige Lösung.", []

    t = _build_result(a_val, b_val, c_val, alpha_r, beta_r, gamma_r)
    return "Eindeutig lösbar (ASA/AAS).", [t]


def _build_result(a: float, b: float, c: float, alpha: float, beta: float, gamma: float) -> TriangleResult:
    p = a + b + c
    s = p / 2
    area = math.sqrt(max(0, s * (s - a) * (s - b) * (s - c)))
    return TriangleResult(a=a, b=b, c=c, alpha=alpha, beta=beta, gamma=gamma, perimeter=p, area=area)
