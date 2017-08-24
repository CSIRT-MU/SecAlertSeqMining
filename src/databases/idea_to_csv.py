import argparse
from alerts.idea import Idea


def none_to_empty_str(o):
    return str(o) if o else ""


def process_line(line: str):
    idea = Idea(line)
    return ",".join(map(none_to_empty_str,
                        [idea.id,
                         idea.detect_time,
                         idea.category,
                         idea.node_name,
                         idea.source_ip4,
                         idea.source_proto,
                         idea.target_ip4,
                         idea.target_proto,
                         ";".join(map(str, idea.target_ports)) if idea.target_ports else None,
                         ]))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert json IDEA alerts to csv. Pass name of input file as "
                                                 "argument. Input file should contain one IDEA alert per line. "
                                                 "Output csv entries are printed to stdout.")
    parser.add_argument('file', type=argparse.FileType('r', encoding='UTF-8'))
    args = parser.parse_args()

    for line in args.file:
        print(process_line(line))
