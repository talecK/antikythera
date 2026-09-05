"""Score registered nulls predictions from completed artifacts, never rerun data."""
import csv
import hashlib
import json
from pathlib import Path

from run_paper2 import HEADLINE, onset_window

ROOT = Path(__file__).resolve().parents[1]


def table(name):
    with (ROOT / "reports" / name).open() as f:
        return list(csv.DictReader(f, delimiter="\t"))


def key(row):
    return int(row["B"]), int(row["window"]), row["stratum"], row["lens"]


def verdict(passed, **evidence):
    return {"status": "PASS" if passed else "FAIL", **evidence}


def consecutive(indices):
    return any(b == a+1 for a,b in zip(indices, indices[1:]))


def score_onset(rows):
    ix = {key(row): row for row in rows}
    zs = [float(ix[4,k,"WSB","union"]["z_seg"]) for k in range(19)]
    dd = [float(ix[4,k,"DD","union"]["z_seg"]) for k in range(19)]
    onset = onset_window(zs)
    p1 = onset is not None and consecutive([k for k in range(onset) if abs(zs[k]) < 3]) \
        and consecutive([k for k in range(onset,19) if zs[k] <= -5])
    p2 = onset is not None and ix[4,onset,"WSB","union"]["eval_start"].startswith("2021")
    cliffs = [k+1 for k in range(18) if dd[k] > -3 and dd[k+1] <= -5
              and "2020Q1" <= ix[4,k+1,"DD","union"]["eval_start"] <= "2022Q4"]
    return {"window": onset, "eval_start": ix[4,onset,"WSB","union"]["eval_start"] if onset is not None else None,
            "P1": bool(p1), "P2": bool(p2), "P3": not cliffs,
            "DD_cliff_windows": cliffs,
            "later_exceptions": [k for k in range(onset+1,19) if zs[k]>-3] if onset is not None else None}


def score_m3(base, directory):
    """Verify manifest/raw pooled estimates before scoring imported results."""
    from verify_m3_results import verify, read_table
    verification = verify(directory)
    label = read_table(directory / "reports/paper2_windows_z_label_R1000_headline.tsv")
    changes = [{"cell":list(key(r)), "relative_z_change":
        abs(float(r['z_seg'])-float(base[key(r)]['z_seg']))/abs(float(base[key(r)]['z_seg']))}
        for r in label]
    tails = []
    for r in label:
        k=key(r); p=float(r['mc_p_2s'])
        if abs(float(base[k]['z_seg']))>=5:
            tails.append(dict(cell=list(k),p=p,passed=abs(p-2/1001)<1e-12))
        elif k in [(4,1,'WSB','union'),(4,2,'WSB','union')]:
            tails.append(dict(cell=list(k),p=p,passed=p>.05))
    manifest = json.loads((directory / 'reports/paper1_nulls_label_R100_thread_seeds10.json').read_text())
    batches=[dict(fold=c['fold'],eligible=c['eligible'],**b) for c in manifest['cells'] for b in c['batches']]
    spread=[dict(fold=c['fold'],relative_range=(max(b['ratio'] for b in c['batches'])-
         min(b['ratio'] for b in c['batches']))/c['ratio']) for c in manifest['cells']]
    return {
        'R-a':verdict(all(c['relative_z_change']<=.2 for c in changes),changes=changes),
        'R-b':verdict(all(c['passed'] for c in tails),cells=tails),
        'T-a':verdict(all(b['z_seg'] < -100 for b in batches),
                      failures=[b for b in batches if b['z_seg']>=-100]),
        'T-b':verdict(all(b['formed']<=.01*b['eligible'] for b in batches),
                      failures=[b for b in batches if b['formed']>.01*b['eligible']]),
        'T-c':verdict(all(s['relative_range']<=.05 for s in spread),folds=spread),
        'M3_verification':verification,
    }, {int(r['window']):float(r['collapsed_frac']) for r in label if r['stratum']=='WSB'}


def main():
    base = {key(r): r for r in table("paper2_windows_z.tsv")}
    rows = table("paper2_windows_z_stratified_R100.tsv")
    required = {(4,k,s,"union") for s in ("WSB","DD") for k in range(19)}
    assert len(rows) == 38 and {key(r) for r in rows} == required, "N1 table incomplete"
    ix = {key(r): r for r in rows}
    fail_sign = [list(key(r)) for r in rows if abs(float(base[key(r)]["z_seg"])) >= 3
                 and float(base[key(r)]["z_seg"])*float(r["z_seg"]) <= 0]
    chance = [list(key(r)) for r in rows if abs(float(base[key(r)]["z_seg"])) < 3
              and abs(float(r["z_seg"])) >= 3]
    onset = score_onset(rows)
    excursion = [{"window": k, "z": float(ix[4,k,"WSB","union"]["z_seg"]),
                   "ratio": float(ix[4,k,"WSB","union"]["ratio"])} for k in (3,4)]
    excess = [{"cell": list(key(r)), "formed": int(r["formed"]), "eligible": int(r["n_eligible"])}
              for r in rows if key(r) not in [(4,k,"WSB","union") for k in (3,4)]
              and int(r["formed"]) > .01*int(r["n_eligible"])]
    result = {
        "N1-a": verdict(not fail_sign and not chance, sign_failures=fail_sign,
                          non_detection_failures=chance),
        "N1-b": verdict(onset["window"] == 5 and all(onset[p] for p in ("P1","P2","P3")), **onset),
        "N1-c": verdict(all(r["z"]>=5 for r in excursion), excursion=excursion),
        "N1-d": verdict(not excess, exceptions=excess,
                          interpretation="Literal nominal-count prediction; not a test that these pairs are true discoveries"),
        "D-a": {"status": "WITHDRAWN_BEFORE_REGISTRATION"},
    }
    p1 = {kind: table(f"paper1_nulls_{kind}_R100.tsv") for kind in ("label","stratified")}
    assert all(len(rs)==4 for rs in p1.values()), "Paper 1 table incomplete"
    failures = [r["space"]+"/"+r["fold"] for r in p1["stratified"]
                if float(r["z_seg"]) > -3 or int(r["formed"]) > .01*int(r["eligible"])]
    result["P1-a"] = verdict(not failures, failures=failures)
    references = {s: json.loads((ROOT / p).read_text()) for s,p in (
        ("author","data/registry/run5_author/run8_author.json"),
        ("thread","data/registry/pilot1_concepts/run8_thread.json"))}
    changes = [{"space":r["space"], "fold":r["fold"],
                "relative_z_change": abs(float(r["z_seg"])-references[r["space"]][r["fold"]]["z_total"])
                                      /abs(references[r["space"]][r["fold"]]["z_total"])} for r in p1["label"]]
    result["P1-b"] = verdict(all(r["relative_z_change"] <= .2 for r in changes), changes=changes)
    hn = {}
    for kind, records in p1.items():
        bycell = {(r["space"],r["fold"]):float(r["collapsed_frac"]) for r in records}
        hn[kind] = {fold:{s:bycell[s,fold] for s in ("author","thread")} for fold in ("fold1","fold2")}
    n1_drift = {k: float(ix[4,k,"WSB","union"]["collapsed_frac"]) for k in (1,2,3,4)}
    result["D-b"] = {"status":"FAIL", "reason":"HN thread collapse is below author collapse in both folds",
                      "HN": hn, "WSB_N1": n1_drift,
                      "WSB_original_null": {"status":"PENDING_M3"}}
    for name in ("R-a","R-b","T-a","T-b","T-c"):
        result[name] = {"status":"PENDING_M3"}
    if (ROOT/'reports/revision_queue_m3.json').exists():
        m3, wsb = score_m3(base, ROOT)
        result.update(m3)
        result['D-b']['WSB_original_null'] = wsb
    result["decision_rules"] = {
        "excursion_withdrawal_triggered": not all(r["z"]>3 for r in excursion),
        "onset_revision_triggered": onset["window"] != 5,
        "exact_margin_null_required": True,
        "public_manuscript_release_ready": False,
    }
    result["source_sha256"] = {name: hashlib.sha256((ROOT / "reports" / name).read_bytes()).hexdigest()
        for name in ("paper2_windows_z.tsv","paper2_windows_z_stratified_R100.tsv",
                     "paper1_nulls_label_R100.tsv","paper1_nulls_stratified_R100.tsv")}
    path = ROOT / "reports/nulls_amendment_scores.json"
    path.write_text(json.dumps(result, indent=2)+'\n')
    for name, rec in result.items():
        if "status" in rec: print(name, rec["status"])


if __name__ == "__main__":
    main()
