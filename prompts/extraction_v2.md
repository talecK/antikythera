# Extraction prompt v2 (granularity v1)

Changes from v1 (smoke-test findings, haiku-4-5_pv1_sv1):
1. Content-free docs drew prose refusals instead of {"claims": []} (5/105).
2. concepts occasionally had 4 items vs schema max 3 (10/105).
3. 100/105 responses wrapped in markdown fences.

---

You extract idea-claims from a Hacker News discussion (story title, optional
self-text, top comments).

A CLAIM is an atomic proposition someone could agree or disagree with,
stated so it stands alone outside this discussion:

- Declarative, present tense, one idea per claim.
- Generalized beyond the anecdote: "static typing reduces production bugs",
  not "my TypeScript rewrite had fewer bugs".
- Self-contained: no "this", "the author", "OP", "the article".
- 10–200 characters.

Extract 3–10 claims covering the distinct ideas actually asserted or
seriously argued in the document. Fewer is fine. Do NOT invent claims not
grounded in the text; do NOT extract questions, jokes, or pure opinions
about the discussion itself ("this thread is toxic").

For each claim give `concepts`: AT MOST 3 lowercase noun phrases naming what
the claim connects (e.g. ["rust", "memory safety"]) — never more than 3.
Optionally give `quote`: the shortest verbatim snippet grounding the claim.

Output rules — no exceptions:
- Respond with ONLY the raw JSON object. No markdown code fences, no
  commentary, no explanation before or after.
- If the document has no extractable claims, respond with exactly:
  {"claims": []}
- Never respond in prose.

Format:
{"claims": [{"claim": "...", "concepts": ["..."], "quote": "..."}]}
