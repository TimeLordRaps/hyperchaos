"""Independent finite counterexamples for the proposed Hyperchaos frame."""

import unittest

import hyperchaos
from hyperchaos import (MISSING, REALIGNMENT, RULING, USAGES, Ruling, Standing,
                        Usage, resolve_sense)


def ruling(**overrides):
    fields = dict(gloss="a proposed sense", said="his words", source="Tyler Roost, a date",
                  builds_on="authority-disruption")
    fields.update(overrides)
    return Ruling(**fields)


class SenseTests(unittest.TestCase):
    def test_hyperchaos_has_no_sense_until_tyler_rules(self):
        self.assertIsNone(RULING)
        with self.assertRaises(KeyError):
            resolve_sense("hyperchaos")

    def test_chaos_is_never_hyperchaos(self):
        for term in ("chaos", "Hyperchaos", "hyper-chaos", ""):
            with self.assertRaises(KeyError, msg=repr(term)):
                resolve_sense(term, ruling())

    def test_every_usage_names_its_source_and_standing(self):
        self.assertEqual(len({u.name for u in USAGES}), len(USAGES))
        for usage in USAGES:
            self.assertTrue(usage.term and usage.gloss and usage.source, usage.name)
            self.assertIsInstance(usage.standing, Standing)

    def test_recording_a_usage_adopts_nothing(self):
        for usage in USAGES:
            with self.assertRaises(KeyError, msg=usage.name):
                resolve_sense(usage.term)

    def test_the_dynamics_term_is_recorded_as_external(self):
        same_word = [u for u in USAGES if u.term == "hyperchaos"]
        self.assertEqual(len(same_word), 1)
        self.assertIs(same_word[0].standing, Standing.EXTERNAL)
        self.assertIn("Lyapunov", same_word[0].gloss)

    def test_tylers_statements_are_recorded_open(self):
        for statement in (REALIGNMENT, MISSING):
            self.assertEqual(statement.status, "OPEN")
            self.assertIn("hyperchaos", statement.said)
            self.assertIn("hyperchaos", statement.relates)

    def test_no_grounding_dynamics_or_clock_is_exported(self):
        for forbidden in ("ground", "grounds", "grounded_in", "realign", "lyapunov",
                          "exponents", "attractor", "time", "clock", "index",
                          "duration", "step"):
            self.assertFalse(hasattr(hyperchaos, forbidden), forbidden)


class RulingTests(unittest.TestCase):
    def test_a_ruling_declares_a_new_sense_not_an_alias(self):
        r = ruling()
        sense = resolve_sense("hyperchaos", r)
        self.assertEqual(sense.name, "hyperchaos")
        self.assertEqual((sense.gloss, sense.source, sense.builds_on),
                         (r.gloss, r.source, "authority-disruption"))
        self.assertNotIsInstance(sense, Usage)

    def test_building_on_the_external_term_must_acknowledge_it(self):
        external = next(u.name for u in USAGES if u.standing is Standing.EXTERNAL)
        with self.assertRaises(ValueError):
            ruling(builds_on=external)
        sense = resolve_sense("hyperchaos", ruling(builds_on=external, acknowledges_external=True))
        self.assertEqual(sense.builds_on, external)

    def test_an_acknowledgement_must_name_an_external_usage(self):
        with self.assertRaises(ValueError):
            ruling(builds_on=None, acknowledges_external=True)
        with self.assertRaises(ValueError):
            ruling(acknowledges_external=True)

    def test_a_ruling_builds_only_on_a_recorded_usage(self):
        with self.assertRaises(ValueError):
            ruling(builds_on="noise")
        self.assertIsNone(resolve_sense("hyperchaos", ruling(builds_on=None)).builds_on)

    def test_a_ruling_states_quotes_and_sources(self):
        for field in ("gloss", "said", "source"):
            for bad in ("", "   ", 3):
                with self.assertRaises(ValueError, msg=(field, bad)):
                    ruling(**{field: bad})
        with self.assertRaises(ValueError):
            ruling(acknowledges_external="yes")

    def test_only_a_ruling_resolves(self):
        with self.assertRaises(TypeError):
            resolve_sense("hyperchaos", "his ruling")


if __name__ == "__main__":
    unittest.main()
