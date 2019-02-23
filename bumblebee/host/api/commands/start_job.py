from bumblebee.host.api.rest import RestApi
from bumblebee.host.events import JobEvents
from bumblebee.host.types import Job


class StartJob(object):
    def __init__(self,
                 api: RestApi):
        self.api = api

    def __call__(self, job_id):
        url = f"/host/jobs/{job_id}"

        token_api = self.api.with_token()
        response = token_api.put(url, {
            "status": "in_progress"
        })

        if not response.ok:
            return

        job_response = token_api.get(url)

        if not job_response.ok:
            return

        json = job_response.json()
        job = Job(
            id=json["id"],
            name=json["name"],
            status=json["status"],
            file_url=json["url"]
        )

        JobEvents.JobStarted(job).fire()