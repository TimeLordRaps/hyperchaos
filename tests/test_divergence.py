"""Semantic acceptance examples supplied independently of implementation."""

import unittest
from dataclasses import replace
from itertools import combinations
import hyperchaos as h


def frame(states, arrows, outcomes):
    return h.ContinuationFrame(tuple(states), tuple(h.Transition(*a) for a in arrows),
                               tuple(outcomes.items()))


class DefinitionAndDepthTests(unittest.TestCase):
    def test_current_user_definition_is_not_frozen_as_absent(self):
        self.assertIsNotNone(h.RULING)
        self.assertIn("divergence", h.resolve_sense("hyperchaos").gloss)
        self.assertIn("2026-10-03", h.RULING.source)

    def test_balanced_divergence_of_divergences_is_hyperchaos(self):
        f = frame("rABabcd", (("r", "A", "left"), ("r", "B", "right"),
                  ("A", "a", "a-choice"), ("A", "b", "b-choice"),
                  ("B", "c", "c-choice"), ("B", "d", "d-choice")),
                  dict(a="a", b="b", c="c", d="d"))
        report = h.analyze(f, "r")
        self.assertEqual(report.direction, "HYPERCHAOS")
        self.assertEqual(len(report.iterated_divergences), 1)
        self.assertFalse(report.iterated_divergences[0].pattern_variation)

    def test_butterfly_redirect_to_another_optimum_is_only_first_order(self):
        f = frame(("r", "a", "b"), (("r", "a", "baseline"),
                  ("r", "b", "perturbed")), dict(a="optimum-a", b="optimum-b"))
        report = h.analyze(f, "r")
        self.assertEqual(report.direction, "ORDINARY_DIVERGENCE")
        self.assertEqual(report.iterated_divergences, ())

    def test_binary_and_ternary_divergences_preserve_semantic_multiplicity(self):
        f = frame("rABabcde", (("r", "A", "left"), ("r", "B", "right"),
                  ("A", "a", "a"), ("A", "b", "b"),
                  ("B", "c", "c"), ("B", "d", "d"), ("B", "e", "e")),
                  dict(a="a", b="b", c="c", d="d", e="e"))
        self.assertNotEqual(f.observed_pattern("A"), f.observed_pattern("B"))
        self.assertTrue(h.analyze(f, "r").iterated_divergences[0].pattern_variation)

    def test_one_more_fork_on_only_one_side_is_not_plural_divergence_of_divergences(self):
        f = frame("rAabc", (("r", "A", "continued"), ("r", "c", "settled"),
                  ("A", "a", "a"), ("A", "b", "b")), dict(a="a", b="b", c="c"))
        report = h.analyze(f, "r")
        self.assertEqual(report.iterated_divergences, ())
        self.assertEqual(report.direction, "ORDINARY_DIVERGENCE")

    def test_convergence_into_a_shared_divergence_is_not_two_independent_divergences(self):
        f, root = h.examples()["convergence-toward-divergence"]
        report = h.analyze(f, root)
        self.assertEqual(report.direction, "HYPERCHAOS")
        self.assertEqual(report.iterated_divergences, ())
        self.assertEqual(len(report.convergence_toward_divergence), 1)
        witness = report.convergence_toward_divergence[0]
        self.assertEqual((witness.convergence.join, witness.divergence_at), ("j", "j"))

    def test_resolved_boundary_has_hyperorder_direction_without_erasing_local_divergence(self):
        f, root = h.examples()["divergence-resolving-into-order"]
        report = h.analyze(f, root)
        self.assertEqual(report.direction, "HYPERORDER")
        self.assertEqual(report.settled_matter, ("shared-optimum",))
        self.assertEqual(len(report.iterated_divergences), 1)
        self.assertEqual(report.convergence_toward_divergence, ())
        self.assertTrue(report.convergences)

    def test_different_terminal_identifiers_do_not_force_different_matter(self):
        f = frame("rab", (("r", "a", "left"), ("r", "b", "right")),
                  dict(a="same", b="same"))
        self.assertEqual(h.analyze(f, "r").direction, "HYPERORDER")
        self.assertEqual(f.settled_capacity("r"), frozenset({"same"}))

    def test_unconnected_divergence_does_not_classify_selected_root(self):
        f = frame("rabc", (("a", "b", "b"), ("a", "c", "c")),
                  dict(r="r", b="b", c="c"))
        self.assertEqual(h.analyze(f, "r").direction, "ORDERLY")


class InvarianceAndWitnessTests(unittest.TestCase):
    def test_renaming_states_choices_and_matter_preserves_all_facets(self):
        for name, (f, root) in h.examples().items():
            rename = {state: f"state-{i}" for i, state in enumerate(reversed(f.states))}
            matter = {value: f"matter-{i}" for i, value in enumerate(sorted({m for _, m in f.outcomes}))}
            changed = h.ContinuationFrame(tuple(rename[s] for s in reversed(f.states)),
                tuple(h.Transition(rename[t.source], rename[t.target],
                                   None if t.choice is None else "renamed-" + t.choice)
                      for t in reversed(f.transitions)),
                tuple((rename[s], matter[m]) for s, m in reversed(f.outcomes)))
            old, new = h.analyze(f, root), h.analyze(changed, rename[root])
            with self.subTest(name=name):
                self.assertEqual(old.direction, new.direction)
                self.assertEqual(len(old.iterated_divergences), len(new.iterated_divergences))
                self.assertEqual(len(old.convergence_toward_divergence), len(new.convergence_toward_divergence))
                self.assertEqual(f.observed_pattern(root), changed.observed_pattern(rename[root]))
                self.assertEqual(sorted(w.pattern_variation for w in old.iterated_divergences),
                                 sorted(w.pattern_variation for w in new.iterated_divergences))

    def test_inserting_unary_presentation_nodes_preserves_semantics(self):
        for name, (f, root) in h.examples().items():
            new_states, arrows = list(f.states), []
            for i, t in enumerate(f.transitions):
                middle = "presentation-" + str(i)
                new_states.append(middle)
                arrows.extend((h.Transition(t.source, middle, t.choice),
                               h.Transition(middle, t.target)))
            changed = h.ContinuationFrame(tuple(new_states), tuple(arrows), f.outcomes)
            old, new = h.analyze(f, root), h.analyze(changed, root)
            with self.subTest(name=name):
                self.assertEqual(old.direction, new.direction)
                self.assertEqual(old.settled_matter, new.settled_matter)
                self.assertEqual(f.observed_pattern(root), changed.observed_pattern(root))
                self.assertEqual(len(old.iterated_divergences), len(new.iterated_divergences))
                self.assertEqual(len(old.convergence_toward_divergence), len(new.convergence_toward_divergence))

    def test_shared_join_survives_contraction_when_semantic_choices_are_retained(self):
        contracted = frame("rjab", (("r", "j", "left"), ("r", "j", "right"),
                           ("j", "a", "a"), ("j", "b", "b")), dict(a="a", b="b"))
        original, _ = h.examples()["convergence-toward-divergence"]
        old, new = h.analyze(original, "r"), h.analyze(contracted, "r")
        self.assertEqual(old.direction, new.direction)
        self.assertEqual(len(new.convergence_toward_divergence), 1)
        self.assertEqual(original.observed_pattern("r"), contracted.observed_pattern("r"))

    def test_pattern_equality_does_not_prove_equal_join_structure(self):
        merged = frame("rlqj", (("r", "l", "left"), ("r", "q", "right"),
                       ("l", "j", None), ("q", "j", None)), dict(j="m"))
        separate = frame("rlq", (("r", "l", "left"), ("r", "q", "right")),
                         dict(l="m", q="m"))
        self.assertEqual(merged.observed_pattern("r"), separate.observed_pattern("r"))
        self.assertTrue(h.analyze(merged, "r").convergences)
        self.assertFalse(h.analyze(separate, "r").convergences)

    def test_reported_iterated_witnesses_pass_local_checker(self):
        for f, root in h.examples().values():
            for witness in h.analyze(f, root).iterated_divergences:
                self.assertTrue(h.check_iterated_witness(f, witness))

    def test_forged_shared_lineage_wrong_endpoint_and_pattern_flag_are_rejected(self):
        f, root = h.examples()["balanced-divergence-of-divergences"]
        witness = h.analyze(f, root).iterated_divergences[0]
        for broken in (replace(witness, right_route=witness.left_route),
                       replace(witness, left_divergence="a"),
                       replace(witness, pattern_variation=True),
                       replace(witness, left_route=(h.Transition("r", "A", "forged"),))):
            self.assertFalse(h.check_iterated_witness(f, broken))
        self.assertFalse(h.check_iterated_witness(f, None))

    def test_root_is_part_of_direction_claim(self):
        f, root = h.examples()["balanced-divergence-of-divergences"]
        self.assertEqual(h.analyze(f, root).direction, "HYPERCHAOS")
        self.assertEqual(h.analyze(f, "A").direction, "ORDINARY_DIVERGENCE")
        self.assertEqual(h.analyze(f, "a").direction, "ORDERLY")


class RejectionTests(unittest.TestCase):
    def test_nodes_alone_do_not_declare_distinct_continuation_choices(self):
        with self.assertRaisesRegex(ValueError, "choice classes"):
            frame("rab", (("r", "a", None), ("r", "b", None)), dict(a="a", b="b"))

    def test_two_presentations_of_one_choice_do_not_count_twice(self):
        with self.assertRaisesRegex(ValueError, "choice classes"):
            frame("rab", (("r", "a", "same"), ("r", "b", "same")), dict(a="a", b="b"))

    def test_unknown_terminal_matter_is_rejected_not_assumed_convergent(self):
        with self.assertRaisesRegex(ValueError, "every terminal"):
            frame("ra", (("r", "a", None),), {})

    def test_a_cycle_is_outside_the_frame_not_a_proof_of_native_nonclosure(self):
        with self.assertRaisesRegex(ValueError, "cyclic continuation is OPEN"):
            frame("rab", (("r", "a", None), ("a", "r", "return"),
                           ("a", "b", "exit")), dict(b="b"))

    def test_duplicate_records_dangling_states_and_nonterminal_outcomes_are_rejected(self):
        for states, arrows, outcomes in (("ra", (("r", "a", None), ("r", "a", None)), dict(a="a")),
                                        ("ra", (("r", "missing", None),), dict(a="a")),
                                        ("ra", (("r", "a", None),), dict(r="r", a="a"))):
            with self.assertRaises(ValueError):
                frame(states, arrows, outcomes)

    def test_constructor_defensively_copies_input_and_maps_are_immutable(self):
        states = ["r", "a"]
        arrows = [h.Transition("r", "a")]
        outcomes = [["a", "a"]]
        f = h.ContinuationFrame(states, arrows, outcomes)
        states.clear(); arrows.clear(); outcomes[0][1] = "changed"
        self.assertEqual(f.settled_capacity("r"), frozenset({"a"}))
        with self.assertRaises(TypeError):
            f._settled["a"] = "changed"

    def test_undeclared_root_is_not_a_synthetic_orderly_pass(self):
        f, _ = h.examples()["orderly-continuation"]
        with self.assertRaises(KeyError):
            h.analyze(f, "missing")

    def test_input_budget_is_a_resource_limit_not_a_divergence_threshold(self):
        states = tuple("state-" + str(i) for i in range(257))
        with self.assertRaisesRegex(ValueError, "observation budget"):
            h.ContinuationFrame(states, (), tuple((s, s) for s in states))

    def test_analysis_pair_and_output_budgets_fail_without_a_synthetic_direction(self):
        f, root = h.examples()["balanced-divergence-of-divergences"]
        with self.assertRaisesRegex(h.AnalysisBudgetExceeded, "result UNKNOWN"):
            h.analyze(f, root, pair_budget=1)
        converging, root = h.examples()["divergence-resolving-into-order"]
        with self.assertRaisesRegex(h.AnalysisBudgetExceeded, "result UNKNOWN"):
            h.analyze(converging, root, witness_budget=1)

    def test_analysis_resource_options_are_not_unbounded_or_boolean(self):
        f, root = h.examples()["orderly-continuation"]
        for options in ({"pair_budget": True}, {"pair_budget": 20001},
                        {"witness_budget": 4097}, {"max_seconds": 0},
                        {"max_seconds": float("nan")}, {"max_seconds": float("inf")}):
            with self.assertRaises(ValueError):
                h.analyze(f, root, **options)

    def test_large_shared_continuation_uses_cached_patterns_and_rejects_output_growth(self):
        arrows = tuple(h.Transition("r", "j", "alternative-" + str(i)) for i in range(130))
        f = h.ContinuationFrame(("r", "j"), arrows, (("j", "j"),))
        self.assertIs(f.observed_pattern("r"), f.observed_pattern("r"))
        self.assertIs(f.reachable("r"), f.reachable("r"))
        with self.assertRaisesRegex(h.AnalysisBudgetExceeded, "result UNKNOWN"):
            h.analyze(f, "r")


class ExhaustiveFiniteOracleTests(unittest.TestCase):
    def test_all_1024_five_state_acyclic_frames_against_complete_path_oracle(self):
        """Independent oracle enumerates complete paths rather than graph search."""
        states = tuple("s" + str(i) for i in range(5))
        possible = tuple(combinations(states, 2))
        for mask in range(1 << len(possible)):
            arrows = tuple(h.Transition(a, b, "choice-" + b)
                           for i, (a, b) in enumerate(possible) if mask & (1 << i))
            outgoing = {s: tuple(t for t in arrows if t.source == s) for s in states}
            outcomes = {s: s for s in states if not outgoing[s]}
            f = h.ContinuationFrame(states, arrows, tuple(outcomes.items()))

            def paths(start):
                if not outgoing[start]:
                    return ((start,),)
                return tuple((start,) + p for t in outgoing[start] for p in paths(t.target))

            complete = {s: paths(s) for s in states}
            reach = {s: set().union(*(set(p) for p in complete[s])) for s in states}
            selected = reach["s0"]
            expected = set()
            for at in selected:
                for left, right in combinations(outgoing[at], 2):
                    common = reach[left.target] & reach[right.target]
                    first = []
                    for target in (left.target, right.target):
                        found = set()
                        for path in complete[target]:
                            for state in path:
                                if state in common:
                                    break
                                if len(outgoing[state]) > 1:
                                    found.add(state)
                                    break
                        first.append(found)
                    expected.update((at, a, b) for a in first[0] for b in first[1])
            report = h.analyze(f, "s0")
            actual = {(w.at, w.left_divergence, w.right_divergence)
                      for w in report.iterated_divergences}
            self.assertEqual(actual, expected, mask)
            self.assertEqual(f.settled_capacity("s0"),
                             frozenset(path[-1] for path in complete["s0"]), mask)
            for witness in report.iterated_divergences:
                self.assertTrue(h.check_iterated_witness(f, witness), mask)


if __name__ == "__main__":
    unittest.main()
