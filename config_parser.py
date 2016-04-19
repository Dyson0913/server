from optparse import OptionParser
import json


def config_parser():

    usage = "usage: %prog [options] arg"

    parser = OptionParser(usage)
    parser.add_option("-f", "--file", default="worker1.json")
    parser.add_option("-p", "--port",action="store",type="int",dest="port",default="7000")
    parser.add_option("-w", "--dbpw",action="store",type="string",dest="dbpw",default=None)
    parser.add_option("-i", "--id",action="store",type="int",dest="id",default=1)

    (options, args) = parser.parse_args()
    print options
    config_file = open(options.file)
    data = json.load(config_file)
    data['port'] = options.port
    data['dbpw'] = options.dbpw
    data['id'] = options.id
    return data
