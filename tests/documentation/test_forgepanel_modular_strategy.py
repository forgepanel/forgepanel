"""Static metadata-only adversarial tests. No installed Core or VM is exercised."""
from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
SPEC=importlib.util.spec_from_file_location('modular_checker',ROOT/'scripts/check_forgepanel_modular_strategy.py')
CHECKER=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)
MODULES=json.loads((ROOT/CHECKER.MODULE_PATH).read_text())
RELEASES=json.loads((ROOT/CHECKER.RELEASE_PATH).read_text())
QA=json.loads((ROOT/CHECKER.QA_PATH).read_text())


class RegistryTests(unittest.TestCase):
    def module_change(self,fn):
        item=copy.deepcopy(MODULES)
        fn(item)
        with self.assertRaises(ValueError): CHECKER.validate_modules(item)

    def row(self,data,identifier):
        return next(x for x in data['modules'] if x['id']==identifier)

    def test_source_registry_valid(self):
        self.assertEqual(CHECKER.validate_modules(MODULES)['catalog_entries'],40)
    def test_rule_mandatory(self):
        self.module_change(lambda d:d['rules'].__setitem__('core_can_boot_and_host_without_optional_modules',False))
    def test_no_generic_root_shell(self):
        self.module_change(lambda d:d['rules'].__setitem__('no_generic_privileged_shell',False))
    def test_mfa_remains_optional(self):
        self.module_change(lambda d:d['rules'].__setitem__('mfa_optional',False))
    def test_no_hub_dependency(self):
        self.module_change(lambda d:d['rules'].__setitem__('independent_hub_not_mandatory',False))
    def test_no_publication_claim(self):
        self.module_change(lambda d:d.__setitem__('runtime_state_evidence','VERIFIED'))
    def test_no_false_git_source_status(self):
        self.module_change(lambda d:d.__setitem__('core_source_state','MERGED'))
    def test_missing_module(self):
        self.module_change(lambda d:d['modules'].pop())
    def test_duplicate_module(self):
        self.module_change(lambda d:d['modules'][-1].__setitem__('id',d['modules'][0]['id']))
    def test_early_core_depends_on_optional(self):
        self.module_change(lambda d:self.row(d,'core.identity')['depends_on'].append('publisher.hub'))
    def test_cycle(self):
        self.module_change(lambda d:self.row(d,'core.bootstrap')['depends_on'].append('core.identity'))
    def test_missing_dependency(self):
        self.module_change(lambda d:self.row(d,'apps.one_click')['depends_on'].append('does.not_exist'))
    def test_no_optional_blocks_core(self):
        self.module_change(lambda d:self.row(d,'container.docker_apps').__setitem__('blocking_when_unavailable',True))
    def test_required_core_cannot_be_optional(self):
        self.module_change(lambda d:self.row(d,'core.rbac').__setitem__('optional',True))
    def test_required_core_cannot_be_deferred(self):
        self.module_change(lambda d:self.row(d,'core.backup').__setitem__('target_release','v1.2.0'))
    def test_module_catalog_outage_does_not_stop_hosting(self):
        self.module_change(lambda d:self.row(d,'core.module_catalog').__setitem__('blocking_when_unavailable',True))
    def test_no_runtime_activation_claim(self):
        self.module_change(lambda d:self.row(d,'apps.one_click').__setitem__('can_execute',True))
    def test_no_fake_available_label(self):
        self.module_change(lambda d:self.row(d,'apps.one_click').__setitem__('ui_display_status','AVAILABLE'))
    def test_no_fake_developing_status(self):
        self.module_change(lambda d:self.row(d,'container.docker_apps').__setitem__('development_status','DEVELOPING'))
    def test_no_claimed_vm_verification(self):
        self.module_change(lambda d:self.row(d,'container.docker_apps').__setitem__('actual_verification_status','PASS'))
    def test_one_click_does_not_require_hub(self):
        self.module_change(lambda d:self.row(d,'apps.one_click')['depends_on'].append('publisher.hub'))
    def test_one_click_does_not_require_docker(self):
        self.module_change(lambda d:self.row(d,'apps.one_click')['depends_on'].append('container.docker_apps'))
    def test_docker_podman_driver_independence(self):
        self.module_change(lambda d:self.row(d,'container.docker_apps')['depends_on'].append('container.podman_apps'))
    def test_one_click_licensing_must_remain_free(self):
        self.module_change(lambda d:self.row(d,'apps.one_click').__setitem__('license_entitlement_policy','PREMIUM'))
    def test_future_optional_commercial_terms_stay_open(self):
        self.module_change(lambda d:self.row(d,'security.waf').__setitem__('license_entitlement_policy','CORE_FREE_ALWAYS'))
    def test_core_free_unrestricted_by_hub(self):
        self.module_change(lambda d:self.row(d,'core.identity').__setitem__('license_entitlement_policy','REQUIRES_HUB'))
    def test_hub_after_abi(self):
        self.module_change(lambda d:self.row(d,'publisher.hub')['depends_on'].remove('extensions.abi'))
    def test_hub_private_owner(self):
        self.module_change(lambda d:self.row(d,'publisher.hub').__setitem__('owner_scope','core-public'))
    def test_unknown_release_target(self):
        self.module_change(lambda d:self.row(d,'container.docker_apps').__setitem__('target_release','v9.0.0'))
    def test_future_dependency(self):
        self.module_change(lambda d:self.row(d,'apps.one_click')['depends_on'].append('hosting.staging'))
    def test_manifest_scope_must_be_complete(self):
        self.module_change(lambda d:d['required_manifest_fields'].remove('permissions'))
    def test_decision_reference_range_checked(self):
        self.module_change(lambda d:self.row(d,'apps.one_click')['related_decisions'].append('Q999'))
    def test_owner_branches_preserved(self):
        self.module_change(lambda d:d['release_policy']['git_promotion_branches'].remove('production'))
    def test_r5_r6_order(self):
        self.module_change(lambda d:d['release_policy'].__setitem__('r6_hub_after_r5',False))


class ReleaseTests(unittest.TestCase):
    def mutate(self,fn):
        d=copy.deepcopy(RELEASES)
        fn(d)
        with self.assertRaises(ValueError):CHECKER.validate_releases(d)
    def test_release_registry_valid(self):
        self.assertEqual(CHECKER.validate_releases(RELEASES)['stage_count'],9)
    def test_semver_examples_increasing(self):
        tags=[x['example_tag'] for x in RELEASES['stages']]
        self.assertEqual(tags,sorted(tags,key=CHECKER.release_sort_key))
    def test_old_bad_lexical_order_rejected(self):
        self.mutate(lambda d:d['stages'][1].__setitem__('example_tag','v1.0.0-alpha.1'))
    def test_invalid_numeric_zero_prerelease(self):
        with self.assertRaises(ValueError): CHECKER.release_sort_key('v1.0.0-01.prealpha.1')
    def test_stage_omission_blocked(self):
        self.mutate(lambda d:d['stages'].pop())
    def test_no_published_claim(self):
        self.mutate(lambda d:d['stages'][-1].__setitem__('published',True))
    def test_no_deployed_claim(self):
        self.mutate(lambda d:d['stages'][-1].__setitem__('deployed',True))
    def test_r2_cannot_claim_installer(self):
        self.mutate(lambda d:d['stages'][1].__setitem__('minimum_criteria','full Linux installer operational'))
    def test_sequence_is_r1_r6(self):
        self.mutate(lambda d:d.__setitem__('q120_order',['R1','R2','R4','R3','R5','R6']))
    def test_version_major_only_on_breaks(self):
        self.mutate(lambda d:d.__setitem__('major_semver_only_when_breaking_changes',False))
    def test_security_gate_immutable(self):
        self.mutate(lambda d:d.__setitem__('security_gates_non_waivable',False))
    def test_production_branch_preserved(self):
        self.mutate(lambda d:d['git_flow'].remove('production'))


class QATests(unittest.TestCase):
    def test_planned_not_executed(self):
        self.assertEqual(CHECKER.validate_qa(QA)['executed'],0)
    def test_false_pass_refused(self):
        d=copy.deepcopy(QA);d['tests'][0]['execution_status']='PASS'
        with self.assertRaises(ValueError):CHECKER.validate_qa(d)
    def test_forged_evidence_refused(self):
        d=copy.deepcopy(QA);d['tests'][0]['evidence']='invented'
        with self.assertRaises(ValueError):CHECKER.validate_qa(d)
    def test_duplication_refused(self):
        d=copy.deepcopy(QA);d['tests'][1]['id']=d['tests'][0]['id']
        with self.assertRaises(ValueError):CHECKER.validate_qa(d)
    def test_missing_cases_refused(self):
        d=copy.deepcopy(QA);d['tests'].pop()
        with self.assertRaises(ValueError):CHECKER.validate_qa(d)


class DocumentationTests(unittest.TestCase):
    def test_parity_metadata(self):
        self.assertEqual(CHECKER.validate_bilingual_docs(ROOT)['bilingual_document_pairs'],5)
    def test_complete_bundle(self):
        r=CHECKER.check(ROOT)
        self.assertEqual(r['status'],'PASS_DOCUMENTARY_CONSISTENCY_ONLY')
        self.assertFalse(r['runtime_feature_execution_authorized'])
        self.assertFalse(r['github_merged'])


if __name__=='__main__':unittest.main()