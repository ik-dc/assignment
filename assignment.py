from collections import defaultdict


DEFAULT_CENTER = "COM"
ORBIT_DELIMITER = ")"


def get_star_map_from_file(file_path: str) -> list[list[str]] | None:

    all_paths = []

    with open(file_path, "r") as file:
        for line in file.readlines():

            # Not clear how to deal with inconsistent information.
            # If a string found without any delimiter, we're not going to process any further and exiting early
            if ORBIT_DELIMITER not in line:
                return None

            else:
                all_paths.append(line.strip("\n").split(ORBIT_DELIMITER))
    return all_paths


def convert_star_map_to_graph_like_form(star_map: list[list[str]]) -> dict[str, set[str]]:
    known_star_paths = defaultdict(set)

    for orbiting_system in star_map:
        center_of_mass, orbiting_bodies = orbiting_system[0], orbiting_system[1:]

        for orbiting_body in orbiting_bodies:
            known_star_paths[center_of_mass].add(orbiting_body)

    return known_star_paths


def count_orbits(star_map: dict[str, set[str]], starting_point: str) -> int:
    def _count(_paths: dict[str, set[str]], _start_from: str, depth: int) -> int:
        count = 0
        if _paths.get(_start_from):
            depth += 1
            count = depth * len(_paths[_start_from])

            for sub_path in _paths[_start_from]:
                count += _count(_paths, sub_path, depth)
        return count

    return _count(star_map, starting_point, 0)


def main(center: str = DEFAULT_CENTER):
    if raw_map := get_star_map_from_file(file_path="data.txt"):
        graph_star_map = convert_star_map_to_graph_like_form(star_map=raw_map)

        # Question: What is the total number of direct and indirect orbits in your map data?
        # Answer: 270768
        print("TOTAL ORBIT COUNT:", count_orbits(star_map=graph_star_map, starting_point=center))

    else:
        raise ValueError("could not extract data from file")


if __name__ == "__main__":  # pragma: no cover
    main()
