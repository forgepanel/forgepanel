#!/usr/bin/env python3
"""Check candidate ForgePanel module/release metadata. Never authorize execution."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = 'DOCUMENTATION/evidence/forgepanel-modular-roadmap-proposed-v2.json'
RELEASE_PATH = 'DOCUMENTATION/evidence/forgepanel-release-trains-proposed-v2.json'
QA_PATH = 'DOCUMENTATION/evidence/forgepanel-modular-qa-proposed-v1.json'
RELEASES = {'v1.0.0', 'v1.1.0', 'v1.2.0', 'v1.3.0', 'v1.4.0', 'v2.0.0', 'v2.1.0'}
STAGES = ['DEV', 'PREALPHA', 'ALPHA_INTERNAL', 'ALPHA_CLOSED', 'PREVIEW',
          'BETA_PRIVATE', 'BETA_PUBLIC', 'RC', 'GA']
DOCS = {
    '00-project-control/modular-development-strategy.md': 'FP-00-MODULAR-STRATEGY',
    '04-modules/progressive-release-policy.md': 'FP-04-PROGRESSIVE',
    '13-tests-quality/modular-release-gates.md': 'FP-13-MODULAR-GATES',
    '14-devops-releases/release-lifecycle-plan.md': 'FP-14-RELEASE-LIFECYCLE',
    '19-audits-risks/modular-strategy-reconciliation.md': 'FP-19-MODULAR-RECONCILIATION',
}
SEMVER = re.compile(r'^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$')
MOD_ID = re.compile(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)+')
QA_ID = re.compile(r'MOD-QA-\d{3}')
META = re.compile(r'^<!-- forgepanel-doc id=([A-Z0-9-]+) revision=(\d+) status=([a-z-]+) -->', re.M)
MANDATORY_RULES = {
    'core_can_boot_and_host_without_optional_modules', 'optional_module_must_not_break_login_site_restore',
    'no_generic_privileged_shell', 'critical_security_and_recovery_cannot_be_deferred',
    'mfa_optional', 'one_click_native_free_and_no_containers', 'docker_podman_separate_engines',
    'development_status_does_not_authorize_install', 'catalog_visibility_is_not_availability_or_activation',
    'all_release_targets_are_provisional', 'no_automatic_git_or_production_promotion',
    'project_specific_branch_workflow_precedence', 'independent_hub_not_mandatory',
}
MANIFEST_FIELDS = {
    'id', 'owner', 'type', 'status', 'business_value', 'target_release', 'core_version_range',
    'api_contract_version', 'dependencies', 'conflicts', 'permissions', 'data_migrations',
    'feature_flag', 'default_enabled', 'installable', 'public_visibility',
    'distribution_channel', 'rollback_strategy', 'tests', 'documentation',
    'support_level', 'license_entitlement',
}


def reject(msg: str) -> None:
    raise ValueError(msg)


def release_sort_key(tag: str) -> tuple:
    """Minimal SemVer ordering, used only on fixed candidate example tags."""
    match = SEMVER.fullmatch(tag)
    if not match:
        reject('invalid_semver')
    version = tuple(int(match.group(i)) for i in (1, 2, 3))
    prerelease = match.group(4)
    if prerelease is None:
        return version + (1, ())
    tokens = prerelease.split('.')
    if any(t.isdigit() and len(t) > 1 and t[0] == '0' for t in tokens):
        reject('leading_zero_in_numeric_prerelease')
    precedence = tuple((0, int(x)) if x.isdigit() else (1, x) for x in tokens)
    return version + (0, precedence)


def validate_modules(data: Any) -> dict:
    if not isinstance(data, dict) or data.get('schema_version') != 'forgepanel.modular-roadmap/proposal-v2':
        reject('invalid_candidate_registry')
    if data.get('decision_status') != 'PROPOSED_FOR_PROJECT_RECONCILIATION':
        reject('unapproved_decision_promotion')
    if data.get('core_source_state') != 'RECOVERED_OUTSIDE_REPOSITORY_NOT_MERGED':
        reject('false_git_source_status')
    if data.get('runtime_state_evidence') != 'NOT_VERIFIED':
        reject('unverified_runtime_claim')
    if not MANDATORY_RULES.issubset(set(data.get('rules', {}))) or any(data['rules'][key] is not True for key in MANDATORY_RULES):
        reject('missing_mandatory_rule')
    if data.get('release_policy', {}).get('git_promotion_branches') != [
        'features/*', 'develop', 'stable', 'main', 'production']:
        reject('owner_git_policy_changed')
    if data.get('release_policy', {}).get('r5_api_after_r4') is not True or data['release_policy'].get('r6_hub_after_r5') is not True:
        reject('abi_hub_sequence_broken')
    if set(data.get('required_manifest_fields', [])) != MANIFEST_FIELDS:
        reject('missing_manifest_contract_fields')
    modules = data.get('modules')
    if not isinstance(modules, list) or len(modules) != 40:
        reject('catalog_not_preserved')
    found: dict[str, dict] = {}
    for entry in modules:
        if not isinstance(entry, dict):
            reject('invalid_module_entry')
        module_id = entry.get('id')
        if not isinstance(module_id, str) or not MOD_ID.fullmatch(module_id) or module_id in found:
            reject('invalid_or_duplicate_module_id')
        found[module_id] = entry
        if entry.get('kind') not in {'core-capability', 'optional-module', 'publisher-extension'}:
            reject('invalid_module_kind')
        if entry.get('target_release') not in RELEASES:
            reject('unsupported_release_target')
        if entry.get('priority') not in {'MUST', 'LATER'}:
            reject('invalid_priority')
        if entry.get('development_status') not in {'SPECIFIED', 'ROADMAP'}:
            reject('unverified_development_status')
        for key, value in {
            'runtime_artifact_present': False, 'actual_verification_status': 'NOT_RUN',
            'package_compatible_verified': False, 'actual_release_status': 'NOT_RELEASED',
            'ui_display_status': 'SPECIFIED_NOT_AVAILABLE', 'activation_policy': 'DENY_UNTIL_QUALIFIED',
            'manifest_contract_state': 'NOT_IMPLEMENTED', 'activation_eligible': False,
            'can_activate': False, 'can_install': False, 'can_execute': False,
            'runtime_status': 'NOT_INSTALLED', 'audience': 'admin-preview',
            'visibility_policy': 'configurable-read-only',
        }.items():
            if entry.get(key) != value or type(entry.get(key)) is not type(value):
                reject('runtime_or_evidence_overclaim:'+key)
        if set(entry.get('future_manifest_required_fields', [])) != MANIFEST_FIELDS:
            reject('weak_module_contract')
        deps = entry.get('depends_on')
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps) or len(set(deps)) != len(deps):
            reject('invalid_dependencies')
        if not isinstance(entry.get('related_decisions'), list) or not entry['related_decisions'] or any(
            not isinstance(d, str) or not re.fullmatch(r'Q(?:[1-9]|[1-9][0-9]|1[0-9]{2}|2[0-1][0-9]|220)', d)
            for d in entry['related_decisions']):
            reject('invalid_or_unknown_decision')
        is_core = entry['kind'] == 'core-capability'
        if is_core and (entry.get('optional') is not False or entry.get('mvp_required') is not True
                        or entry.get('target_release') != 'v1.0.0' or entry.get('priority') != 'MUST'):
            reject('core_mvp_downgraded')
        if not is_core and (entry.get('optional') is not True or entry.get('mvp_required') is not False
                            or entry.get('blocking_when_unavailable') is not False or entry.get('priority') != 'LATER'
                            or entry.get('missing_runtime_safe_to_ignore') is not True):
            reject('optional_module_blocks_core')
        if entry['kind'] == 'publisher-extension' and entry.get('owner_scope') != 'publisher-private':
            reject('publisher_must_remain_private')
        if entry['kind'] != 'publisher-extension' and entry.get('owner_scope') != 'core-public':
            reject('public_module_misclassified')
    if sum(x['kind']=='core-capability' for x in modules) != 15 or sum(x['kind']!='core-capability' for x in modules)!=25:
        reject('original_40_entry_composition_changed')
    graph_visiting: set[str] = set()
    graph_done: set[str] = set()
    def walk(key: str) -> None:
        if key in graph_visiting:
            reject('dependency_cycle')
        if key in graph_done:
            return
        graph_visiting.add(key)
        item = found[key]
        for dependent in item['depends_on']:
            if dependent not in found:
                reject('unresolved_dependency')
            target=found[dependent]
            if item['kind'] == 'core-capability' and target['kind'] != 'core-capability':
                reject('core_depends_on_optional')
            if release_sort_key(target['target_release']) > release_sort_key(item['target_release']):
                reject('early_module_depends_on_later_release')
            walk(dependent)
        graph_visiting.remove(key)
        graph_done.add(key)
    for item_id in found:
        walk(item_id)
    for expected in ['core.bootstrap','core.identity','core.rbac','core.agent','core.php_site','core.https',
                     'core.files_sftp','core.backup','core.module_catalog','apps.one_click',
                     'container.docker_apps','container.podman_apps','publisher.hub','extensions.abi']:
        if expected not in found:
            reject('mandatory_catalog_item_missing')
    if any(item['license_entitlement_policy'] != 'CORE_FREE_UNGATED' for item in modules if item['kind'] == 'core-capability'):
        reject('core_must_remain_free')
    if found['apps.one_click']['license_entitlement_policy'] != 'CORE_FREE_ALWAYS':
        reject('native_one_click_is_free')
    if any(item['license_entitlement_policy'] != 'OPTIONAL_COMMERCIAL_POLICY_NOT_SELECTED' for item in modules if item['kind'] == 'optional-module' and item['id'] != 'apps.one_click'):
        reject('unauthorized_optional_premium_policy')
    if found['core.module_catalog']['blocking_when_unavailable'] is not False or found['core.module_catalog']['missing_runtime_safe_to_ignore'] is not True:
        reject('module_catalog_outage_must_not_block_core_boot')
    if any(x in found['apps.one_click']['depends_on'] for x in ('publisher.hub','container.docker_apps','container.podman_apps')):
        reject('one_click_requires_optional_container_or_hub')
    if found['publisher.hub']['kind'] != 'publisher-extension' or 'extensions.abi' not in found['publisher.hub']['depends_on']:
        reject('hub_must_follow_neutral_abi')
    for engine,other in [('container.docker_apps','container.podman_apps'),('container.podman_apps','container.docker_apps')]:
        if any(x in found[engine]['depends_on'] for x in (other,'apps.one_click')):
            reject('container_driver_not_independent')
    return {'catalog_entries':40,'required_core':15,'optional':25,'runtime_qualified':False}


def validate_releases(data: Any) -> dict:
    if not isinstance(data, dict) or data.get('schema_version') != 'forgepanel.release-trains/proposal-v2' or data.get('policy_status') != 'PROPOSED_NOT_APPROVED':
        reject('release_policy_not_a_proposal')
    if data.get('no_release_published') is not True or data.get('major_semver_only_when_breaking_changes') is not True:
        reject('false_release_or_major_claim')
    if data.get('git_flow') != ['features/*','develop','stable','main','production'] or data.get('q120_order') != ['R1','R2','R3','R4','R5','R6']:
        reject('release_order_drift')
    if data.get('hub_never_required_for_core') is not True or data.get('security_gates_non_waivable') is not True:
        reject('security_or_hub_boundary_drift')
    rows=data.get('stages')
    if not isinstance(rows,list) or len(rows)!=9 or [x.get('stage') for x in rows]!=STAGES:
        reject('stage_sequence_changed')
    tags=[x.get('example_tag') for x in rows]
    if len(set(tags))!=9 or any(release_sort_key(tags[i]) >= release_sort_key(tags[i+1]) for i in range(8)):
        reject('semver_stage_order_broken')
    for i,x in enumerate(rows,1):
        if x.get('id')!=f'FP-REL-{i:02d}' or x.get('actual_gate_state')!='NOT_RUN' or x.get('published') is not False or x.get('deployed') is not False:
            reject('stage_proof_or_id_overclaim')
    if rows[1]['dependency_gate']!='R2' or rows[2]['dependency_gate']!='R3' or rows[3]['dependency_gate']!='R4':
        reject('r2_r3_r4_sequence_mismatch')
    if 'non-executable' not in rows[1]['minimum_criteria'] or 'VM' not in rows[2]['minimum_criteria']:
        reject('prealpha_installer_false_claim')
    if rows[-1]['distribution_channel']!='Stable' or rows[0]['distribution_channel']!='Dev':
        reject('distribution_channel_mismatch')
    return {'stage_count':9,'published':False}


def validate_qa(data: Any) -> dict:
    if not isinstance(data,dict) or data.get('schema_version')!='forgepanel.module-qa/proposal-v1' or data.get('status')!='PLANNED_NOT_EXECUTED':
        reject('invalid_qa_registry')
    rows=data.get('tests')
    if not isinstance(rows,list) or len(rows)!=35:
        reject('invalid_qa_count')
    ids=set()
    for x in rows:
        if not isinstance(x,dict) or not QA_ID.fullmatch(x.get('id','')) or x['id'] in ids:
            reject('duplicate_or_invalid_qa_id')
        ids.add(x['id'])
        if x.get('execution_status')!='NOT_RUN' or x.get('evidence') is not None:
            reject('unexecuted_qa_mislabeled')
        if not all(isinstance(x.get(k),str) and x[k].strip() for k in ('description','gate','type')):
            reject('qa_missing_description')
    return {'planned_qa':len(rows),'executed':0}


def validate_bilingual_docs(root: Path) -> dict:
    for rel,expected in DOCS.items():
        docs=[]
        for locale in ('fr','en'):
            path=root/'DOCUMENTATION'/locale/rel
            s=path.read_text(encoding='utf-8')
            m=META.search(s)
            if m is None or m.group(1)!=expected or m.group(3)!='proposed':
                reject('invalid_doc_metadata:'+rel)
            docs.append((m.group(1),m.group(2),m.group(3)))
            other='fr' if locale=='en' else 'en'
            other_link=f'../../{other}/{rel}'
            if other_link not in s:
                reject('missing_language_backlink:'+rel)
            if len(s.strip()) < 1800:
                reject('unreasonable_empty_doc:'+rel)
        if docs[0]!=docs[1]:
            reject('fr_en_metadata_drift:'+rel)
    return {'bilingual_document_pairs':len(DOCS)}


def check(root: Path = ROOT) -> dict:
    root=Path(root)
    def load(name: str) -> Any:
        return json.loads((root/name).read_text(encoding='utf-8'))
    result={}
    result.update(validate_modules(load(MODULE_PATH)))
    result.update(validate_releases(load(RELEASE_PATH)))
    result.update(validate_qa(load(QA_PATH)))
    result.update(validate_bilingual_docs(root))
    result.update({'status':'PASS_DOCUMENTARY_CONSISTENCY_ONLY', 'core_deployed':False,
                   'os_vm_certified':False,'runtime_feature_execution_authorized':False,
                   'project_decision_ratified':False,'github_merged':False})
    return result


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args()
    try:
        print(json.dumps(check(args.root),sort_keys=True,ensure_ascii=False))
    except (ValueError,OSError,TypeError,OverflowError,KeyError,json.JSONDecodeError) as e:
        print(json.dumps({'status':'BLOCKED','reason':str(e)},sort_keys=True,ensure_ascii=False))
        return 2
    return 0

if __name__=='__main__':
    raise SystemExit(main())