# Technical-debt and proof obligations

| ID | Mechanism or uncertainty | Status | Revisit gate |
|---|---|---|---|
| HC-001 | No sense of hyperchaos is declared. `RULING` is `None`. | OPEN | Tyler's ruling (Q1), entered as a `Ruling` with his words and their source, and a test of the sense it gives. |
| HC-002 | The word collides with the dynamics term: chaos with at least two positive Lyapunov exponents. The guard reads the ruling's declared `builds_on`; a ruling whose gloss restates the dynamics meaning without naming it is not caught. | OPEN | Tyler's ruling (Q2). If he keeps the name with another meaning, say so in the README beside the citation. |
| HC-003 | Which chaos realigns into order: the 2026-09-26 disruption from authorities, or another. The two statements are not reconciled. | OPEN | Tyler's ruling (Q3). |
| HC-004 | Hyperethics as hyperchaos's ground. Tyler: "Im not sure". | OPEN | Tyler's ruling (Q4), stated in both repositories, and kept consistent with Hyperorder's HO-002. |
| HC-005 | How hyperchaos relates to hyperorder. | OPEN | Tyler's ruling (Q5), after Hyperorder's HO-001. |
| HC-006 | Which field owns atemporality, described on 2026-09-25 as "ORDER reachable from either direction". | OPEN | Tyler's ruling (Q6). |
| HC-007 | An unpublished Hypergrammar draft treats chaos as having no causal structure. It is not a recorded usage. | OPEN | Record it as a usage, with its pinned source, when Hypergrammar publishes it. |
| HC-008 | The `authority-disruption` usage cites Tyler's statements of 2026-09-26. Hyperethics's published repository does not state them yet. | OPEN | Re-pin the usage to Hyperethics when it publishes them. |
| HC-009 | A `Ruling` is checked for form. Nothing authenticates that its words are Tyler's. | OPEN | Before a ruling is entered, quote it from his statement and cite where it was made. |
| HC-010 | The ruling's form, the two standings and "a ruling declares a new sense, never an alias" are assistant-proposed bookkeeping. | OPEN | Tyler's acceptance of the discipline as this field's own. |

Checkpoint 1 on 2026-09-30 inspected the ruling's form, which is the hotspot:
no ruling may make `hyperchaos` an alias of a usage, and none may take on the
external meaning without acknowledging it. Its neighbour, the empty sense
table, was inspected alongside it: `hyperchaos` must resolve to nothing
while `RULING` is `None`.

The tests check three refusals and one reading:
- refusals: a sense without a ruling, `chaos` for `hyperchaos`, and an
  unacknowledged external meaning;
- reading: a ruling gives a new sense that names what it builds on.

The rotating neglected area is the external citation (HC-002: the dynamics
term is cited from its original paper, and the two-exponent criterion is the
literature's later usage). PowerShell `Get-Random -Minimum 3 -Maximum 8` drew
**3**, so the next rotating audit is due at coherent change-and-check
checkpoint **4**. No seed was supplied, so do not redraw to postpone the
audit.
