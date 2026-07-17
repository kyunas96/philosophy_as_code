"""
Luxury as a subclass that may or may not honor its base class contract.

Base class:  Purchase.better_off()  -- the real thing being measured.
Subclass:    Luxury(Purchase)       -- inherits the interface, but its
                                       implementation may quietly swap
                                       in a different behavior (status
                                       signaling) while still claiming
                                       to answer the same question.

This is a Liskov Substitution Principle violation: code that calls
better_off() expects the base contract ("does this improve my life"),
but some Luxury instances substitute a different, incompatible
behavior ("does this improve how I'm perceived") without saying so.
"""

from dataclasses import dataclass


class Purchase:
    """Base class. The contract: better_off() measures genuine,
    durable improvement to the buyer's life. Any subclass that
    overrides this method is expected to preserve that meaning."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def better_off(self) -> float:
        """Returns a well-being delta. Positive = genuinely worth it."""
        raise NotImplementedError


@dataclass
class Luxury(Purchase):
    """A subclass of Purchase. Whether it honors the base contract
    depends on what's actually driving the purchase."""

    name: str
    price: float
    durability_years: float      # how long the value actually persists
    craft_quality: float         # 0-1, genuine functional/aesthetic merit
    status_signal_weight: float  # 0-1, how much of the "value" is optics

    def better_off(self) -> float:
        """
        Honors the contract to the extent that durability and craft
        (real, base-class-compatible value) dominate. Violates it to
        the extent that status signaling (a different behavior wearing
        the same interface) is doing the work instead.
        """
        genuine_value = self.craft_quality * self.durability_years
        status_value = self.status_signal_weight * 3  # decays fast, no durability term
        return genuine_value - self.price / 1000 + status_value


def violates_liskov(purchase: Luxury, tolerance: float = 1.0) -> bool:
    """
    Substitutability check: if you swapped this Luxury instance for a
    plain Purchase that only tracked genuine value, would the answer
    change by more than `tolerance`? If yes, the subclass is not
    honoring the base contract -- it's a different method pretending
    to be the same one.
    """
    genuine_only = purchase.craft_quality * purchase.durability_years - purchase.price / 1000
    actual = purchase.better_off()
    return abs(actual - genuine_only) > tolerance


def diagnose(purchase: Luxury) -> str:
    score = purchase.better_off()
    broken_contract = violates_liskov(purchase)

    verdict = f"{purchase.name}: better_off() = {score:.2f}"
    if broken_contract:
        verdict += "\n  -> Liskov violation: status signaling is standing in for genuine value."
        verdict += "\n     You're being duped -- the interface says 'better off,' the body says 'seen.'"
    else:
        verdict += "\n  -> Contract honored: the subclass actually implements what it inherited."
    return verdict


if __name__ == "__main__":
    examples = [
        Luxury("Handmade leather boots", price=450, durability_years=15,
               craft_quality=0.9, status_signal_weight=0.1),
        Luxury("Logo-covered designer bag", price=3000, durability_years=3,
               craft_quality=0.3, status_signal_weight=0.9),
        Luxury("Mechanical watch, family heirloom quality", price=8000,
               durability_years=40, craft_quality=0.85, status_signal_weight=0.2),
        Luxury("Limited-edition sneakers", price=1200, durability_years=1,
               craft_quality=0.2, status_signal_weight=0.95),
    ]

    for p in examples:
        print(diagnose(p))
        print()
