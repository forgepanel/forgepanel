<!-- forgepanel-doc id=FP-16 revision=1 status=documented -->
# Performance and capacity

[Français](../../fr/16-performance/README.md) · [Index](../README.md)

No representative ForgePanel benchmark, hosting-capacity claim or production service-level objective is supported by the inspected material. Do not rank web stacks by an unmeasured universal speed score. Native test duration is not a benchmark.

## Measurement plan

Measure interactive panel latency (including p50/p95/p99 and errors), database query count/time, memory per worker, operation queue wait/execution, configuration reload impact and resource isolation under concurrent tenants. Fix workload, dataset, hardware, OS, runtime, commit and cache state. Separate cold/warm runs, repeat trials and retain raw sanitized results. Define acceptance thresholds after a baseline and product capacity target, not by invention in this document.

Test the panel independently from customer web traffic, then together under contention. Include long-running jobs, cancellation, failed operations and an unavailable dependency; successful requests alone hide overload behavior. Fixture OS selection does not measure kernel, filesystem or web-server performance.

## Optimization constraints

Keep heavy system operations outside the HTTP request. Use targeted indexes and bounded queries before adding distributed caches. Redis remains optional until measurements justify it. OPcache and pool settings require environment-specific validation; JIT is not assumed to help. Do not cache private admin pages across identities or serve stale authorization. Avoid frequent full Live Component refreshes for high-rate telemetry; UI transport choices need measured limits.

A proposal to change a runtime, worker model or web profile must include correctness/isolation tests alongside performance results. Throughput improvements cannot justify bypassing `.htaccess` access controls, tenant limits or secret protection. Regression budgets and a repeatable load suite belong to the future integration milestone.

[Architecture](../02-architecture/README.md) · [Operations](../15-operations/README.md)
