# Merge adjudication prompt v1 (control plane)

Used by the incremental clustering stage for borderline merges (cosine
similarity in the gray zone between auto-merge and auto-distinct thresholds;
thresholds live in the clustering config and are pre-registered per registry
build). Batched: several PAIR blocks per call.

---

You maintain a registry of distinct idea-claims. For each PAIR below decide
whether the two entries are the SAME idea (one would be an alias of the
other) or DISTINCT ideas.

SAME means: agreeing with one entails agreeing with the other; they differ
only in phrasing, specificity of wording, or emphasis.
DISTINCT means: they connect different concepts, take different stances, or
one is a strictly narrower sub-claim that could be true while the general
claim is false (or vice versa).

When genuinely undecidable from the text, answer UNSURE (treated as
DISTINCT downstream; the pair is re-visited at the next registry rebuild).

Input format per pair:
PAIR <id>
A: <canonical phrasing> | aliases: <up to 3> | e.g. seen in: <context snippet>
B: <canonical phrasing> | aliases: <up to 3> | e.g. seen in: <context snippet>

Respond with ONLY valid JSON:
{"verdicts": [{"pair": "<id>", "verdict": "SAME|DISTINCT|UNSURE", "reason": "<one short sentence>"}]}
