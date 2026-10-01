# Hyperchaos

**A field named before its sense.** On 2026-09-30 Tyler Roost / The TimeLord
wrote:

> "Chaos realigns into order, this has to do with atemporality, also
> hyperorder and hyperchaos theories might need grounding from hyperethics,
> Im not sure"

Later that day he named hyperchaos, with hyperorder and hyperreality, as a
field the family was missing, and asked for this repository. No statement of
his says what hyperchaos is, and no family repository defines it. Outside
the family the word is already taken: in dynamics, hyperchaos is chaos with
at least two positive Lyapunov exponents, a term Rössler introduced in 1979.

This repository is proposed as the family's home for hyperchaos. It declares
no sense. What hyperchaos is, is Q1 in [FIELD_SPEC.md](FIELD_SPEC.md);
whether it takes the dynamics meaning is Q2; which chaos realigns into order
is Q3. None of these is decided here. The usages are recorded; the finite
reading is a [FRAME].

The [finite Python frame](hyperchaos.py) keeps two disciplines:

- **No sense without a ruling.** `hyperchaos` resolves to nothing until
  Tyler rules. `chaos` never resolves to it. Recording a usage of either
  word adopts nothing.
- **A ruling is checked, not inferred.** A ruling states the sense, quotes
  his words and names their source. It may build on one recorded usage, or on
  none. Building on the dynamics meaning takes that meaning from outside the
  family, so the ruling must acknowledge it. A ruling declares a new sense;
  it never makes `hyperchaos` an alias of a usage.

The frame computes nothing: no Lyapunov exponent, attractor, clock, index,
duration or step. Order is [Hyperorder](https://github.com/TimeLordRaps/hyperorder)'s,
and the 2026-09-30 statement is recorded there too. Order among reality
presentations is [Hypertime](https://github.com/TimeLordRaps/hypertime)'s.
Chaos as disruption injected by authorities, in Tyler's account of
innocence, belongs to [Hyperethics](https://github.com/TimeLordRaps/hyperethics).
This repository cites them and does not restate them. [FIELD.json](FIELD.json)
is a local integration descriptor, not a Verifier Standard (VSTD)
certificate.

Run the standard-library suite with `python -u validate.py`. The runner
streams named tests under a 20-second overall deadline. It has no per-test
process isolation. Open questions are in [FIELD_SPEC.md](FIELD_SPEC.md),
sources in [PROVENANCE.md](PROVENANCE.md), obligations in
[TECHNICAL_DEBT.md](TECHNICAL_DEBT.md), and the next step in
[AGENT_HANDOFF.md](AGENT_HANDOFF.md).
