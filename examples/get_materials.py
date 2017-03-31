import json
import argparse

from endpoints.login import ExabyteLoginEndpoint
from endpoints.materials import ExabyteMaterialsEndpoint

HOST = 'platform.exabyte.io'
PORT = 443


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='username')
    parser.add_argument('-p', '--password', required=True, help='password')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    login_endpoint = ExabyteLoginEndpoint(HOST, PORT, args.username, args.password)
    auth_params = login_endpoint.login()
    materials_endpoint = ExabyteMaterialsEndpoint(HOST, PORT, **auth_params)
    materials = materials_endpoint.get_materials()
    print json.dumps(materials, indent=4)
