# Hyperchaos

**The chaos of chaotic divergences: how divergences themselves diverge.**
Tyler Roost / The TimeLord supplied this field's sense on 2026-10-03.
Convergence toward divergence belongs to Hyperchaos. Divergences resolving
toward convergent states point toward Hyperorder. A butterfly effect that
redirects an orderly trajectory toward another optimum is ordinary chaos;
that alone is not Hyperchaos. [PROVENANCE.md](PROVENANCE.md) preserves his
exact definition and the preceding, now superseded, absence of a definition.

This repository develops the field in two connected parts:

- [THEORY.md](THEORY.md): divergence, divergence of divergences, convergence
  direction, recursive pattern observation, propositions, counterexamples,
  and native grounding obligations that remain open.
- [hyperchaos.py](hyperchaos.py): a runnable continuation analyzer returning
  actual lineage witnesses for first divergence, iterated divergence,
  reconvergence, and convergence into a divergence-producing region.

The definition is **USER-STATED [HYPER]**. Its mathematical observation
mechanism is an **assistant-developed [FRAME]**. It uses supplied semantic
choice classes; different node names alone do not manufacture divergence.

## Run it

Python 3.12 or later, standard library only:

```console
python -B -u hyperchaos.py --examples
python -B -u hyperchaos.py --input examples/balanced-divergence.json
python -B -u validate.py
```

The examples print full JavaScript Object Notation (JSON) reports, including
the transitions that witness each observation:

| Example | Boundary direction | Finite observation |
|---|---|---|
| Redirected orderly trajectory | `ORDINARY_DIVERGENCE` | One fork toward different optima; no divergence of divergences |
| Balanced divergence of divergences | `HYPERCHAOS` | Two separate alternatives each generate divergence; identical split patterns still qualify |
| Varying divergence patterns | `HYPERCHAOS` | Iterated divergence plus variation in its recursive split pattern |
| Convergence toward divergence | `HYPERCHAOS` | Two lineage routes reconverge into a shared divergence-producing region |
| Divergence resolving into order | `HYPERORDER` | Local iterated divergence persists, while every maximal continuation resolves to the same declared matter |
| Orderly continuation | `ORDERLY` | Unary continuation without a declared alternative fork |

`HYPERORDER` here names a **directional reading of a selected boundary**;
this repository does not implement or replace Hyperorder's field. Local
Hyperchaos motifs and that resolved boundary can coexist. Looking only at
final matter would erase how divergence happened, so reports preserve both.

## Analyze a continuation family

```python
from hyperchaos import ContinuationFrame, Transition, analyze, check_iterated_witness

family = ContinuationFrame(
    states=("root", "left", "right", "a", "b", "c", "d"),
    transitions=(
        Transition("root", "left", "left-alternative"),
        Transition("root", "right", "right-alternative"),
        Transition("left", "a", "a-alternative"),
        Transition("left", "b", "b-alternative"),
        Transition("right", "c", "c-alternative"),
        Transition("right", "d", "d-alternative"),
    ),
    outcomes=(("a", "a"), ("b", "b"), ("c", "c"), ("d", "d")),
)
report = analyze(family, "root")
assert report.direction == "HYPERCHAOS"
assert check_iterated_witness(family, report.iterated_divergences[0])
```

Each fork's `choice` identifiers declare **distinct semantic continuation
classes**, not just different buttons or spellings. Two displays of one
choice need one class; duplicate classes at a fork are rejected. Unary
presentation edges may omit the choice. Terminal states declare settled
matter independently of their identifiers, so several terminal presentations
can resolve to the same matter. The caller must justify these declarations
in the system being studied.

Possible applications include branching search strategies, alternative
formation paths, reconverging workflows, and changes in how a process opens
further alternatives. The mechanism produces inspectable structure rather
than a scalar chaos score. Real application qualification remains open;
the tests exercise supplied finite structures.

## Grounding and execution boundaries

The source family preserves `□`, `~~`, `=~`, and `==`: ground/application,
continuation overlap, same substance regardless of path, and mutual
simulation. This implementation's reachability, matter equality and pattern
equality are finite observations. Their native bridge is **[OPEN]**. Equal
split patterns do not establish `==`; absence of a finite witness does not
establish native nonclosure.

The frame accepts complete acyclic observations with 1–256 states and at
most 1,024 transitions. Cached reachability and recursive pattern classes
avoid unfolding all paths. Analysis has operation/output budgets and an
infrastructure deadline; exhausted budgets reject with `UNKNOWN`, without
a synthetic directional result. These are execution limits, not field
thresholds. Cycles and unknown terminal matter are rejected, not turned
into order. No clock, metric, probability, Lyapunov exponent, ethical verdict
or physical mechanism is required by the field observation.

The full suite includes witness tampering, relabeling, unary insertion and
contraction, malformed input, and an independent complete-path oracle over
all 1,024 acyclic five-state structures. `validate.py` streams named tests
under a 20-second overall deadline, without per-test process isolation.
These checks establish the finite contract, not universal closure or a
Verifier Standard (VSTD) certificate.

[FIELD_SPEC.md](FIELD_SPEC.md) specifies the API and input contract;
[FIELD.json](FIELD.json) lists exports;
[TECHNICAL_DEBT.md](TECHNICAL_DEBT.md) tracks open obligations;
[AGENT_HANDOFF.md](AGENT_HANDOFF.md) records the development gates.
