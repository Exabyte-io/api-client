import json
import argparse

from endpoints.jobs import ExabyteJobsEndpoint
from endpoints.login import ExabyteLoginEndpoint

HOST = 'platform.exabyte.io'
PORT = 443

JOB = {
    "_material": {
        "_id": ""
    },
    "compute": {
        "nodes": 1,
        "notify": "n",
        "ppn": 1,
        "queue": "D",
        "timeLimit": "01:00:00"
    },
    "model": {
        "method": {
            "data": {
                "pseudo": [
                    {
                        "_id": ""
                    }
                ]
            },
            "precision": {
                "kpoints": {
                    "shift": {
                        "x": 0,
                        "y": 0,
                        "z": 0
                    },
                    "value": {
                        "x": 2,
                        "y": 2,
                        "z": 2
                    }
                }
            },
            "workflow": {
                "_id": ""
            }
        }
    },
    "title": "TEST JOB"
}


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='username')
    parser.add_argument('-p', '--password', required=True, help='password')
    parser.add_argument('-m', '--material', required=True, help='material ID')
    parser.add_argument('-w', '--workflow', required=True, help='workflow ID')
    parser.add_argument('-s', '--pseudo', required=True, help='pseudo potential ID')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    login_endpoint = ExabyteLoginEndpoint(HOST, PORT, args.username, args.password)
    auth_params = login_endpoint.login()
    jobs_endpoint = ExabyteJobsEndpoint(HOST, PORT, **auth_params)
    JOB['_material']['_id'] = args.material
    JOB['model']['method']['workflow']['_id'] = args.workflow
    JOB['model']['method']['data']['pseudo'][0]['_id'] = args.pseudo
    job = jobs_endpoint.create_job(JOB)
    jobs_endpoint.submit_job(job['_id'])
    print json.dumps(jobs_endpoint.get_job(job['_id']), indent=4)
