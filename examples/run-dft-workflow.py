import time
import argparse

from tabulate import tabulate

from endpoints.jobs import JobEndpoints
from endpoints.login import LoginEndpoint
from endpoints.charges import ChargeEndpoints
from endpoints.materials import MaterialEndpoints
from endpoints.raw_properties import RawPropertiesEndpoints


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', '--host', default="platform.exabyte.io", help='RESTful API hostname')
    parser.add_argument('-P', '--port', type=int, default=443, help='RESTful API port')
    parser.add_argument('-S', '--insecure', action="store_true", default=False, help='Whether to use SSL')
    parser.add_argument('-u', '--username', required=True, help='Your Exabyte username')
    parser.add_argument('-p', '--password', required=True, help='Your Exabyte password')
    parser.add_argument('-k', '--key', required=True, help='materialsproject key')
    parser.add_argument('-mi', '--material-id', dest="material_ids", action="append", required=True, help='material ID')
    parser.add_argument('-wi', '--workflow-id', dest="workflow_id", help='workflow ID')
    parser.add_argument('-pi', '--project-id', dest="project_id", help='project id')
    parser.add_argument('-t', '--tag', dest="tags", action="append", help='material/job tag')
    parser.add_argument('-j', '--job-prefix', dest="job_prefix", default="job", help='job name prefix')
    parser.add_argument('-ms', '--materials-set', dest="materials_set", default="new-set", help='materials set name')
    parser.add_argument('-js', '--jobs-set', dest="jobs_set", default="new-set", help='jobs set name')
    return parser.parse_args()


def login(host, port, username, password, insecure):
    """
    Logs in with given parameters and returns credentials to use for further calls to the API.

    Returns:
        dict
    """
    endpoint = LoginEndpoint(host, port, username, password, secure=not insecure)
    response = endpoint.login()
    return {
        "host": host,
        "port": port,
        "secure": not insecure,
        "auth_token": response["X-Auth-Token"],
        "account_id": response["X-Account-Id"],
    }


def create_submit_jobs(job_endpoints, materials, workflow_id, project_id, job_prefix, tags, jobs_set):
    jobs = []
    for material in materials:
        job = job_endpoints.create({
            "_project": {
                "_id": project_id
            },
            "_material": {
                "_id": material["_id"]
            },
            "workflow": {
                "_id": workflow_id
            },
            "name": "-".join((job_prefix, material["name"])),
            "tags": tags
        })
        jobs.append(job)
        job_endpoints.move_to_set(job["_id"], "", jobs_set["_id"])
        job_endpoints.submit(job['_id'])
    return jobs


def get_jobs_in_state(jobs, state):
    return [job for job in jobs if job["status"] == state]


def print_status(jobs):
    error_jobs = get_jobs_in_state(jobs, "error")
    active_jobs = get_jobs_in_state(jobs, "active")
    finished_jobs = get_jobs_in_state(jobs, "finished")
    submitted_jobs = get_jobs_in_state(jobs, "submitted")
    header = ['SUBMITTED-JOBS', 'ACTIVE-JOBS', 'FINISHED-JOBS', 'ERROR-JOBS']
    row = [[len(submitted_jobs), len(active_jobs), len(finished_jobs), len(error_jobs)]]
    print tabulate(row, header, tablefmt='grid', stralign='center')
    print "\n"


def wait_for_jobs_to_finish(job_endpoints, jobs):
    while True:
        all_jobs = job_endpoints.list(query={"_id": {"$in": [job["_id"] for job in jobs]}}, projection={"status": 1})
        print_status(all_jobs)
        if all([job["status"] not in ["pre-submission", "submitted", "active"] for job in all_jobs]): break
        time.sleep(10)


def get_material_info(material):
    lattice = material["lattice"]
    return [
        material["_id"],
        lattice["a"],
        lattice["b"],
        lattice["c"],
        lattice["alpha"],
        lattice["beta"],
        lattice["gamma"],
    ]


if __name__ == '__main__':
    args = parse_arguments()

    endpoint_kwargs = login(args.host, args.port, args.username, args.password, args.insecure)

    # params
    tags = args.tags or []
    job_prefix = args.job_prefix
    project_id = args.project_id
    workflow_id = args.workflow_id

    # endpoints
    job_endpoints = JobEndpoints(**endpoint_kwargs)
    charge_endpoints = ChargeEndpoints(**endpoint_kwargs)
    material_endpoints = MaterialEndpoints(**endpoint_kwargs)
    raw_property_endpoints = RawPropertiesEndpoints(**endpoint_kwargs)

    # import materials
    materials = material_endpoints.import_from_materialsproject(args.key, args.material_ids, tags)

    # create a materials set and move materials into it
    materials_set = material_endpoints.create_set({"name": args.materials_set})
    for material in materials:
        material_endpoints.move_to_set(material["_id"], "", materials_set["_id"])

    # create jobs set
    jobs_set = job_endpoints.create_set({"name": args.jobs_set, "projectId": project_id})

    # create and submit jobs
    jobs = create_submit_jobs(job_endpoints, materials, workflow_id, project_id, job_prefix, tags, jobs_set)

    # wait for jobs to finish
    wait_for_jobs_to_finish(job_endpoints, jobs)

    # extract properties
    headers = [
        "NAME", "TAGS", "COORDINATES-LENGTH",
        "INI-ID", "INI-LAT-A", "INI-LAT-B", "INI-LAT-C", "INI-LAT-ALPHA", "INI-LAT-BETA", "INI-LAT-GAMMA",
        "FIN-ID", "FIN-LAT-A", "FIN-LAT-B", "FIN-LAT-C", "FIN-LAT-ALPHA", "FIN-LAT-BETA", "FIN-LAT-GAMMA",
        "PRESSURE", "DIRECT-GAP", "INDIRECT-GAP", "RUN-TIME", "COST"
    ]
    rows = []
    for job in jobs:
        initial_structure = material_endpoints.get(job["_material"]["_id"])

        # extract final structure
        unit_flowchart_id = job["workflow"]["subworkflows"][0]["units"][0]["flowchartId"]
        selector = {"source.info.jobId": job["_id"], "source.info.unitId": unit_flowchart_id, "slug": "final_structure"}
        final_structure = raw_property_endpoints.list(query=selector)[0]["data"]

        # extract pressure
        unit_flowchart_id = job["workflow"]["subworkflows"][0]["units"][0]["flowchartId"]
        selector = {"source.info.jobId": job["_id"], "source.info.unitId": unit_flowchart_id, "slug": "pressure"}
        pressure = raw_property_endpoints.list(query=selector)[0]["data"]["value"]

        # extract band_gaps
        unit_flowchart_id = job["workflow"]["subworkflows"][1]["units"][1]["flowchartId"]
        selector = {"source.info.jobId": job["_id"], "source.info.unitId": unit_flowchart_id, "slug": "band_gaps"}
        band_gaps = raw_property_endpoints.list(query=selector)[0]["data"]
        band_gaps_direct = next((v for v in band_gaps["values"] if v["type"] == "direct"), None)["value"]
        band_gaps_indirect = next((v for v in band_gaps["values"] if v["type"] == "indirect"), None)["value"]

        # extract charge
        charge = charge_endpoints.list(query={"jid": job["compute"]["cluster"]["jid"]})[0]

        # form data
        data = [
            initial_structure["name"],
            ", ".join(initial_structure["tags"]),
            len(initial_structure["basis"]["coordinates"])
        ]
        data.extend(get_material_info(initial_structure))
        data.extend(get_material_info(final_structure))
        data.append(pressure)
        data.extend([band_gaps_direct, band_gaps_indirect])
        data.extend([charge["wallDuration"], charge["charge"]])

        rows.append(data)

    print tabulate(rows, headers, tablefmt='grid', stralign='center')
