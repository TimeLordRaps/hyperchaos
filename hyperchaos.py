"""Finite Hyperchaos frame: a field named before its sense, and the ruling that would give it one.

This module does not implement hyperchaos. No sense of hyperchaos has been given, so the
term resolves to nothing. The module records the senses in which the sources use the
words "chaos" and "hyperchaos", keeps Tyler's 2026-09-30 statements open, and checks the
form of the ruling that would choose a sense: his words, their source, and what the sense
builds on, with any outside meaning of the same word acknowledged.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Standing(Enum):
    USER_STATED = "USER_STATED"
    EXTERNAL = "EXTERNAL"


@dataclass(frozen=True)
class Usage:
    """A sense in which a source uses a word. Recording it adopts nothing."""

    name: str
    term: str
    gloss: str
    source: str
    standing: Standing


USAGES = (
    Usage("authority-disruption", "chaos",
          "disruption injected by authorities, which may be unnecessary and need not carry "
          "negative intent; it corrupts innocence, and is contrasted with the pleasure of order",
          "Tyler Roost, 2026-09-26, USER-STATED in a working session on innocence",
          Standing.USER_STATED),
    Usage("two-positive-lyapunov-exponents", "hyperchaos",
          "chaotic dynamics with at least two positive Lyapunov exponents",
          "the dynamics literature's usage of the term introduced in O. E. Rossler, "
          "'An equation for hyperchaos', Physics Letters A 71 (1979) 155-157",
          Standing.EXTERNAL),
)

_USAGE = {u.name: u for u in USAGES}


@dataclass(frozen=True)
class Statement:
    said: str
    source: str
    relates: tuple[str, ...]
    status: str


REALIGNMENT = Statement(
    said=("Chaos realigns into order, this has to do with atemporality, also hyperorder "
          "and hyperchaos theories might need grounding from hyperethics, Im not sure"),
    source="Tyler Roost, 2026-09-30, USER-STATED in a working session",
    relates=("chaos", "order", "atemporality", "hyperorder", "hyperchaos", "hyperethics"),
    status="OPEN",
)

MISSING = Statement(
    said="We are missing at least hyperorder, hyperchaos, hyperreality",
    source="Tyler Roost, 2026-09-30, USER-STATED in a working session",
    relates=("hyperorder", "hyperchaos", "hyperreality"),
    status="OPEN",
)


def _is_text(x: object) -> bool:
    return isinstance(x, str) and bool(x.strip())


@dataclass(frozen=True)
class Ruling:
    """Tyler's choice of a sense for hyperchaos: the sense, his words, their source.

    ``builds_on`` names a recorded usage, or None for a sense that builds on none. Building
    on an external usage takes its meaning from outside the family, so it must say so.
    """

    gloss: str
    said: str
    source: str
    builds_on: str | None = None
    acknowledges_external: bool = False

    def __post_init__(self) -> None:
        if not (_is_text(self.gloss) and _is_text(self.said) and _is_text(self.source)):
            raise ValueError("a ruling states its sense, quotes his words, and names their source")
        if not isinstance(self.acknowledges_external, bool):
            raise ValueError("acknowledges_external is a declaration, True or False")
        if self.builds_on is not None and self.builds_on not in _USAGE:
            raise ValueError("a ruling builds only on a recorded usage")
        external = self.builds_on is not None and _USAGE[self.builds_on].standing is Standing.EXTERNAL
        if external != self.acknowledges_external:
            raise ValueError("an external usage is built on only when acknowledged, "
                             "and only an external usage is acknowledged")


@dataclass(frozen=True)
class Sense:
    name: str
    gloss: str
    source: str
    builds_on: str | None


# No sense of hyperchaos has been chosen. This stays None until Tyler rules.
RULING: Ruling | None = None


def resolve_sense(term: str, ruling: Ruling | None = RULING) -> Sense:
    """The sense of 'hyperchaos' under a ruling; KeyError for any other term or without one."""
    if ruling is not None and not isinstance(ruling, Ruling):
        raise TypeError("only a Ruling chooses a sense")
    if term != "hyperchaos" or ruling is None:
        raise KeyError(term)
    return Sense("hyperchaos", ruling.gloss, ruling.source, ruling.builds_on)
