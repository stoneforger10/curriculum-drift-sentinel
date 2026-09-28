import hashlib
import json


BASE = "Objective method: plan a controlled trial. Objective evidence: record measured observations."
CHANGED = "Objective method: plan a controlled trial. Objective evidence: observations are optional."


def h(text):
    return hashlib.sha256(text.encode()).hexdigest()


def prepare(c, vm, owner):
    vm.sender = owner
    c.register_policy("pilot", "method,evidence", "https://archive.example.org/base", h(BASE),
                      "https://live.example.org/current")


def test_material_change_pauses_permissionlessly(direct_vm, direct_deploy, direct_alice, direct_bob):
    c = direct_deploy("contracts/CurriculumDriftSentinel.py")
    prepare(c, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    direct_vm.mock_web(r"archive\.example\.org/base", {"status": 200, "body": BASE})
    direct_vm.mock_web(r"live\.example\.org/current", {"status": 200, "body": CHANGED})
    direct_vm.mock_llm(r".*compare learner-facing requirements.*", json.dumps({"method": "UNCHANGED", "evidence": "MATERIAL"}))
    c.audit("pilot", "round-1")
    assert json.loads(c.get_policy("pilot"))["state"] == "PAUSED"
    assert json.loads(c.get_audit("pilot", "round-1"))["decision"] == "PAUSE"
    with direct_vm.expect_revert("audit replay"):
        c.audit("pilot", "round-1")


def test_same_content_continues(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/CurriculumDriftSentinel.py")
    prepare(c, direct_vm, direct_alice)
    direct_vm.mock_web(r"archive\.example\.org/base", {"status": 200, "body": BASE})
    direct_vm.mock_web(r"live\.example\.org/current", {"status": 200, "body": BASE})
    c.audit("pilot", "same")
    assert json.loads(c.get_audit("pilot", "same"))["decision"] == "CONTINUE"


def test_bad_baseline_fails_closed(direct_vm, direct_deploy, direct_alice):
    c = direct_deploy("contracts/CurriculumDriftSentinel.py")
    prepare(c, direct_vm, direct_alice)
    direct_vm.mock_web(r"archive\.example\.org/base", {"status": 200, "body": "tampered"})
    direct_vm.mock_web(r"live\.example\.org/current", {"status": 200, "body": CHANGED})
    c.audit("pilot", "bad")
    assert json.loads(c.get_audit("pilot", "bad"))["decision"] == "INCONCLUSIVE"
    assert json.loads(c.get_policy("pilot"))["state"] == "ACTIVE"
