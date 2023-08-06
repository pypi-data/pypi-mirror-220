import base64
import json
import tempfile
from ast import Dict
from typing import Optional, Union

import strangeworks as sw
from dimod import (
    BinaryQuadraticModel,
    ConstrainedQuadraticModel,
    DiscreteQuadraticModel,
    SampleSet,
)
from strangeworks.core.client.jobs import Job
from strangeworks.core.errors.error import StrangeworksError


class OptimizationJob:
    def __init__(
        self,
        model: Union[BinaryQuadraticModel, str]
        | ConstrainedQuadraticModel
        | DiscreteQuadraticModel
        | Dict,
        solver: dict,
        var_type: str = "BINARY",
        lagrange_multiplier: float = 0.0,
    ) -> None:
        self.var_type = var_type
        self.lagrange_multiplier = lagrange_multiplier
        self.solver = solver

        provider = solver["solver"].split(".")[0]
        target = solver["solver"].split(".")[1]
        if len(solver["solver"].split(".")) > 2:
            # needed for something like dwave.Advantage_system4.1
            for iter in range(2, len(solver["solver"].split("."))):
                target += "." + solver["solver"].split(".")[iter]

        if provider == "dwave" or provider == "dwave_swhybrid":
            if type(model) == BinaryQuadraticModel:
                self.model = json.dumps(model.to_serializable())
                self.run_path = "qubo"
            elif type(model) == ConstrainedQuadraticModel:
                cqm_file = model.to_file()
                cqm_bytes = base64.b64encode(cqm_file.read())
                self.model = cqm_bytes.decode("ascii")
                self.run_path = "cqm"
            elif type(model) == DiscreteQuadraticModel:
                dqm_file = model.to_file()
                dqm_bytes = base64.b64encode(dqm_file.read())
                self.model = dqm_bytes.decode("ascii")
                self.run_path = "dqm"
        elif provider == "gurobi":
            self.run_path = target
            if type(model) == BinaryQuadraticModel:
                if target != "qubo":
                    raise StrangeworksError("Model and backend do not match")
                self.model = json.dumps(model.to_serializable())
            elif type(model) == str:
                if model.split(".")[-1] != "mps":
                    raise StrangeworksError("Input file must be .mps")

                with open(model, "r") as f:
                    self.model = f.read()


class StrangeworksOptimization:
    """Strangeworks client object."""

    def __init__(self, resource_slug: Optional[str] = " ") -> None:
        if resource_slug != " " and resource_slug != "":
            self.rsc = sw.resources(slug=resource_slug)[0]
        else:
            rsc_list = sw.resources()
            for rr in range(len(rsc_list)):
                if rsc_list[rr].product.slug == "optimization":
                    self.rsc = rsc_list[rr]

        # self.backend_list = " "

    def add_sub_resource_credentials(self, resource_slug):
        self.sub_rsc = sw.resources(slug=resource_slug)[0]

        return self.sub_rsc.product.name

    def run(self, qubo_job: OptimizationJob) -> str:
        payload = qubo_job.__dict__
        payload["resource_slug"] = self.sub_rsc.slug
        path = payload["run_path"]
        payload.pop("run_path")

        result = sw.execute(self.rsc, payload=payload, endpoint=path)
        return Job(
            slug=result["job_slug"],
            child_jobs=None,
            external_identifier=None,
            resource=self.rsc,
            status=result["job_status"],
            is_terminal_state=None,
        )

    def get_results(self, sw_job):
        current_status = self.get_status(sw_job)
        if current_status != "COMPLETED":
            new_status = self.update_status(sw_job)

        if current_status == "COMPLETED" or new_status == "COMPLETED":
            if type(sw_job) is dict:
                job_slug = sw_job["slug"]
            else:
                job_slug = sw_job.slug

            result = sw.execute(self.rsc, endpoint=f"jobs/{job_slug}")
            result = json.loads(result["samples_url"])

            try:
                return SampleSet.from_serializable(result)
            except Exception:
                try:
                    # Gurobi BQM/QUBO Solutions
                    return SampleSet.from_serializable(result["results"])
                except Exception:
                    # MPS Solutions
                    return result
        else:
            return new_status

    def upload_model(self, bqm: BinaryQuadraticModel) -> str:
        with tempfile.NamedTemporaryFile(mode="w+") as t:
            json.dump(bqm.to_serializable(), t)
            t.flush()

            return sw.upload_file(t.name)

    def get_status(self, sw_job):
        # Will get the current status of the job
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        else:
            job_slug = sw_job.slug

        return sw.jobs(slug=job_slug)[0].status

    def update_status(self, sw_job):
        # Will contact the backends API to refresh/update the status of the job
        if type(sw_job) is dict:
            job_slug = sw_job.get("slug")
        else:
            job_slug = sw_job.slug

        if sw.jobs(slug=job_slug)[0].status != "COMPLETED":
            res = sw.execute(self.rsc, endpoint=f"jobs/{job_slug}")
            return res["job_status"]
        else:
            return sw.jobs(slug=job_slug)[0].status

    def backends(self):
        """
        To-Do: Add cross check as to which backends the current user actually has
          access to.
                Currently, this just lists all backends that could work with the qaoa
                  service.
        """

        self.backends = sw.backends(backend_type_slugs=["optimization"])

        return self.backends
