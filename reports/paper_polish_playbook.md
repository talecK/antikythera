# Paper polish playbook

Distilled from the paper 2 session of 2026-09-01 (commits af651b7 through
the ladder pass). Written so a fresh session can apply the same passes to
paper 1 (reports/paper1_draft.md) without re-deriving anything. Work in
the order given; each step was learned by doing it out of order once.

## 0. Ground rules that bound every edit

- The markdown draft is the source of record. Every edit goes there,
  then the review page is regenerated and republished:
  `python3 eval/render_paper_html.py paper1 --out <scratch>/paper1_draft_artifact.html`
  then the Artifact tool with the paper 1 URL from
  HANDOFF.md ("Review artifacts") passed as `url`. The page footer shows
  the commit hash, so re-render after committing.
- Never touch numbers, verdicts, tables, quoted registered language, or
  disclosure terms. After every prose edit, run the numeric diff below
  and explain every token that changed. A lost token must be a section
  number, a repository path, a date bump, or a label; nothing else.
- Owner prose rules: no em-dashes, no AI-tell phrasing ("as such",
  "in concrete terms", "precisely", "notably", "crucially", "by the
  lights of", "worth recording", "as designed", "likewise stated",
  non-quantitative "exactly"), conventional paper register, accessible
  language, sentences split at about 45 words unless they are lists.
- Commit only when the owner says so, one commit per approved pass, with
  a message that says what changed and that no number changed.
- People-related content (referees, targets, allies) never enters a
  tracked file or a commit message. It lives in private/.
- Decisions are handed to the owner as "Pending: X, yes or no". The
  owner approves each pass; do not chain passes without approval.

Numeric diff (run from the repo root, HEAD = last commit of the draft):

```python
import re, subprocess, collections
new = open('reports/paper1_draft.md').read()
old = subprocess.run(['git','show','HEAD:reports/paper1_draft.md'],
                     capture_output=True, text=True).stdout
num = lambda t: collections.Counter(re.findall(r'-?\d[\d,]*\.?\d*', t))
print('lost', dict(num(old) - num(new))); print('new', dict(num(new) - num(old)))
```

## 1. Venue and limits, verified before editing

- Decide the venue ladder first and verify the limits on the venue's own
  pages that day (they bounce WebFetch through a cookie gate; use the
  browser pane). Paper 2's verified set, 2026-09-01: Nature
  Communications abstract 200 words unreferenced, main text 5,000
  excluding abstract, Methods, references and legends, Methods under
  3,000, about 70 references, up to 10 display items, legends 350 words,
  structure Introduction, Results, Discussion, Methods; first submission
  is format-flexible. PNAS Nexus abstract 250, 12-page ceiling counting
  everything, significance statement 50 to 120 words. EPJ Data Science
  abstract 150 to 250 with no unspecified references, no body limit,
  required Declarations block. Nature Human Behaviour abstract 150,
  main text 5,000, dropped as a reach for paper 2 because it wants a
  mechanism claim.
- Paper 1's venue per the outreach plan is EPJ Data Science, with
  Quantitative Science Studies as the alternative. Use the same
  Introduction, Results, Discussion, Methods structure as paper 2
  regardless: EPJ Data Science accepts it, it keeps the two papers
  consistent, and SocArXiv imposes nothing. Keep the provenance
  appendix in the preprint; a journal moves it to Supplementary.
- Word-count the draft by section before and after (Python split on
  `## ` headings, excluding table rows) and report main text versus
  Methods against the limits.

## 2. Title and abstract

- Title: a declarative sentence with a verb that states the finding,
  15 words or fewer. Keep the memorable phrase the outreach plan quotes
  if there is one, as the part before the colon.
- Abstract template (from the Nature Communications precedents): one or
  two sentences of the phenomenon for a general reader, a "but" sentence
  naming the gap, a "Here we" sentence carrying the design and the data
  scale, findings in order with their numbers, and a last sentence that
  lifts to the general implication in the present tense with no "we".
  No references in the abstract; cite the companion in the
  Introduction's first paragraph instead. Target 200 words or under for
  Nature Communications, 250 for PNAS Nexus, one paragraph everywhere.
- The closing line is calm, not a punchline. If the outreach plan quotes
  a hedge line, keep that line verbatim in the Conclusion paragraph,
  where the HN post can quote it; the abstract gets the general
  implication sentence instead.
- Cut order that worked: prediction labels and their clauses, per-window
  ranges and counts, control-group values, placebo standard deviations,
  duplicate "only" claims, filler openers, the companion citation. Each
  number dropped from the abstract must still appear in the body.

## 3. Structure and the venue patterns

Restructure in one pass, then apply the six patterns from the precedent
papers (Shi and Evans 2023, Ueshima et al. 2024, Simpson et al. 2023,
all Nature Communications; only the first was a high-attention paper):

1. Merge the numbered opening sections into one Introduction. Weave
   related work into referenced paragraphs; drop the roadmap paragraph;
   end with a test-case-then-general-claim sentence and a one-sentence
   statement of the finding.
2. Results opens with a short measurement summary that defines the
   unit, the statistic, the null, and the windows in plain words, with a
   pointer to Methods, because Methods now sits at the end.
3. A table of registered predictions with the pre-committed reading of
   each outcome and the observed result, placed at the top of Results.
4. Discussion has no subheadings. Bold run-in phrases are allowed.
   Limitations become prose. The conclusion is the last paragraph.
5. Methods at the end with subheadings; AI-assistance statement as its
   last subsection. Then Data availability, Code availability,
   Competing interests (paper 1 already has one), Author contributions,
   Figure legends that stand alone (define z and any band or threshold
   in the first data figure's legend), the commit appendix, References.
6. Convert every "Section N" cross-reference to a section name. Move
   repository paths out of the body into the appendix. Cite the
   companion paper by section title, never number.
7. Figure 1 is a schematic of the instrument, not a result. Data
   figures renumber after it; file names stay.

Verify with: no em-dashes, no "Section \d" left, no repo paths in the
body, per-section word counts, the numeric diff.

## 4. References

- Resolve every DOI against Crossref: `https://api.crossref.org/works/<doi>`
  returns title, authors, journal, volume, pages. Remove [verify] tags
  only after the record matches. Check for journal versions of working
  papers with `https://api.crossref.org/works?query.bibliographic=<title>`.
- Reference density in the precedents runs 40 to 60. Raise it through
  the Introduction rewrite with well-known background citations, each
  Crossref-checked before it goes in.

## 5. Jargon pass

Run the counter (grep for a list of candidate terms, count uses in the
body, note first section) and present three groups to the owner:
rename, define at first use, keep. Paper 2's decisions carry over:

- Internal names never reach the reader: "the gate" and any run
  number become "the companion analysis"; "owner" becomes "the author";
  "fleet run", "shard", "loader", "parquet", "seed document", "pull era",
  "provenance seam", "regex", "hub guard", "macro-hub", "SSE",
  "truth-null", "z-first", "densification", "author-space",
  "mixing-deficit instrument" become plain English.
- "eval" becomes "evaluation" in prose; tables keep the short form.
- "frozen" becomes "fixed in advance" or "committed before any result"
  when it means pre-committed, and "unchanged" or "standing" when it
  means reused from the companion analysis.
- "provenance" becomes "data source" (data-source confound, a single
  data source, artifact of the data source); the appendix becomes
  "Appendix: where every number comes from", referred to as the commit
  appendix.
- "bar" becomes "pass threshold"; "ladder" becomes "rule".
- Terms the registration file uses internally (gate, bar, B-ladder) get
  one gloss sentence in the Methods Registration paragraph so a reader
  who opens the registration recognizes them. Quoted registered text is
  never reworded; drop the quote and gloss instead.
- Define once at first use: the research program (companion paper plus
  this study), endpoints, the extraction lenses (checked against the
  extractor code: cashtag is the $-prefixed form, bare is the plain
  uppercase symbol under a stoplist, union is both).
- Keep: census, stratum, fold A/B, Part A/B, Amendment V1 to V4,
  conforming run, primary cell, LOW-POWER and UNINFORMATIVE as registered
  labels, verbatim, seeds and replicate counts, build and evaluation
  periods.
- Fresh prose compresses into slogans. Any sentence written new during
  a pass, rather than edited from the draft, gets read aloud once before
  it goes in; if it names a defined term without its context ("the
  fusion", "the cascade") or stacks two claims in one clause, unpack it.
- A word can be jargon in one sentence and load-bearing in the next.
  Paper 2's "cascade" is the theory term where the sentence says what
  happened, and "the squeeze" where the sentence says when; decide per
  use, not per word, and keep the quoted lines intact.
- Figure legends carry no internal notes (no "per the registered
  display rule", no "generated from committed TSVs"); the reader-facing
  reason for a design choice goes in the legend where it first applies.

## 6. Figures

All four paper 2 figures share eval/paper2_figstyle.py. Paper 1 should
import the same module (or a copy named for paper 1 with identical
values) so the two papers' figures read as one set.

- Palette, validated with the dataviz skill's checker on a light
  surface: blue #3b6ea5, orange #b8761c, green #3d8f5f as the only
  series colors, in that fixed order; red #b0413e reserved for
  highlights and always paired with a text label; grey #8a8a8a for
  nulls, bands, reference lines and uninformative markers, never a
  series. Orange and green sit in the colorblind warn band, so any
  panel with both also uses distinct markers (o, s, ^) and a legend.
  Run `node scripts/validate_palette.js "<hexes>" --mode light` from
  the dataviz skill directory before adding any color.
- Type and marks: 8 pt base, 8.5 pt titles left-aligned, 7 pt ticks and
  legends, 10 pt bold panel letters, 1.3 pt lines, 4 pt markers with a
  white edge, 0.6 pt axes with top and right spines off, chance band as
  a flat fill, thresholds dashed, onset dotted red.
- Layout rules: panel letter and title share one baseline; titles alone
  above the axes; legends inside the empty upper right of each z panel;
  a spacer row between panel groups; quarter labels only on the bottom
  axis; the onset labelled once, horizontally; values labelled above
  their points in ink, never in the series color.
- Outer padding: crop to drawn content, then pad 64 px horizontally and
  48 px vertically at 300 dpi (PAD_X, PAD_Y in the style module). For an
  axis-off canvas, union the drawn artists rather than the axes bbox.
  Measure the PNG margins with Pillow after every regeneration.
- Schematic figures are drawn on one figure-wide axes in inches, as
  cards of fixed size with one inner padding, one header band, and a
  vertical budget per card. Strips and bars span the full card width so
  they align with the paragraph beneath.
- Every figure is generated by a committed script from committed TSVs,
  and the owner reviews the PNG. Expect three to four rounds of owner
  markup; ask for circles on the image rather than descriptions.
- After each round, pin the figure rows in the commit appendix to the
  new commit.

## 7. Closing checks before handing back

- Numeric diff empty or fully explained.
- Word counts against the venue limits.
- Review page re-rendered at the committed hash and republished.
- HANDOFF.md paper line updated with the state and the open items.
- Memory updated (project status) in one paragraph.

## Paper 1 specifics to carry in

- Draft: reports/paper1_draft.md, last commit ddb7e29 before this
  playbook; results final and audited; competing-interests statement
  present; one consistency check open (abstract "2006 to 2026" versus
  Section 3.1 "active since 2007").
- Its review artifact URL is in HANDOFF.md. Both pages cross-link in
  their headers, so re-render paper 2 too if paper 1's title changes.
- Paper 2 cites paper 1's section "A second platform" by title; keep
  that heading text or update paper 2's Introduction in the same commit.
- Paper 1 is solo-authored by decision; the competing-interests wording
  is the template paper 2 reused.
