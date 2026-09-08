"""Regression checks for conflicting BOM counts and stale power results."""
import contextlib
import csv
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import board1_documents as documents


class DocumentAuditTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.board = Path(directory.name) / 'board1'
        shutil.copytree(documents.BOARD, self.board)
        board_patch = patch.object(documents, 'BOARD', self.board)
        board_patch.start()
        self.addCleanup(board_patch.stop)

    def audit(self):
        with contextlib.redirect_stdout(io.StringIO()):
            documents.audit()

    def change_json(self, filename, change):
        path = self.board / filename
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_current_documents_pass(self):
        self.audit()

    def test_csv_override_conflicts_fail(self):
        path = self.board / 'bom_internal.csv'
        original = path.read_bytes()
        for item, count in [('B1-B059', '5'), ('B1-B027', '2'), ('B1-B011', '1')]:
            with self.subTest(item=item):
                path.write_bytes(original)
                rows = documents.read_rows()
                next(row for row in rows if row['item_id'] == item)['quantity'] = count
                with path.open('w', newline='') as stream:
                    writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                    writer.writeheader()
                    writer.writerows(rows)
                with self.assertRaisesRegex(AssertionError, 'CSV quantity disagrees'):
                    self.audit()
                with self.assertRaisesRegex(AssertionError, 'CSV quantity disagrees'):
                    documents.render_bom()

    def test_balanced_but_inconsistent_cut_schedule_fails(self):
        def change(data):
            data['header_cut']['cuts'][0]['pieces'] = 3
            data['header_cut']['spare_positions_unallocated'] = 16
        self.change_json('bom_quantity_rules.json', change)
        with self.assertRaisesRegex(AssertionError, 'placement quantity disagrees'):
            self.audit()

    def test_nominal_load_change_rejects_stale_results(self):
        def change(data):
            data['current_rev_a_input']['load_scenarios']['loaded_nominal']['gw_3v3'] = 55
        self.change_json('power_budget.json', change)
        with self.assertRaisesRegex(AssertionError, 'result load disagrees'):
            self.audit()

    def test_nominal_bridge_change_rejects_stale_results(self):
        def change(data):
            data['current_rev_a_input']['load_scenarios']['loaded_nominal']['bridge_5v'] = 90
        self.change_json('power_budget.json', change)
        with self.assertRaisesRegex(AssertionError, 'result bridge allowance disagrees'):
            self.audit()

    def test_conservative_bridge_change_rejects_stale_break_even(self):
        def change(data):
            data['current_rev_a_input']['load_scenarios']['loaded_conservative']['bridge_5v'] = 110
        self.change_json('power_budget.json', change)
        with self.assertRaisesRegex(AssertionError, 'conservative bridge allowance disagrees'):
            self.audit()

    def test_consistent_nominal_update_passes(self):
        def change(data):
            model = data['current_rev_a_input']
            model['load_scenarios']['loaded_nominal']['gw_3v3'] = 55
            result = model['results'][0]
            result['main_load_mA'] = 289.15
            result['usb_mA'] = documents.usb_current(5, 0.12, 80, 289.15, 0.9)
            result['buck_input_V'] = 5 - 0.12 * result['usb_mA'] / 1000
        self.change_json('power_budget.json', change)
        self.audit()


if __name__ == '__main__':
    unittest.main()
