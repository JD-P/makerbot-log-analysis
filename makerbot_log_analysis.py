import os
import os.path
import sys
import json
import csv
import argparse

def conv_stats_into_row(logpath):
    """Takes a path to a user_stats.json file and deserializes it into a tabular
    CSV format suitable for Excel."""
    logfile = open(logpath)
    logs = json.load(logfile)
    stats = logs["all_stats"]
    fieldnames = []
    row = []
    for stat in stats:
        if stat != "tool_usage":
            fieldnames.append(stat)
    fieldnames.sort()
    for field in fieldnames:
        row.append(stats[field])
    return (row, fieldnames)

def conv_dir_to_csv(path):
    """Convert a given directory paths log folders to a CSV where each row is
    a tabular form of that log folders "user_stats.json" file."""
    if not os.path.isdir(path):
        raise ValueError("Path given to conv_dir_to_csv was not a directory.")
    foldernames = os.listdir(path)
    row_count = 0
    rows = []
    for folder in foldernames:
        logpath = os.path.join(path, folder, "user_stats.json")
        row = conv_stats_into_row(logpath)
        if row_count == 0:
            rows.append(row[1])
            rows.append(row[0])
            row_count += 2
        else:
            rows.append(row[0])
            row_count += 1
    return rows

def write_csv_file(rows, outpath):
    """Write each row in [rows] to a CSV file at the filepath [outpath]."""
    try:
        outfile = open(outpath, mode="w", newline='')
    except TypeError:
        outfile = outpath
    outwriter = csv.writer(outfile)
    for row in rows:
        outwriter.writerow(row)
    outfile.close()
    return True

if __name__ == '__main__':
    description = """This tool converts Makerbot log files into CSV format.
If given the --csv option the tool converts the directories in [path] into a single
CSV file usable by excel.""" 
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="file or directory path to the extruder files")
    parser.add_argument("-o", "--output",
                        help="Filepath to the csv output file, prints to STDOUT otherwise.") 
    parser.add_argument("--csv", help="Convert the path to a CSV file usable by Excel.")
    arguments = parser.parse_args()

    if os.path.isdir(arguments.path):
        rows = conv_dir_to_csv(arguments.path)
        if arguments.output:
            write_csv_file(rows, arguments.output)
        else:
            write_csv_file(rows, sys.stdout)
    elif os.path.isfile(arguments.path):
        rows = []
        row = conv_stats_into_row(arguments.path)
        rows.append(row[1])
        rows.append(row[0])
        if arguments.output:
            write_csv_file(rows, arguments.output)
        else:
            write_csv_file(rows, sys.stdout)
    else:
        raise ValueError("Path given '" + arguments.path +
                         "' is not a valid directory or file.")
