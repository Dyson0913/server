from optparse import OptionParser
import json


def config_parser():

    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage)
    parser.add_option("-f", "--file", default="worker1.json")
    (options, args) = parser.parse_args()

    config_file = open(options.file)
    data = json.load(config_file)
    return data
