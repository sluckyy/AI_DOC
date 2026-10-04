from app.content.checks import polarity_ok, run_checks
from app.content.rules import evaluate, referenced_slot_ids


def test_authoring_checks_pass(bundle):
    findings = run_checks(bundle)
    assert findings == [], "\n".join(str(f) for f in findings)


def _first_gates_owner(bundle):
    """A context or module slot with a non-empty `gates` list, and its owner name."""
    for s in bundle.context.slots:
        if s.gates:
            return "context", s.id
    for name, m in bundle.modules.items():
        for s in m.slots:
            if s.gates:
                return name, s.id
    raise AssertionError("fixture content has no slot with `gates` set; test needs updating")


def _first_route_to_slot(bundle):
    for name, m in bundle.modules.items():
        for s in m.slots:
            if s.route_to:
                return name, s
    raise AssertionError("fixture content has no slot with `route_to` set; test needs updating")


def test_c12_gates_references_unknown_module(bundle):
    b = bundle.model_copy(deep=True)
    owner, slot_id = _first_gates_owner(b)
    slots = b.context.slots if owner == "context" else b.modules[owner].slots
    slot = next(s for s in slots if s.id == slot_id)
    slot.gates = ["not_a_real_module"]
    findings = run_checks(b)
    assert any(f.check == "C12" and "gates references unknown module" in f.message for f in findings), findings


def test_c12_gating_references_unknown_slot(bundle):
    b = bundle.model_copy(deep=True)
    name, m = next((n, m) for n, m in b.modules.items() if m.kind == "presentation")
    m.gating = ["gate.not_a_real_slot"]
    findings = run_checks(b)
    assert any(f.check == "C12" and f.where == name and "gating references unknown gate slot" in f.message for f in findings), findings


def test_c11_routes_to_unknown_module(bundle):
    b = bundle.model_copy(deep=True)
    owner, slot = _first_route_to_slot(b)
    option_id = next(iter(slot.route_to))
    slot.route_to[option_id] = "not_a_real_module"
    findings = run_checks(b)
    assert any(f.check == "C11" and "routes to unknown module" in f.message for f in findings), findings


def test_c11_routes_to_non_presentation_module(bundle):
    b = bundle.model_copy(deep=True)
    owner, slot = _first_route_to_slot(b)
    option_id = next(iter(slot.route_to))
    slot.route_to[option_id] = "review_of_systems"   # a real module, but kind=closing, not presentation
    findings = run_checks(b)
    assert any(f.check == "C11" and "non-presentation module" in f.message for f in findings), findings


def test_c11_routes_to_blocked_module(bundle):
    b = bundle.model_copy(deep=True)
    owner, slot = _first_route_to_slot(b)
    option_id = next(iter(slot.route_to))
    target = slot.route_to[option_id]
    b.modules[target].status = "blocked"
    findings = run_checks(b)
    assert any(f.check == "C11" and "routes to blocked module" in f.message for f in findings), findings


def test_c11_route_to_key_not_a_defined_option(bundle):
    b = bundle.model_copy(deep=True)
    owner, slot = _first_route_to_slot(b)
    target = next(iter(slot.route_to.values()))
    slot.route_to["not_a_real_option"] = target
    findings = run_checks(b)
    assert any(f.check == "C11" and "is not a defined option on this slot" in f.message for f in findings), findings


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
