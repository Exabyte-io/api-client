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
    parser.add_argument('-u', '--username', required=True, help='Your Exabyte username')
    parser.add_argument('-p', '--password', required=True, help='Your Exabyte password')
    parser.add_argument('-k', '--key', required=True, help='materialsproject key')
    parser.add_argument('-mi', '--material-id', dest="material_ids", action="append", required=True, help='material ID')
    parser.add_argument('-oi', '--owner-id', dest="owner_id", help='owner ID')
    parser.add_argument('-wi', '--workflow-id', dest="workflow_id", help='workflow ID')
    parser.add_argument('-pi', '--project-id', dest="project_id", help='project id')
    parser.add_argument('-t', '--tag', dest="tags", action="append", help='material/job tag')
    parser.add_argument('-j', '--job-prefix', dest="job_prefix", default="job", help='job name prefix')
    parser.add_argument('-ms', '--materials-set', dest="materials_set", default="set", help='materials set name')
    parser.add_argument('-js', '--jobs-set', dest="jobs_set", default="set", help='jobs set name')
    parser.add_argument('-c', '--cluster', help='cluster name')
    return parser.parse_args()


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


if __name__ == '__main__':
    args = parse_arguments()

    # params
    tags = args.tags or []
    cluster = args.cluster
    owner_id = args.owner_id
    job_prefix = args.job_prefix
    project_id = args.project_id
    workflow_id = args.workflow_id

    endpoint_options = LoginEndpoint.get_endpoint_options(args.host, args.port, args.username, args.password)

    # endpoints
    job_endpoints = JobEndpoints(**endpoint_options)
    charge_endpoints = ChargeEndpoints(**endpoint_options)
    material_endpoints = MaterialEndpoints(**endpoint_options)
    raw_property_endpoints = RawPropertiesEndpoints(**endpoint_options)

    # import materials and move them into a set
    materials = material_endpoints.import_from_materialsproject(args.key, args.material_ids, owner_id, tags)
    materials_set = material_endpoints.create_set({"name": args.materials_set, "owner": {"_id": owner_id}})
    [material_endpoints.move_to_set(m["_id"], "", materials_set["_id"]) for m in materials]

    # create jobs in a set and submit them
    compute = job_endpoints.get_compute(cluster)
    jobs_set = job_endpoints.create_set({"name": args.jobs_set, "projectId": project_id, "owner": {"_id": owner_id}})
    jobs = job_endpoints.create_by_ids(materials, workflow_id, project_id, owner_id, compute, job_prefix)
    job_endpoints.move_to_set_by_ids([j["_id"] for j in jobs], "", jobs_set["_id"])
    [job_endpoints.submit(id) for id in [j["_id"] for j in jobs]]

    # wait for jobs to finish and get the final jobs
    wait_for_jobs_to_finish(job_endpoints, jobs)
    jobs = job_endpoints.list(query={"_id": {"_id": [j["_id"] for j in jobs]}})

    # form final table
    keys = ["ID", "NAME", "TAGS", "N-SITES", "LAT-A", "LAT-B", "LAT-C", "LAT-ALPHA", "LAT-BETA", "LAT-GAMMA"]
    headers = ["-".join(("INI", key)) for key in keys]
    headers.extend(["-".join(("FIN", key)) for key in keys])
    headers.extend(["PRESSURE", "DIRECT-GAP", "INDIRECT-GAP", "WALL-DURATION", "CHARGE"])

    rows = []
    for job in jobs:
        initial_structure = material_endpoints.get(job["_material"]["_id"])

        # extract final structure
        unit_flowchart_id = job["workflow"]["subworkflows"][0]["units"][0]["flowchartId"]
        final_structure = raw_property_endpoints.get_property(job["_id"], unit_flowchart_id, "final_structure")["data"]

        # extract pressure
        unit_flowchart_id = job["workflow"]["subworkflows"][0]["units"][0]["flowchartId"]
        pressure = raw_property_endpoints.get_property(job["_id"], unit_flowchart_id, "pressure")["data"]["value"]

        # extract band gaps
        unit_flowchart_id = job["workflow"]["subworkflows"][1]["units"][1]["flowchartId"]
        band_gap_direct = raw_property_endpoints.get_direct_band_gap(job["_id"], unit_flowchart_id)
        band_gap_indirect = raw_property_endpoints.get_indirect_band_gap(job["_id"], unit_flowchart_id)

        # extract charge
        charge = charge_endpoints.get_by_job(job)

        # form table
        data = material_endpoints.flatten_material(initial_structure)
        data.extend(material_endpoints.flatten_material(final_structure))
        data.extend([pressure, band_gap_direct, band_gap_indirect])
        data.extend([charge["wallDuration"], charge["charge"]])

        rows.append(data)

    print tabulate(rows, headers, tablefmt='grid', stralign='center')
