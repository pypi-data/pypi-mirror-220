import datetime

import schedule


class Scheduler(schedule.Scheduler):

    # noinspection PyProtectedMember
    def run_pending(self) -> None:
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            try:
                self._run_job(job)
            except Exception as e:
                job.last_run = datetime.datetime.now()
                job._schedule_next_run()
                raise e
