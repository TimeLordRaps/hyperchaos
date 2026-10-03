# Hyperchaos field specification, 0.2.0

## Meaning and classifications

**[HYPER] USER-STATED, 2026-10-03:** Hyperchaos concerns chaos of chaotic
divergences, specifically divergence of divergences and how they diverge.
Convergence toward divergence belongs to it; divergences resolving into
convergent states point toward Hyperorder. A redirected orderly process
reaching a different optimum is ordinary chaos and does not suffice.

The exact statement is `USER_DEFINITION`; `RULING` now quotes it, and
`resolve_sense("hyperchaos")` returns that sense. The previous empty ruling
is superseded by the direct clarification. `chaos` remains distinct, never
an alias. Explicit `None` still leaves a ruling unresolved. Usage records do
not choose a sense by themselves, and ruling shape does not authenticate
the speaker.

**[FRAME]** Everything below is an assistant-developed finite observation.
**[OPEN]** Native derivation from `□` and relation-preserving transfer into
`~~`, `=~`, `~=`, and `==` have not been discharged. The concrete L1
implication subpath `== ⇒ =~ ⇒ ~~` is one part of the published quadrilateral
architecture. Its distinct `~=` abstraction branch and conditional retrace
must not be flattened into a four-term implication chain. In the pinned
public snapshot the quadrilateral research/Lean sources expose the branch,
but L2 `.hm` does not; the public Lean retrace witness already supplies mutual
simulation. The source-level restrictions are stated in
[THEORY.md](THEORY.md) and [PROVENANCE.md](PROVENANCE.md).

## Immutable input

`ContinuationFrame(states, transitions, outcomes)` copies its inputs and
protects internal maps. State identifiers are unique nonempty strings.
`Transition(source, target, choice)` has bound endpoints and an optional
nonempty choice class. Duplicate records are refused. Each fork must
declare pairwise distinct semantic choice classes. This is a caller-supplied
semantic quotient: the caller first identifies presentations of the same
continuation act. Unequal endpoint names alone are insufficient.

Every terminal must declare nonempty settled matter; nonterminals may not.
Different terminal identifiers may name the same matter. Unknown matter is
refused, not declared convergent. Kahn's directed acyclic graph (DAG)
traversal rejects cycles. Acyclicity supplies termination of this finite
computation, not native truth or closure. Input budgets: 1–256 states and
at most 1,024 transitions.

## Observations and witnesses

- `outgoing(state)` returns declared acts; unknown states fail.
- `reachable(state)` returns cached reflexive finite reachability.
- `settled_capacity(state)` returns terminal matter classes reachable from
  this state. It is not the full native continuation capacity.
- `route(source, target, allowed=...)` returns an actual transition route or
  `None`. Breadth-first search (BFS) selects a witness; its search distance
  is not a time model.
- `observed_pattern(state)` returns a cached recursive multiset of fork
  patterns after erasing identifiers, matter spellings and unary chains.
  Semantic alternative multiplicities remain; branch ordering has no meaning.
  This finite presentation abstraction does not establish native `~=` or
  authorize a retrace from pattern equality to native simulation.

`analyze(frame, root)` returns `Analysis` with:

| Field | Exact finite proposition |
|---|---|
| `first_divergences` | Every reachable fork of distinct declared choice classes |
| `iterated_divergences` | A fork has two alternatives, each reaching its own first divergence site in separate regions before reconvergence |
| `pattern_variation` on an iterated witness | The two sites have unequal recursive split patterns, a stricter facet rather than a requirement for Hyperchaos |
| `convergences` | Distinct choices have routes with disjoint interiors to a first shared state |
| `convergence_toward_divergence` | Such a shared state continues to a first divergence site |
| `settled_matter` | Terminal matter classes reachable from the selected root |
| `direction` | Boundary reading below; local witnesses are retained |

The first divergence sites on both sides occur before any state reachable
from the other side. Reaching one shared fork by two routes is therefore
convergence toward divergence, not two independent divergences. Witnesses
retain actual acts, including distinct choices landing at the same state.

## Boundary direction and limits

This assistant-proposed rule binds the observation boundary to the claim:

1. Reachable forks with one common terminal matter give `HYPERORDER` direction.
2. Otherwise an iterated-divergence or convergence-toward-divergence witness
   gives `HYPERCHAOS` direction.
3. Other reachable forks give `ORDINARY_DIVERGENCE`.
4. No reachable fork gives `ORDERLY`.

These classify this finite observation, not the complete ontology of Tyler's
field. Boundary `HYPERORDER` does not erase local Hyperchaos motifs. Equal
nested patterns still qualify as iterated divergence. Two orderly redirected
alternatives do not.

`analyze` defaults to at most 20,000 alternative-pair inspections, 4,096
combined higher/merge/onward witnesses, and a two-second infrastructure
deadline. Budgets can be lowered; the deadline may be raised to at most
20 seconds. Exhaustion raises `AnalysisBudgetExceeded` with result `UNKNOWN`,
returning no classification. The constructor caches reachability and
pattern classes. No claim of constant-time analysis or unbounded capacity
is made. Input limits and infrastructure seconds are not field variables.

## Check and command-line interface

`check_iterated_witness(frame, witness)` checks edges, connected paths,
distinct choices, divergence endpoints, separate lineage and the pattern
facet without trusting the analyzer's search. It does not authenticate
semantic input facts. Forged transition, shared lineage, wrong endpoint or
wrong pattern flag fails.

`python -B -u hyperchaos.py --examples` emits six full JavaScript Object
Notation (JSON) reports. `--input <frame.json>` reads exactly `states`,
`transitions`, `outcomes` and `root`; transition objects contain `source`,
`target` and optional `choice`. Duplicate JSON keys are ambiguous and refused.
The read budget is one mebibyte (MiB, 1,048,576 bytes). Malformed or exhausted
inputs exit 2. The command writes no frame and performs no remote operation.

The descriptor binds actual exports. `validate.py` runs the full streaming
`unittest` suite under a 20-second overall deadline without per-test process
isolation. The finite oracle checks all 1,024 five-state acyclic structures;
this does not prove all unbounded frames correct. Native integration, real
application qualification, cyclic continuation and ethical assessment stay
separate [OPEN] gates described in [THEORY.md](THEORY.md).
