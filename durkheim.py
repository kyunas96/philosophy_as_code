"""
Emile Durkheim, expressed in code.

Core claim: society is not reducible to the sum of individuals who make
it up. It is 'sui generis' -- a thing of its own kind, with emergent
properties (social facts) that exist externally to any one person and
exert constraint on them, the way gravity constrains a thrown ball
without being "in" the ball.

This program models:
  - SocialFact: external, constraining, collective (Durkheim's definition)
  - Individual vs Society: Society is not just a list, it has emergent state
  - Mechanical vs Organic solidarity: two ways a society coheres
  - The suicide typology: the famous move of explaining a maximally
    "individual" act (suicide) via social variables (integration, regulation)
"""

from dataclasses import dataclass
from enum import Enum


# ---------------------------------------------------------------------
# A social fact is NOT reducible to any individual's psychology.
# It's external (exists before/after any one person), constraining
# (shapes behavior via pressure, not physics), and collective (shared).
# ---------------------------------------------------------------------
@dataclass
class SocialFact:
    name: str
    external: bool = True
    constraining: bool = True
    collective: bool = True

    def is_genuine(self) -> bool:
        """Durkheim's test: a fact is properly 'social' only if all
        three properties hold. Drop any one and you've reduced it
        back to psychology or biology -- exactly the move Durkheim
        spent his career resisting."""
        return self.external and self.constraining and self.collective


class Individual:
    def __init__(self, name: str, integration: float, regulation: float):
        self.name = name
        # integration: how tightly bound to social groups (0-1)
        self.integration = integration
        # regulation: how much external norms constrain desires (0-1)
        self.regulation = regulation


class Society:
    """Society is emergent: it holds properties (solidarity type,
    collective conscience strength) that no individual holds alone,
    and that don't reduce to an average of individual states."""

    def __init__(self, members: list[Individual], division_of_labor: float):
        self.members = members
        self.division_of_labor = division_of_labor  # 0 = none, 1 = highly specialized
        self.social_facts: list[SocialFact] = []

    def add_social_fact(self, fact: SocialFact):
        self.social_facts.append(fact)

    def solidarity_type(self) -> str:
        """Low division of labor -> mechanical solidarity: people are
        alike, cohesion comes from shared beliefs (a strong collective
        conscience stamping everyone the same way).

        High division of labor -> organic solidarity: people are
        different and specialized, cohesion comes from mutual
        dependence, like organs in a body -- not from being alike."""
        return "mechanical" if self.division_of_labor < 0.5 else "organic"

    def collective_conscience_strength(self) -> float:
        """Emergent property: NOT an average of individuals. It's
        strongest precisely where solidarity is mechanical."""
        base = 1 - self.division_of_labor
        genuine_facts = [f for f in self.social_facts if f.is_genuine()]
        return round(base + 0.05 * len(genuine_facts), 2)


class SuicideType(Enum):
    EGOISTIC = "egoistic"       # too little integration
    ALTRUISTIC = "altruistic"   # too much integration
    ANOMIC = "anomic"           # too little regulation
    FATALISTIC = "fatalistic"   # too much regulation
    NONE = "no elevated risk"


def classify_suicide_risk(person: Individual) -> SuicideType:
    """
    Durkheim's central move in 'Suicide' (1897): take the most
    seemingly private, individual act imaginable, and show it's
    explained by two social variables -- integration and regulation --
    each of which is pathological at BOTH extremes, not just when low.
    """
    low, high = 0.3, 0.7

    if person.integration < low:
        return SuicideType.EGOISTIC       # cut loose from the group
    if person.integration > high:
        return SuicideType.ALTRUISTIC     # self dissolved into the group
    if person.regulation < low:
        return SuicideType.ANOMIC         # desires unchecked, norms collapsed
    if person.regulation > high:
        return SuicideType.FATALISTIC     # desires suffocated by over-regulation
    return SuicideType.NONE


def diagnose_society(society: Society) -> str:
    lines = [
        f"Solidarity type: {society.solidarity_type()}",
        f"Division of labor: {society.division_of_labor}",
        f"Collective conscience strength: {society.collective_conscience_strength()}",
        "",
        "Individual risk profiles (social, not psychological, explanation):",
    ]
    for person in society.members:
        risk = classify_suicide_risk(person)
        lines.append(
            f"  {person.name}: integration={person.integration}, "
            f"regulation={person.regulation} -> {risk.value}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    # A tight-knit, low-division-of-labor traditional society
    traditional = Society(
        division_of_labor=0.1,
        members=[
            Individual("Isolated newcomer", integration=0.15, regulation=0.5),
            Individual("Devout elder", integration=0.9, regulation=0.5),
            Individual("Ordinary villager", integration=0.5, regulation=0.5),
        ],
    )
    traditional.add_social_fact(SocialFact("Shared religious ritual"))
    traditional.add_social_fact(SocialFact("Common language"))

    # A modern, high-division-of-labor industrial society
    modern = Society(
        division_of_labor=0.85,
        members=[
            Individual("Gig worker, no norms", integration=0.5, regulation=0.15),
            Individual("Overregulated employee", integration=0.5, regulation=0.85),
            Individual("Well-adjusted professional", integration=0.6, regulation=0.5),
        ],
    )
    modern.add_social_fact(SocialFact("Legal contracts"))

    print("=== Traditional society (mechanical solidarity) ===")
    print(diagnose_society(traditional))
    print()
    print("=== Modern society (organic solidarity) ===")
    print(diagnose_society(modern))
