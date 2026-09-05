# Final bounded extension: verified results

Verified on M1 on 2026-09-05. All 44 registered extension jobs completed
on the native ARM MBP with passing pilot and aggregate production checks.
There were no resource-limited attempts. The UTC guard recorded queue exit
at 08:36:55 UTC (01:36:55 Pacific), before the original 12:21:31 UTC cutoff.
The queue reported 7457.17 seconds of internal elapsed time, which excludes
macOS sleep; UTC start to observed exit was approximately 2 hours 15 minutes.
Summed attempt durations were 4.140 worker-hours. No further sampling is planned.

The final M1 audit verified 496 files (164,102,602 bytes), frozen input,
code, matrix, census and transfer hashes, and recomputed all archived stage
diagnostics and production estimates. All 44 extension results passed the
audit. Together with the 32 passing original results, all 76 Paper 2
window/null combinations are usable. Original results and registrations
are preserved; pilots, unresolved original chains and nulls were not pooled.
The extension does not evaluate pair formation.

## Unchanged scientific predictions

| Prediction | N2 | N3 |
|---|---|---|
| X-a: detected original cells retain sign | FAIL: WSB k=4 reverses | FAIL: WSB k=3 and k=4 reverse |
| X-b: onset k=5 and all original P1/P2/P3 | FAIL: k=4, P1 fails | FAIL: k=0, P1 and P2 fail |
| X-c: both excursion cells have z>=5 and ratio>1 | FAIL | FAIL |

The N2 onset rule returns evaluation 2021Q1-Q2, one window before the
registered 2021Q2-Q3. The full prediction still fails because the original
preceding nondetection pattern does not hold. N3 returns the first measured
window, 2020Q1-Q2, and every subsequent WSB window has z<=-3. This places
separation before GameStop under N3; it does not date its emergence before
the observed series or identify a causal effect of the squeeze.

| WSB evaluation window | N2 ratio | N2 z | N3 ratio | N3 z |
|---|---:|---:|---:|---:|
| 2020Q1-Q2 | 0.6403 | -6.764 | 0.6834 | -5.879 |
| 2020Q2-Q3 | 0.8433 | -4.655 | 0.8466 | -4.742 |
| 2020Q3-Q4 | 0.8220 | -2.977 | 0.7559 | -4.133 |
| 2020Q4-2021Q1 | 1.0825 | 3.007 | 0.8957 | -4.450 |
| 2021Q1-Q2 | 0.8497 | -10.501 | 0.8422 | -10.993 |
| 2021Q2-Q3 | 0.4171 | -19.514 | 0.4333 | -18.833 |
| 2024Q3-Q4 | 0.5531 | -12.057 | 0.5379 | -12.568 |

Diagnostic passes are not scientific prediction passes. The first excursion
has attenuated positive support under N2 and a reversed sign under N3;
the second reverses under both. The original strong positive excursion
and the claim of a newly segregated community after GameStop cannot be
presented as robust across these nulls. These failures must remain explicit.

Paper 1's separately verified aggregate separation result remains intact
(X-d passes both nulls); its pair formation precision remains unresolved
(X-e under both nulls). The extension changes neither conclusion.

The recommended editorial path is to consolidate Paper 2's consistent
source validation, longitudinal evidence and failed robustness predictions
into Paper 1 and its supplement, unless a separate distinct contribution
can be justified without recasting a failed prediction as a success.
This is a recommendation, not a completed manuscript merge. Both drafts
still require substantive revision; no preprint update or outreach occurred.

Evidence: `curveball_extension1_verification_final.json`,
`curveball_extension1_transfer_manifest_final.json`,
`curveball_extension1_completed_queue.json`,
`curveball_extension1_completed_wall_guard.json`,
`curveball_extension1_scores.json`, and the unchanged registrations.
