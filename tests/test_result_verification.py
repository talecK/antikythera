"""Reject partial/tampered imported artifacts before scientific scoring."""
import json
from pathlib import Path
import sys,tempfile
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'eval'))
import verify_m3_results as m3
import score_curveball as cb


def test_incomplete_m3_manifest_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp);(root/'reports').mkdir()
        (root/'reports/revision_queue_m3.json').write_text(json.dumps({'jobs':{}}))
        try: m3.verify(root)
        except ValueError as e: assert 'queue jobs' in str(e)
        else: raise AssertionError('accepted empty M3 queue')


def test_curveball_raw_corruption_rejected():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp); matrix=root/'matrix'; matrix.write_bytes(b'matrix')
        raw=root/'raw';raw.write_bytes(b'original')
        report={'matrix':{'matrix_path':'matrix','matrix_sha256':m3.sha256(matrix)},
                'pilot':{'stages':[{'raw_path':'raw','raw_sha256':m3.sha256(raw)}]}}
        path=root/'record.json';path.write_text(json.dumps(report))
        with patch.object(cb,'ROOT',root):
            assert cb.checked(path)==report
            raw.write_bytes(b'changed')
            try: cb.checked(path)
            except ValueError as e: assert 'chain hash' in str(e)
            else: raise AssertionError('accepted changed chain')


if __name__=='__main__':
    test_incomplete_m3_manifest_rejected();test_curveball_raw_corruption_rejected();print('2 passed')
