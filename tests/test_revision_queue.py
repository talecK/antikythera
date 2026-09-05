"""Queue safety and registered workload checks; no real-data evaluation."""
import csv
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "eval"))
import run_revision_queue as queue


def test_registered_workload():
    jobs = queue.plan(8)
    assert len(jobs) == 3
    for _, command, _ in jobs[:2]:
        assert command[command.index("--R") + 1] == "1000"
        assert command[command.index("--drift") + 1] == "10"
        assert "--headline" in command
    thread = jobs[2][1]
    assert thread[thread.index("--seeds") + 1] == "10"
    assert thread[thread.index("--space") + 1] == "thread"
    assert thread[thread.index("--workers") + 1] == "2"


def test_partial_table_is_not_complete():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        path = root / "result.tsv"
        with path.open("w") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(["R"])
            writer.writerows([[1000]] * 7)
        with patch.object(queue, "ROOT", root):
            try:
                queue.validate_output("paper2_label_R1000", ["result.tsv"])
            except RuntimeError:
                pass
            else:
                raise AssertionError("partial table accepted")
            with path.open("a") as f:
                f.write("1000\n")
            assert queue.validate_output("paper2_label_R1000", ["result.tsv"]) == {
                "result.tsv": queue.sha256(path)}


if __name__ == "__main__":
    test_registered_workload()
    test_partial_table_is_not_complete()
    print("2 passed")
