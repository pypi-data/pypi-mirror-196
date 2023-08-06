import time
import unittest
from unittest import TestCase
from unittest.mock import MagicMock

import pytest

import replifactory.device.base_device
from replifactory.culture.culture_universal import CultureUniversal

device = replifactory.device.base_device.BaseDevice()
device.make_dilution = MagicMock()


class TestCultureUniversal(TestCase):
    @pytest.mark.skip(reason="test depends on system timer")
    def test_time_to_decrease_stress(self):
        # Test case 1: Culture is not growing and has not been diluted for a long time
        c = CultureUniversal()

        c._t_doubling = 30
        c.no_growth_t_doubling_threshold = 25
        c._last_dilution_start_time = time.time() - 50 * 60 * 60
        c.no_growth_period_max = 45
        result = c.time_to_decrease_stress()
        self.assertTrue(result)

        # Test case 2: Culture is growing but has never been diluted
        c._last_dilution_start_time = None
        c._t_doubling = 20
        c.no_growth_t_doubling_threshold = 25
        c.no_growth_period_max = 45
        result = c.time_to_decrease_stress()
        self.assertFalse(result)

        # Test case 3: Culture is growing but has not been diluted for a long time
        c._t_doubling = 20
        c.no_growth_t_doubling_threshold = 25
        c._last_dilution_start_time = time.time() - 50 * 60 * 60
        c.no_growth_period_max = 45
        result = c.time_to_decrease_stress()
        self.assertFalse(result)

        # Test case 4: Is not growing but has been diluted recently
        c._t_doubling = 20
        c.no_growth_t_doubling_threshold = 25
        c._last_dilution_start_time = time.time() - 20 * 60 * 60
        c.no_growth_period_max = 45
        result = c.time_to_decrease_stress()
        self.assertFalse(result)

    def test_make_first_dilution(self):
        c = CultureUniversal()
        c.dilute_adjust_drug1 = MagicMock()

        c.dilute_adjust_drug1.assert_not_called()
        c.make_first_dilution()
        c.dilute_adjust_drug1.assert_called()

    def test_time_to_increase_stress(self):
        c = CultureUniversal()
        c._od = 0.5
        c.dilution_trigger_od = 0.3
        # Test case 1: Culture has been diluted enough times, growing fast enough, and stress has not been increased for a long time
        c._n_dilutions = 10
        c.stress_increase_initial_dilution_number = 9
        c._t_doubling = 20
        c.stress_increase_t_doubling_threshold = 25
        c._n_dilutions_last_stress_increase = 5
        c.stress_increase_delay_dilutions = 4
        result = c.time_to_increase_stress()
        self.assertTrue(result)

        # Test case 2: Culture has not been diluted enough times
        c._n_dilutions = 8
        c.stress_increase_initial_dilution_number = 9
        c._t_doubling = 20
        c.stress_increase_t_doubling_threshold = 25
        c._n_dilutions_last_stress_increase = 5
        c.stress_increase_delay_dilutions = 4
        result = c.time_to_increase_stress()
        self.assertFalse(result)

        # Test case 3: Culture is not growing fast enough
        c._n_dilutions = 10
        c.stress_increase_initial_dilution_number = 9
        c._t_doubling = 30
        c.stress_increase_t_doubling_threshold = 25
        c._n_dilutions_last_stress_increase = 5
        c.stress_increase_delay_dilutions = 4
        result = c.time_to_increase_stress()
        self.assertFalse(result)

        # Test case 4: Stress has been increased for a short time
        c._n_dilutions = 10
        c.stress_increase_initial_dilution_number = 9
        c._t_doubling = 20
        c.stress_increase_t_doubling_threshold = 25
        c._n_dilutions_last_stress_increase = 8
        c.stress_increase_delay_dilutions = 4
        result = c.time_to_increase_stress()
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
