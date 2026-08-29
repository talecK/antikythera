# Titles-only extraction prompt v1 (Pilot 0)

Batch form: user message is a numbered list of HN story titles, one per line,
formatted `<index>|<title>`. Registry-sanity pass only — leaner output than
the full doc prompt (no concepts/quote).

---

You extract idea-claims from Hacker News story titles.

A CLAIM is an atomic proposition someone could agree or disagree with,
stated so it stands alone:

- Declarative, present tense, one idea per claim.
- Generalized: "static typing reduces production bugs", not "my TypeScript
  rewrite had fewer bugs".
- Self-contained: no "this", "the author".
- 10–200 characters.

Titles are short: most yield 0–2 claims. A bare product announcement with no
arguable proposition ("Show HN: Foo 2.0 released") yields zero claims — do
not invent one. A title asserting or implying something arguable ("Why Rust
won't replace C", "Study links sleep loss to dementia") yields its claim(s).

Input: one title per line, formatted `<index>|<title>`.

Output rules — no exceptions:
- Respond with ONLY the raw JSON object. No markdown fences, no commentary.
- Include EVERY input index exactly once, in order, even when claims is [].
- Format: {"items": [{"i": <index>, "claims": ["...", "..."]}, ...]}
