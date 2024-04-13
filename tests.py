from unittest import TestCase
from unittest.mock import patch

from assignment import convert_star_map_to_graph_like_form
from assignment import count_orbits
from assignment import get_star_map_from_file
from assignment import main


class TestGetStarMapFromFile(TestCase):
    def test_get_star_map_from_file__returns_empty_list_if_the_file_is_empty(self):
        with patch("builtins.open") as file_mock:
            file_mock.return_value.__enter__.return_value.readlines.return_value = []

            self.assertEqual([], get_star_map_from_file(file_path="test.txt"))

    def test_get_star_map_from_file__raises_value_error_if_single_line_cannot_be_parsed(self):
        with patch("builtins.open") as file_mock:
            file_mock.return_value.__enter__.return_value.readlines.return_value = [
                "test)test\n",
                "test\n",
                "test2)test3\n",
            ]

            self.assertIsNone(get_star_map_from_file(file_path="test.txt"))

    def test_get_star_map_from_file__returns_expected_results(self):
        with patch("builtins.open") as file_mock:

            test_file_lines = [
                "test)test1\n",
                "test1)test2\n",
                "test2)test3\n",
            ]
            file_mock.return_value.__enter__.return_value.readlines.return_value = test_file_lines

            self.assertCountEqual(
                [entry.strip("\n").split(")") for entry in test_file_lines],
                get_star_map_from_file(file_path="test.txt"),
            )


class TestConvertStarMapToGraphLikeForm(TestCase):
    def test_convert_star_map_to_graph_like_form__delivers_expected_results_with_one_orbiting_body_to_one_ratio(self):
        test_raw_star_map = [["test", "test1"], ["test1", "test2"], ["test2", "test3"]]

        self.assertDictEqual(
            {"test": {"test1"}, "test1": {"test2"}, "test2": {"test3"}},
            convert_star_map_to_graph_like_form(test_raw_star_map),
        )

    def test_convert_star_map_to_graph_like_form__delivers_expected_results_with_two_orbiting_bodies_to_one_ratio(self):
        test_raw_star_map = [
            ["test", "test1"],
            ["test", "test2"],
            ["test1", "test3"],
            ["test1", "test4"],
        ]

        self.assertDictEqual(
            {"test": {"test1", "test2"}, "test1": {"test3", "test4"}},
            convert_star_map_to_graph_like_form(test_raw_star_map),
        )

    def test_convert_star_map_to_graph_like_form__delivers_expected_results_with_three_orbiting_bodies_to_one_ratio(
        self,
    ):
        test_raw_star_map = [
            ["test", "test1"],
            ["test", "test2"],
            ["test", "test3"],
            ["test1", "test4"],
            ["test1", "test5"],
            ["test1", "test6"],
        ]

        self.assertDictEqual(
            {"test": {"test1", "test2", "test3"}, "test1": {"test4", "test5", "test6"}},
            convert_star_map_to_graph_like_form(test_raw_star_map),
        )


class TestCountOrbits(TestCase):
    def test_count_orbits__returns_expected_results(self):
        test_graphs_and_expected_results = [
            (6, "test", {"test": {"test1", "test2"}, "test1": {"test3", "test4"}}),
            (9, "test", {"test": {"test1", "test2", "test3"}, "test1": {"test4", "test5", "test6"}}),
            (
                42,
                "COM",
                {
                    "COM": {"B"},
                    "B": {"C", "G"},
                    "C": {"D"},
                    "D": {"E", "I"},
                    "E": {"F", "J"},
                    "G": {"H"},
                    "J": {"K"},
                    "K": {"L"},
                },
            ),
            (0, "NON-EXISTENT-CENTER", {"test": {"test1", "test2", "test3"}, "test1": {"test4", "test5", "test6"}}),
            (0, "test", {"test": {}, "test1": {}}),
        ]
        for expected_result, starting_point, test_graph in test_graphs_and_expected_results:
            with self.subTest(graph=test_graph):
                self.assertEqual(expected_result, count_orbits(test_graph, starting_point=starting_point))


class TestMain(TestCase):
    def test_main__raises_value_error_if_no_data_was_extracted_from_file(self):
        with patch("assignment.get_star_map_from_file") as data_getter_mock:
            data_getter_mock.return_value = None

            with self.assertRaises(ValueError):
                main()

    def test_main__works_as_expected(self):
        with patch("assignment.get_star_map_from_file") as data_getter_mock, patch("builtins.print") as print_mock:
            data_getter_mock.return_value = ["test", "test1"], ["test1", "test2"], ["test2", "test3"]
            main(center="test")

            print_mock.assert_called_with("TOTAL ORBIT COUNT:", 6)
