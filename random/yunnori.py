""" random.yunnori parses records from yunnori games """
import csv
from enum import Enum, unique
import os
import sys
from typing import Dict, List


@unique
class Outcome(Enum):
    do = "1"
    ge = "2"
    geol = "3"
    yut = "4"
    mo = "5"
    back = "-1"
    home = "h"
    eat = "x"


def write_to_csv(stats_obj: Dict, filename: str) -> None:
    """
    Takes a player input object and writes to CSV
    :param stats_obj: Dict
    :param filename: str
    :return: None
    """
    header = ["Name", "Rounds Played", "Avg. Score per Round", "Avg. Eats per Round",
              "Avg. Rolls per Round"]
    flattened_list = [
        [
            key,
            stats_obj[key]["rounds_played"],
            stats_obj[key]["avg_score_per_round"],
            stats_obj[key]["avg_eats_per_round"],
            stats_obj[key]["avg_rolls_per_round"],
        ] for key in stats_obj]
    with open("{}.csv".format(filename), "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for row in flattened_list:
            writer.writerow(row)


def prep_raw_stats(user_dict: Dict) -> Dict:
    """
    Small helper method that prepares
    :param user_dict: Dict
    :return: Dict
    """
    return {
        "rounds_played": user_dict["rounds"],
        "avg_score_per_round": float(user_dict["total_score"]) / user_dict["rounds"],
        "avg_eats_per_round": float(user_dict["total_eats"]) / user_dict["rounds"],
        "avg_rolls_per_round": float(user_dict["total_rolls"]) / user_dict["rounds"],
    }


def parse_raw_file(filename: str) -> Dict:
    """
    Parses a raw csv file and outputs a dict
    :param filename: str
    :return: None
    """
    raw_rows = []
    with open(filename, newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            raw_rows.append(row)

    player_stats = {}
    for idx, row in enumerate(raw_rows):
        if row[0] != "Player:" and row[0] and "Round" not in row[0]:
            print("Found valid row!")
        else:
            continue

        print("Parsing row for user: {}".format(row[0]))
        entries = [entry for entry in row if entry]
        rounds = entries[1:]
        name = entries[0]

        user_dict = {
            "rounds": len(rounds),
            "total_score": 0,
            "total_eats": 0,
            "total_home": 0,
            "total_rolls": 0,
            "max_score": 0,
        }

        for round in rounds:
            user_dict["total_rolls"] += len(round.split(","))

            skip = False
            for idx, char in enumerate(round):
                if char is ",":
                    continue

                if skip:
                    skip = False
                    continue

                if char == "-" and idx+1 < len(round) and round[idx+1] == "1":
                    print("Found -1 value.")
                    user_dict["total_score"] -= 1
                    skip = True
                    continue

                try:
                    _ = Outcome(char)
                except Exception:
                    print("Special character not found: {}".format(char))
                    continue

                if char == "h":
                    user_dict["total_home"] += 1
                elif char == "x":
                    user_dict["total_eats"] += 1
                else:
                    user_dict["total_score"] += int(char)

        player_stats[name] = user_dict
    return player_stats


def process_files(files: List[str], output_name: str = "") -> None:
    """
    Processes a list of input files and sums results before writing to file.
    :param files:
    :param output_name:
    :return:
    """
    player_stats = {}
    for file in files:
        file_output = parse_raw_file(file)

        for key in file_output:
            if key in player_stats:
                # sum these up
                player_stats[key]["rounds"] += file_output[key]["rounds"]
                player_stats[key]["total_score"] += file_output[key]["total_score"]
                player_stats[key]["total_eats"] += file_output[key]["total_eats"]
                player_stats[key]["total_home"] += file_output[key]["total_home"]
                player_stats[key]["total_rolls"] += file_output[key]["total_rolls"]
            else:
                player_stats[key] = file_output[key]

    prepped_stats = {name: prep_raw_stats(player_stats[name]) for name in player_stats}

    if not output_name:
        output_name = "output_stats"

    write_to_csv(prepped_stats, output_name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Yutnori parse requires subcommand.")
        sys.exit(1)

    if sys.argv[1] == "parse":

        if len(sys.argv) < 3:
            print("Parse mode requires at least one input filename.")
            sys.exit(1)

        print("Beginning yootnori parse mode for file: {}.".format(sys.argv[2]))
        process_files(sys.argv[2:])
    else:
        print("No command found for: {}".format(sys.argv[1]))
        sys.exit(1)
