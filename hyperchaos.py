"""Hyperchaos: divergence of divergences, in a finite continuation frame.

Tyler's definition is USER-STATED. This executable observation mechanism is an
assistant-developed FRAME; it neither implements the native □ operator nor turns
the meaning of a supplied continuation choice into an independently proven fact.
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


USER_DEFINITION = Statement(
    said=("hyper chaos is about chaos of chaotic divergences, so divergences diverging "
          "into convergent states is more akin to hyperorder, but a convergence towards "
          "divergence is hyperchaos, a divergence from something directed towards "
          "convergence, think like a butterfly effect breaking a trajectory into a "
          "different optimum is just chaos of an orderly process so not hyperchaos, "
          "but specifically divergence of divergences how they diverge, what divergence "
          "means, things like that for hyperchaos"),
    source="Tyler Roost, 2026-10-03, direct field clarification",
    relates=("hyperchaos", "divergence", "convergence", "hyperorder"),
    status="USER_STATED",
)

RULING: Ruling | None = Ruling(
    gloss=("Chaos of chaotic divergences: divergence of divergences, including "
           "convergence toward divergence. A redirected orderly trajectory toward "
           "another optimum is ordinary chaos; divergence resolving toward "
           "convergent states is the Hyperorder direction."),
    said=USER_DEFINITION.said,
    source=USER_DEFINITION.source,
)


def resolve_sense(term: str, ruling: Ruling | None = RULING) -> Sense:
    """The sense of 'hyperchaos' under a ruling; KeyError for any other term or without one."""
    if ruling is not None and not isinstance(ruling, Ruling):
        raise TypeError("only a Ruling chooses a sense")
    if term != "hyperchaos" or ruling is None:
        raise KeyError(term)
    return Sense("hyperchaos", ruling.gloss, ruling.source, ruling.builds_on)


# The continuation mechanism is intentionally independent of the historical
# usage registry. A USER-STATED definition is not a Python operationalization.
from collections import Counter, deque
from dataclasses import asdict, field
from itertools import combinations


@dataclass(frozen=True)
class Transition:
    """One supplied continuation act; choice names a semantic alternative class.

    Choice identifiers are opaque and have no order or units. A fork declares
    pairwise distinct choice classes. An ordinary unary presentation edge may
    leave choice unspecified. Renaming a choice does not alter observations.
    """

    source: str
    target: str
    choice: str | None = None

    def __post_init__(self) -> None:
        if not (_is_text(self.source) and _is_text(self.target)):
            raise ValueError("transition endpoints must be nonempty state identifiers")
        if self.choice is not None and not _is_text(self.choice):
            raise ValueError("a declared choice class must be nonempty text")


@dataclass(frozen=True)
class DivergencePattern:
    """Exact recursive split pattern, after unary and label erasure.

    Children form a canonical multiset: equal subpatterns share one pattern
    class but retain their semantic alternative multiplicity. Balanced repeated
    splitting is iterated divergence even when both sides have the same pattern.
    This records neither node identity nor terminal matter.
    """

    forks: bool
    children: frozenset[tuple[DivergencePattern, int]] = frozenset()

    def __post_init__(self) -> None:
        if not isinstance(self.forks, bool) or not isinstance(self.children, frozenset):
            raise ValueError("a pattern has a boolean fork marker and a canonical child multiset")
        seen, total = set(), 0
        for child, multiplicity in self.children:
            if not isinstance(child, DivergencePattern) or type(multiplicity) is not int or multiplicity < 1:
                raise ValueError("child multiplicity counts declared alternatives and must be positive")
            if child in seen:
                raise ValueError("one child class has one multiplicity")
            seen.add(child)
            total += multiplicity
        if (not self.forks and self.children) or (self.forks and total < 2):
            raise ValueError("a settled pattern has no children; a fork has multiple alternatives")


@dataclass(frozen=True)
class ContinuationFrame:
    """A complete, finite, acyclic observation of declared continuation choices.

    Terminals must name settled matter. Distinct terminal state identifiers may
    declare the same matter. State names do not create semantic alternatives:
    forks require distinct supplied choice classes. Cyclic/incomplete frames are
    outside this implementation and rejected rather than declared convergent.
    """

    states: tuple[str, ...]
    transitions: tuple[Transition, ...]
    outcomes: tuple[tuple[str, str], ...]
    _outgoing: dict[str, tuple[Transition, ...]] = field(init=False, repr=False,
                                                     compare=False, hash=False)
    _settled: dict[str, str] = field(init=False, repr=False, compare=False, hash=False)
    _topological: tuple[str, ...] = field(init=False, repr=False, compare=False, hash=False)
    _reachable: dict[str, frozenset[str]] = field(init=False, repr=False, compare=False, hash=False)
    _patterns: dict[str, DivergencePattern] = field(init=False, repr=False, compare=False, hash=False)

    def __post_init__(self) -> None:
        from types import MappingProxyType

        states, transitions = tuple(self.states), tuple(self.transitions)
        outcomes = tuple(tuple(pair) for pair in self.outcomes)
        if not states or len(states) > 256 or len(transitions) > 1024:
            raise ValueError("observation budget: 1..256 states and at most 1024 transitions")
        if any(not _is_text(s) for s in states) or len(set(states)) != len(states):
            raise ValueError("state identifiers must be unique nonempty text")
        if any(not isinstance(t, Transition) for t in transitions):
            raise TypeError("transitions must be Transition values")
        if len(set(transitions)) != len(transitions):
            raise ValueError("duplicate continuation records are not additional choices")
        outgoing: dict[str, list[Transition]] = {s: [] for s in states}
        indegree = {s: 0 for s in states}
        for transition in transitions:
            if transition.source not in outgoing or transition.target not in outgoing:
                raise ValueError("every transition endpoint must be a declared state")
            outgoing[transition.source].append(transition)
            indegree[transition.target] += 1
        for arrows in outgoing.values():
            if len(arrows) > 1:
                classes = [t.choice for t in arrows]
                if None in classes or len(set(classes)) != len(classes):
                    raise ValueError("a fork requires pairwise distinct declared choice classes")
        settled: dict[str, str] = {}
        for pair in outcomes:
            if len(pair) != 2:
                raise ValueError("settled declarations are (state, matter) pairs")
            state, matter = pair
            if state not in outgoing or not _is_text(matter) or state in settled:
                raise ValueError("settled declarations must be unique, bound, and nonempty")
            if outgoing[state]:
                raise ValueError("settled matter is declared only at terminal states")
            settled[state] = matter
        if set(settled) != {s for s in states if not outgoing[s]}:
            raise ValueError("every terminal must declare its settled matter")
        # Kahn's structural traversal rejects a cycle before any outcome analysis.
        pending = deque(sorted(s for s in states if indegree[s] == 0))
        ordered = []
        while pending:
            state = pending.popleft()
            ordered.append(state)
            for transition in outgoing[state]:
                indegree[transition.target] -= 1
                if indegree[transition.target] == 0:
                    pending.append(transition.target)
        if len(ordered) != len(states):
            raise ValueError("cyclic continuation is OPEN in this finite acyclic frame")
        object.__setattr__(self, "states", states)
        object.__setattr__(self, "transitions", transitions)
        object.__setattr__(self, "outcomes", outcomes)
        object.__setattr__(self, "_outgoing", MappingProxyType({
            s: tuple(sorted(arrows, key=lambda t: (t.choice or "", t.target)))
            for s, arrows in outgoing.items()}))
        object.__setattr__(self, "_settled", MappingProxyType(settled))
        object.__setattr__(self, "_topological", tuple(ordered))
        capacities, patterns = {}, {}
        terminal_pattern = DivergencePattern(False)
        for state in reversed(ordered):
            arrows = self.outgoing(state)
            capacities[state] = frozenset({state}).union(*(capacities[t.target] for t in arrows))
            if not arrows:
                patterns[state] = terminal_pattern
            elif len(arrows) == 1:
                patterns[state] = patterns[arrows[0].target]
            else:
                multiplicities = Counter(patterns[t.target] for t in arrows)
                patterns[state] = DivergencePattern(True, frozenset(multiplicities.items()))
        object.__setattr__(self, "_reachable", MappingProxyType(capacities))
        object.__setattr__(self, "_patterns", MappingProxyType(patterns))

    def outgoing(self, state: str) -> tuple[Transition, ...]:
        """Return declared acts, failing on an undeclared state."""
        return self._outgoing[state]

    def reachable(self, state: str) -> frozenset[str]:
        """Reflexive finite reachability. This is not native □ derivability."""
        return self._reachable[state]

    def settled_capacity(self, state: str) -> frozenset[str]:
        """The matter classes at all maximal continuations from this observation."""
        return frozenset(self._settled[s] for s in self.reachable(state) if s in self._settled)

    def observed_pattern(self, state: str) -> DivergencePattern:
        """Compute exact unordered recursive fork structure, erasing unary chains.

        Pattern variation is a stricter facet, not an adoption condition for
        Hyperchaos. Equal patterns can still be two divergent continuations.
        """
        return self._patterns[state]

    def route(self, source: str, target: str, *, allowed: frozenset[str] | None = None
              ) -> tuple[Transition, ...] | None:
        """Find a finite route, or None. BFS is a witness search, not a time model."""
        self.outgoing(source)
        self.outgoing(target)
        if allowed is not None and (source not in allowed or target not in allowed):
            return None
        pending = deque([source])
        previous: dict[str, Transition | None] = {source: None}
        while pending:
            current = pending.popleft()
            if current == target:
                path = []
                while previous[current] is not None:
                    transition = previous[current]
                    path.append(transition)
                    current = transition.source
                return tuple(reversed(path))
            for transition in self.outgoing(current):
                if transition.target not in previous and (
                        allowed is None or transition.target in allowed):
                    previous[transition.target] = transition
                    pending.append(transition.target)
        return None


@dataclass(frozen=True)
class DivergenceWitness:
    at: str
    alternatives: tuple[Transition, ...]


@dataclass(frozen=True)
class IteratedDivergenceWitness:
    at: str
    left_route: tuple[Transition, ...]
    right_route: tuple[Transition, ...]
    left_divergence: str
    right_divergence: str
    pattern_variation: bool


@dataclass(frozen=True)
class ConvergenceWitness:
    from_state: str
    join: str
    left_route: tuple[Transition, ...]
    right_route: tuple[Transition, ...]


@dataclass(frozen=True)
class ConvergenceTowardDivergenceWitness:
    convergence: ConvergenceWitness
    onward_route: tuple[Transition, ...]
    divergence_at: str


@dataclass(frozen=True)
class Analysis:
    root: str
    direction: str
    settled_matter: tuple[str, ...]
    first_divergences: tuple[DivergenceWitness, ...]
    iterated_divergences: tuple[IteratedDivergenceWitness, ...]
    convergences: tuple[ConvergenceWitness, ...]
    convergence_toward_divergence: tuple[ConvergenceTowardDivergenceWitness, ...]
    classification: str = "FRAME"

    def to_dict(self) -> dict:
        return asdict(self)


def _route_states(route: tuple[Transition, ...]) -> tuple[str, ...]:
    return (route[0].source,) + tuple(t.target for t in route) if route else ()


def _first_forks(frame: ContinuationFrame, start: str, allowed: frozenset[str]
                 ) -> tuple[str, ...]:
    """First divergence sites reachable before leaving one exclusive branch region."""
    if start not in allowed:
        return ()
    pending, reached, forks = [start], set(), set()
    while pending:
        current = pending.pop()
        if current in reached or current not in allowed:
            continue
        reached.add(current)
        arrows = frame.outgoing(current)
        if len(arrows) > 1:
            forks.add(current)
        else:
            pending.extend(t.target for t in arrows)
    return tuple(sorted(forks))


class AnalysisBudgetExceeded(ValueError):
    """Resource exhaustion yields no directional classification."""


def analyze(frame: ContinuationFrame, root: str, *, pair_budget: int = 20000,
            witness_budget: int = 4096, max_seconds: float = 2.0) -> Analysis:
    """Observe divergence, iterated divergence, and convergence direction.

    Iterated witnesses require separate divergence-producing branch regions
    before reconvergence. A fork reached by both routes after their join is
    instead convergence toward divergence. A common settled matter at the
    declared terminal boundary gives Hyperorder direction while retaining any
    local Hyperchaos motifs; the boundary is part of the proposition.
    """
    if not isinstance(frame, ContinuationFrame):
        raise TypeError("analyze requires a ContinuationFrame")
    if type(pair_budget) is not int or not 1 <= pair_budget <= 20000:
        raise ValueError("pair budget must be an integer within 1..20000")
    if type(witness_budget) is not int or not 1 <= witness_budget <= 4096:
        raise ValueError("witness budget must be an integer within 1..4096")
    if type(max_seconds) not in (int, float) or not 0 < max_seconds <= 20:
        raise ValueError("analysis infrastructure deadline must be within (0,20] seconds")
    from time import monotonic
    deadline, pairs = monotonic() + max_seconds, 0
    reachable = frame.reachable(root)
    forks = {s for s in reachable if len(frame.outgoing(s)) > 1}
    first = tuple(DivergenceWitness(s, frame.outgoing(s)) for s in sorted(forks))
    iterated, convergences, toward = [], [], []
    capacities = {s: frame.reachable(s) for s in reachable}
    def check_budget() -> None:
        if pairs > pair_budget or len(iterated) + len(convergences) + len(toward) > witness_budget:
            raise AnalysisBudgetExceeded("finite analysis operation/output budget exhausted; result UNKNOWN")
        if monotonic() > deadline:
            raise AnalysisBudgetExceeded("finite analysis infrastructure deadline exceeded; result UNKNOWN")
    for at in sorted(forks):
        for left, right in combinations(frame.outgoing(at), 2):
            pairs += 1
            check_budget()
            common = capacities[left.target] & capacities[right.target]
            left_only, right_only = capacities[left.target] - common, capacities[right.target] - common
            for left_fork in _first_forks(frame, left.target, left_only):
                for right_fork in _first_forks(frame, right.target, right_only):
                    left_path = frame.route(left.target, left_fork, allowed=left_only)
                    right_path = frame.route(right.target, right_fork, allowed=right_only)
                    iterated.append(IteratedDivergenceWitness(
                        at, (left,) + left_path, (right,) + right_path,
                        left_fork, right_fork,
                        frame.observed_pattern(left_fork) != frame.observed_pattern(right_fork)))
                    check_budget()
            for join in sorted(common):
                check_budget()
                # A first merge admits two paths with disjoint interior states.
                # Keeping transition acts preserves two distinct direct choices
                # even when they already land at the same state.
                left_allowed, right_allowed = left_only | {join}, right_only | {join}
                left_path = frame.route(left.target, join, allowed=frozenset(left_allowed))
                right_path = frame.route(right.target, join, allowed=frozenset(right_allowed))
                if left_path is None or right_path is None:
                    continue
                convergence = ConvergenceWitness(at, join, (left,) + left_path,
                                                  (right,) + right_path)
                convergences.append(convergence)
                check_budget()
                for divergence in _first_forks(frame, join, capacities[join]):
                    onward = frame.route(join, divergence)
                    toward.append(ConvergenceTowardDivergenceWitness(
                        convergence, onward, divergence))
                    check_budget()
    matter = tuple(sorted(frame.settled_capacity(root)))
    if len(matter) == 1 and forks:
        direction = "HYPERORDER"
    elif iterated or toward:
        direction = "HYPERCHAOS"
    elif forks:
        direction = "ORDINARY_DIVERGENCE"
    else:
        direction = "ORDERLY"
    return Analysis(root, direction, matter, first, tuple(iterated),
                    tuple(convergences), tuple(toward))


def check_iterated_witness(frame: ContinuationFrame, witness: IteratedDivergenceWitness
                           ) -> bool:
    """Check a supplied witness locally without trusting analyze's search.

    This checks finite edges, declared choices, separate lineage before the two
    divergence sites, and the optional pattern facet. It authenticates no input
    fact and makes no native □/~~/=~/== closure assertion.
    """
    if not isinstance(frame, ContinuationFrame) or not isinstance(witness, IteratedDivergenceWitness):
        return False
    left, right = witness.left_route, witness.right_route
    if not left or not right:
        return False
    for path, endpoint in ((left, witness.left_divergence), (right, witness.right_divergence)):
        if path[0].source != witness.at or path[-1].target != endpoint:
            return False
        if any(t not in frame.transitions for t in path):
            return False
        if any(a.target != b.source for a, b in zip(path, path[1:])):
            return False
        if len(frame.outgoing(endpoint)) < 2:
            return False
    if left[0] == right[0] or left[0].choice == right[0].choice:
        return False
    if set(_route_states(left)[1:]) & set(_route_states(right)[1:]):
        return False
    common = frame.reachable(left[0].target) & frame.reachable(right[0].target)
    if common & (set(_route_states(left)[1:]) | set(_route_states(right)[1:])):
        return False
    expected = frame.observed_pattern(witness.left_divergence) != frame.observed_pattern(witness.right_divergence)
    return witness.pattern_variation is expected


def examples() -> dict[str, tuple[ContinuationFrame, str]]:
    """Six independently readable field controls. Node identifiers are presentation."""
    def make(states, arrows, outcomes):
        return ContinuationFrame(tuple(states), tuple(Transition(*a) for a in arrows),
                                 tuple(outcomes.items()))

    shallow = make("rab", (("r", "a", "baseline"), ("r", "b", "perturbed")),
                   dict(a="optimum-a", b="optimum-b"))
    balanced = make("rABabcd", (("r", "A", "left"), ("r", "B", "right"),
                    ("A", "a", "a"), ("A", "b", "b"),
                    ("B", "c", "c"), ("B", "d", "d")),
                    dict(a="a", b="b", c="c", d="d"))
    varied = make("rABCabcde", (
                   ("r", "A", "left"), ("r", "B", "right"),
                   ("A", "a", "a"), ("A", "b", "b"),
                   ("B", "c", "c"), ("B", "C", "more"),
                   ("C", "d", "d"), ("C", "e", "e")),
                   dict(a="a", b="b", c="c", d="d", e="e"))
    into_divergence = make("rlqjab", (
                           ("r", "l", "left"), ("r", "q", "right"),
                           ("l", "j", None), ("q", "j", None),
                           ("j", "a", "a"), ("j", "b", "b")), dict(a="a", b="b"))
    into_order = make("rABabcdj", (("r", "A", "left"), ("r", "B", "right"),
                      ("A", "a", "a"), ("A", "b", "b"),
                      ("B", "c", "c"), ("B", "d", "d"),
                      ("a", "j", None), ("b", "j", None),
                      ("c", "j", None), ("d", "j", None)), dict(j="shared-optimum"))
    orderly = make("rsa", (("r", "s", None), ("s", "a", None)), dict(a="optimum"))
    return {"redirected-orderly-trajectory": (shallow, "r"),
            "balanced-divergence-of-divergences": (balanced, "r"),
            "varying-divergence-patterns": (varied, "r"),
            "convergence-toward-divergence": (into_divergence, "r"),
            "divergence-resolving-into-order": (into_order, "r"),
            "orderly-continuation": (orderly, "r")}


def main(argv: list[str] | None = None) -> int:
    """Read-only CLI: built-in examples, or a supplied JSON continuation frame."""
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--examples", action="store_true", help="print six contrasting reports")
    selection.add_argument("--input", type=Path, help="read a finite continuation frame from JSON")
    args = parser.parse_args(argv)
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key is ambiguous")
            result[key] = value
        return result
    try:
        if args.examples:
            reports = {name: analyze(frame, root).to_dict()
                       for name, (frame, root) in examples().items()}
        else:
            with args.input.open("rb") as source:
                content = source.read(1024 * 1024 + 1)
            if len(content) > 1024 * 1024:
                raise ValueError("input budget is one MiB of UTF-8 JSON")
            data = json.loads(content.decode("utf-8"), object_pairs_hook=unique_object)
            if not isinstance(data, dict) or set(data) != {"states", "transitions", "outcomes", "root"}:
                raise ValueError("frame JSON requires states, transitions, outcomes, root only")
            if not isinstance(data["states"], list) or not isinstance(data["transitions"], list):
                raise ValueError("states and transitions must be JSON arrays")
            if not isinstance(data["outcomes"], dict) or not _is_text(data["root"]):
                raise ValueError("outcomes must be a matter map and root a state identifier")
            frame = ContinuationFrame(tuple(data["states"]),
                                      tuple(Transition(**t) for t in data["transitions"]),
                                      tuple(data["outcomes"].items()))
            reports = analyze(frame, data["root"]).to_dict()
    except (ValueError, TypeError, KeyError, OSError) as error:
        parser.exit(2, f"FRAME REJECTED: {error}\n")
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
