from app.content.checks import polarity_ok, run_checks
from app.content.rules import evaluate, referenced_slot_ids


def test_authoring_checks_pass(bundle):
    findings = run_checks(bundle)
    assert findings == [], "\n".join(str(f) for f in findings)


def test_p7_polarity():
    assert not polarity_ok("No chest pain?")
    assert not polarity_ok("You're not still drinking, are you?")
    assert not polarity_ok("You don't get breathless, do you?")
    assert polarity_ok("How much are you drinking at the moment?")
    assert polarity_ok("Does the pain go anywhere else?")


def test_rule_evaluation_missing_slot_is_undecidable():
    expr = "cp.onset == 'abrupt' and cp.quality in ['tearing', 'ripping'] and 'back' in cp.radiation"
    assert referenced_slot_ids(expr) == ["cp.onset", "cp.quality", "cp.radiation"]
    r = evaluate(expr, {"cp.onset": "abrupt", "cp.quality": "tearing"})
    assert not r.fired and r.missing == ["cp.radiation"]
    r = evaluate(expr, {"cp.onset": "abrupt", "cp.quality": "tearing", "cp.radiation": ["back", "both_arms"]})
    assert r.fired
    r = evaluate(expr, {"cp.onset": "gradual", "cp.quality": "tearing", "cp.radiation": ["back"]})
    assert not r.fired and r.missing == []


def test_every_module_has_closing_and_no_suppressible_rules(bundle):
    for m in bundle.modules.values():
        if m.kind == "presentation":
            assert m.closing is not None
        assert all(not rf.suppressible for rf in m.red_flags)
