"""Static R3 integrity audit checks. No SQL, Linux agent, or privilege is executed."""
from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "DOCUMENTATION"
EV = DOC / "evidence"
RISKS = {f"RISK-{i:03d}" for i in range(33, 37)}
FINDINGS = {f"AUDIT-FP-{i:04d}" for i in range(33, 37)}
TESTS = {f"R3-AUDIT-TEST-{i:03d}" for i in range(1, 9)}
NEEDED = {
    "denied_admission_produces_redacted_audit_without_creating_job",
    "accepted_job_audit_has_real_job_reference",
    "fencing_generation_must_not_reset_on_lease_row_delete",
    "database_restore_invalidates_pre_restore_effect_authority",
    "inbox_receipt_is_not_external_effect",
    "uncertain_effect_forces_reconciliation_before_retry",
    "verified_server_scope_required_even_with_RLS",
    "no_generic_shell_or_privileged_apply_from_candidate",
}


def load(name: str):
    return json.loads((EV / name).read_text(encoding="utf-8"))


def table(model: dict, name: str) -> dict:
    matches = [t for t in model["candidate_tables"] if t["name"] == name]
    if len(matches) != 1:
        raise AssertionError(f"expected one candidate table {name}")
    return matches[0]


def safety_errors(db: dict, transitions: dict, execution: dict) -> list[str]:
    """Contract-only checks; intentional mutations in tests must fail closed."""
    problems = []
    for name in NEEDED:
        if db.get("required_invariants_before_migration", {}).get(name) is not True:
            problems.append(f"required invariant missing: {name}")
    audit = table(db, "fp_job_audit_events")
    fields = {x["column"]: x for x in audit["columns"]}
    if not {"job_id", "request_ref", "subject_kind", "decision_code"} <= set(fields):
        problems.append("audit subject fields missing")
    if fields.get("job_id", {}).get("nullability") != "CANDIDATE_NULLABLE_FOR_DENIED_ADMISSION":
        problems.append("denied admissions require nullable job FK")
    for guard in (
        "denied_admission_has_no_accepted_job_and_nullable_job_ref",
        "all_audit_events_bind_server_generated_request_ref",
        "accepted_job_audit_event_requires_valid_job_ref",
    ):
        if guard not in audit["guards"]:
            problems.append("audit guard missing")
    lease = table(db, "fp_resource_leases")
    if "fencing_epoch_ref" not in {x["column"] for x in lease["columns"]}:
        problems.append("restore epoch design placeholder missing")
    for guard in (
        "monotonic_fencing_generation_cannot_reset_on_lease_row_recreation",
        "backup_restore_requires_independent_epoch_reconciliation_before_apply",
        "lease_expiry_alone_never_grants_reexecution",
    ):
        if guard not in lease["guards"]:
            problems.append(f"lease guard missing: {guard}")
    inbox = table(db, "fp_agent_inbox")
    fields = {x["column"]: x for x in inbox["columns"]}
    if not {"processing_state", "effect_verdict_ref", "fencing_generation"} <= set(fields):
        problems.append("inbox receipt versus effect fields missing")
    if set(fields.get("processing_state", {}).get("candidate_values", [])) != {
        "RECEIVED", "IN_PROGRESS", "EFFECT_UNCERTAIN",
        "EFFECT_VERIFIED", "PROVEN_NO_EFFECT",
    }:
        problems.append("inbox state set missing uncertain effect")
    for guard in ("inbox_receipt_is_transport_only_not_linux_effect",
                  "effect_verified_requires_separately_persisted_observation",
                  "duplicate_delivery_never_blindly_reapplies"):
        if guard not in inbox["guards"]:
            problems.append(f"inbox safety guard missing: {guard}")
    intent = table(db, "fp_operation_intents")
    for guard in ("scope_kind_scope_ref_resource_kind_resource_ref_all_nonnull",
                  "scope_derived_from_verified_server_authorization_not_payload_or_session_GUC_alone"):
        if guard not in intent["guards"]:
            problems.append(f"scope guard missing: {guard}")
    checks = transitions.get("requirements", {})
    for key in ("inbox_received_is_proof_of_linux_effect",
                "restored_database_may_reauthorize_stale_fence",
                "uncertain_outbox_delivery_can_be_replayed_blindly"):
        if checks.get(key) is not False:
            problems.append(f"unsafe transition permission: {key}")
    if checks.get("persisted_job_requires_committed_acceptance") is not True:
        problems.append("uncommitted jobs could appear accepted")
    if execution.get("effect_boundary_fence_epoch_reconciliation_approved") is not False:
        problems.append("effect boundary epoch falsely approved")
    for key in ("post_restore_privileged_apply_authorized",
                "inbox_receipt_as_effect_proof_authorized",
                "tenant_scope_from_unverified_actor_claim_authorized"):
        if execution.get(key) is not False:
            problems.append(f"unsafe execution permission: {key}")
    if set(execution["privileged_operations_explicitly_blocked"]) != {
        "ACT-FP-0005", "ACT-FP-0007"
    }:
        problems.append("privileged operations became available")
    return problems


class R3IntegrityAuditDocumentTests(unittest.TestCase):
    def setUp(self):
        self.db = load("candidate-r3-physical-data-model-v1.json")
        self.transitions = load("candidate-job-transitions-v1.json")
        self.execution = load("candidate-typed-execution-guards-v1.json")
        self.registry = load("r3-job-integrity-review-v1.json")

    def test_bilingual_review_metadata_and_open_findings(self):
        for lang in ("fr", "en"):
            value = (DOC / lang / "19-audits-risks/r3-job-integrity-audit.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("id=FP-19-R3-JOB-INTEGRITY-AUDIT revision=1 status=specified", value)
            for item in RISKS | FINDINGS:
                self.assertIn(item, value)
            self.assertIn("OPEN", value)
            self.assertIn("PLANNED", value)
            self.assertIn("Q1–Q170", value)
            self.assertIn("DOC-GAP-004/005/006", value)

    def test_all_eight_future_scenarios_planned_and_mirrored(self):
        orders = []
        for lang in ("fr", "en"):
            value = (DOC / lang / "19-audits-risks/r3-job-integrity-audit.md").read_text()
            rows = [r for r in value.splitlines() if r.startswith("| " + chr(96) + "R3-AUDIT-")]
            ids = [re.match(r"^\| .(R3-AUDIT-TEST-\d{3}).", row).group(1) for row in rows]
            self.assertEqual(len(rows), 8)
            self.assertEqual(set(ids), TESTS)
            self.assertTrue(all(r.strip().endswith("| **PLANNED** |") for r in rows))
            orders.append(ids)
        self.assertEqual(orders[0], orders[1])

    def test_machine_readable_review_stays_unapproved(self):
        r = self.registry
        self.assertEqual(r["status"], "REVIEW_REQUIRED_NOT_APPROVED")
        for field in ("database_migration_approved", "privileged_executor_authorized",
                      "source_code_imported", "real_sql_tests_performed",
                      "real_linux_tests_performed"):
            self.assertIs(r[field], False)
        self.assertEqual(len(r["findings"]), 4)
        self.assertEqual({f["id"] for f in r["findings"]}, FINDINGS)
        self.assertEqual({f["risk_id"] for f in r["findings"]}, RISKS)
        self.assertEqual({tid for f in r["findings"] for tid in f["required_test_ids"]},
                         TESTS)
        for f in r["findings"]:
            self.assertEqual(f["status"], "OPEN")
            self.assertEqual(f["implementation_status"], "NOT_IMPLEMENTED")
            self.assertIs(f["no_automatic_adoption"], True)
        self.assertEqual(set(r["blocked_operations"]), {"ACT-FP-0005", "ACT-FP-0007"})

    def test_candidate_schema_addresses_findings_without_claiming_fix(self):
        self.assertIs(self.db["not_sql_migration"], True)
        self.assertIs(self.db["authorized_to_create_tables"], False)
        self.assertEqual(set(self.db["review_findings"]), FINDINGS)
        self.assertEqual(set(self.db["required_invariants_before_migration"]), NEEDED)
        self.assertEqual(safety_errors(self.db, self.transitions, self.execution), [])

    def test_contract_mutation_does_not_silently_remove_safety_guards(self):
        mutations = [
            ("denied audit", lambda d, t, e: d["required_invariants_before_migration"].update(
                denied_admission_produces_redacted_audit_without_creating_job=False)),
            ("restored fencing", lambda d, t, e: d["required_invariants_before_migration"].update(
                database_restore_invalidates_pre_restore_effect_authority=False)),
            ("double effect", lambda d, t, e: t["requirements"].update(
                inbox_received_is_proof_of_linux_effect=True)),
            ("tenant spoof", lambda d, t, e: e.update(
                tenant_scope_from_unverified_actor_claim_authorized=True)),
            ("root privilege", lambda d, t, e: e.update(
                privileged_operations_explicitly_blocked=[])),
        ]
        for name, change in mutations:
            with self.subTest(mutation=name):
                d, t, e = map(copy.deepcopy, (self.db, self.transitions, self.execution))
                change(d, t, e)
                self.assertTrue(safety_errors(d, t, e), name)

    def test_original_physical_count_not_misreported_as_approved(self):
        self.assertEqual(len(self.db["candidate_tables"]), 8)
        self.assertTrue(all(t["status"] == "CANDIDATE_NOT_APPROVED"
                            for t in self.db["candidate_tables"]))
        for lang in ("fr", "en"):
            value = (DOC / lang / "09-database/physical-jobs-model-r3.md").read_text()
            for risk in RISKS:
                self.assertIn(risk, value)
            self.assertIn("fencing_epoch_ref", value)
            self.assertIn("processing_state", value)
            self.assertIn("request_ref", value)
            self.assertIn("DOC-GAP-004/005/006", value)


if __name__ == "__main__":
    unittest.main()
