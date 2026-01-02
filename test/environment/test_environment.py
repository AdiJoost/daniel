import csv
"""Unit tests for Environment using unittest.TestCase and ARRANGE/ACT/ASSERT pattern."""

import csv
import tempfile
import unittest
from pathlib import Path

from src.environment.environment import Environment


def write_csv(path: Path, header: list, rows: list):
	with path.open("w", newline="", encoding="utf-8") as f:
		writer = csv.writer(f)
		writer.writerow(header)
		writer.writerows(rows)


class TestEnvironment(unittest.TestCase):
	def test_load_data_sets_current_date_to_min(self):
		# ARRANGE: create a sample CSV with unsorted dates
		with tempfile.TemporaryDirectory() as tmpdir:
			csv_path = Path(tmpdir) / "prices.csv"
			header = ["date", "AAPL", "MSFT", "GOOG"]
			rows = [
				["2020-01-03", "305", "162", "1355"],
				["2020-01-02", "300", "160", "1360"],
				["2020-01-06", "310", "165", "1365"],
			]
			write_csv(csv_path, header, rows)

			# ACT: load environment
			env = Environment(str(csv_path))

			# ASSERT: current_date set to the minimum date string
			self.assertEqual(env.current_date, "2020-01-02")

	def test_set_current_date_and_get_price(self):
		# ARRANGE: CSV with two dates and known prices
		with tempfile.TemporaryDirectory() as tmpdir:
			csv_path = Path(tmpdir) / "prices2.csv"
			header = ["date", "AAPL", "MSFT"]
			rows = [
				["2020-01-01", "100", "50"],
				["2020-01-02", "110", "55"],
			]
			write_csv(csv_path, header, rows)
			env = Environment(str(csv_path))

			# ACT: set current date to second date and query prices
			env.set_current_date("2020-01-02")
			aapl_price = env.get_current_price("AAPL")
			msft_price = env.get_current_price("MSFT")

			# ASSERT: returned prices match CSV values (as floats or ints)
			self.assertEqual(float(aapl_price), 110.0)
			self.assertEqual(float(msft_price), 55.0)

	def test_set_next_date_and_bounds(self):
		# ARRANGE: CSV with sequential dates
		with tempfile.TemporaryDirectory() as tmpdir:
			csv_path = Path(tmpdir) / "prices3.csv"
			header = ["date", "AAPL"]
			rows = [
				["2020-01-01", "10"],
				["2020-01-02", "20"],
			]
			write_csv(csv_path, header, rows)
			env = Environment(str(csv_path))

			# ACT / ASSERT: advance to next date
			self.assertEqual(env.current_date, "2020-01-01")
			env.set_next_date()
			self.assertEqual(env.current_date, "2020-01-02")

			# ACT / ASSERT: attempting to advance past last date raises IndexError
			with self.assertRaises(IndexError):
				env.set_next_date()

	def test_buy_and_sell_return_amount_times_price(self):
		# ARRANGE: single-date CSV
		with tempfile.TemporaryDirectory() as tmpdir:
			csv_path = Path(tmpdir) / "prices4.csv"
			header = ["date", "AAPL"]
			rows = [["2020-01-01", "5"]]
			write_csv(csv_path, header, rows)
			env = Environment(str(csv_path))

			# ACT: buy and sell operations
			cost = env.buy(3, "AAPL")
			revenue = env.sell(2, "AAPL")

			# ASSERT: cost and revenue are amount * price
			self.assertEqual(float(cost), 3 * 5.0)
			self.assertEqual(float(revenue), 2 * 5.0)


if __name__ == "__main__":
	unittest.main()

