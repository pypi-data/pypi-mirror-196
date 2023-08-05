from xclientai.utils.requests_utils import do_request
from xclientai.config import Config
from xclientai.datatypes import Job
from typing import List

class JobsClient:
    
    @classmethod
    def get_jobs(cls) -> List[Job]:        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.BASE_URL_X_BACKEND
            ),
            http_method="get"
        )
        
        list_job_dicts = response.json()["data"]
        jobs = []
        
        for job_dict in list_job_dicts:
            job = Job.parse_obj(job_dict)
            jobs.append(job)
            
        return jobs
    
    @classmethod
    def get_job_by_name(cls, job_name) -> List[Job]:        
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="get"
        )
        
        job_dict = response.json()["data"]
        job = Job.parse_obj(job_dict)
        
        return job
    
    @classmethod
    def delete_job(cls, job_name: str) -> Job:
        response = do_request(
            url="{}/v1/jobs/{}".format(
                Config.BASE_URL_X_BACKEND,
                job_name
            ),
            http_method="delete"
        )
        
        job_dict = response.json()["data"]
        job = Job.parse_obj(job_dict)
        return job
    
    @classmethod
    def create_job(cls, job: Job) -> Job:
        job_dict = job.dict()
        
        response = do_request(
            url="{}/v1/jobs/".format(
                Config.BASE_URL_X_BACKEND
            ),
            http_method="post",
            json_data=job_dict
        )
        
        returned_job_dict = response.json()["data"]
        returned_job = Job.parse_obj(returned_job_dict)
        
        return returned_job
       