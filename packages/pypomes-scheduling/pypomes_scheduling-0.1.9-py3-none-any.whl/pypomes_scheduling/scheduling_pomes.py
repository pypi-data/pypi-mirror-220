from datetime import datetime
from pypomes_core import exc_format
from typing import Final
import logging
import pytz
import re
import sys
from .__threaded_scheduler import __ThreadedScheduler

__REGEX_VERIFY_CRON: Final[str] = "/(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|" \
                                  "(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})"

__scheduler: __ThreadedScheduler


def scheduler_create(errors: list[str], timezone: pytz.BaseTzInfo,
                     retry_interval: int, logger: logging.Logger = None) -> bool:
    """
    Create the threaded job scheduler. This is a wrapper around the package *APScheduler*.

    :param errors: incidental errors
    :param timezone: the timezone to be used
    :param retry_interval: interval between retry attempts, in minutes
    :param logger: optional logger object
    :return: True if scheduler was created, or False otherwise
    """
    global __scheduler
    # inicialize the return variable
    result: bool = False

    try:
        __scheduler = __ThreadedScheduler(timezone, retry_interval, logger)
        __scheduler.daemon = True
        result = True
    except Exception as e:
        errors.append(f"Error creating the job scheduler: {exc_format(e, sys.exc_info())}")

    return result


def scheduler_add_job(errors: list[str], job: callable, job_id: str, job_name: str,
                      job_cron: str = None, job_start: datetime = None,
                      job_args: tuple = None, job_kwargs: dict = None) -> bool:
    """
    Schedule the job identified as *job_id* and named as *job_name*,
    with the *CRON* expression *job_cron*, starting at the timestamp *job_start*.
    Positional arguments for the scheduled job may be provided in *job_args*.
    Named arguments for the scheduled job may be provided in *job_kwargs*.
    Return *True* if the scheduling was successful.

    :param errors: incidental errors
    :param job: the job to be scheduled
    :param job_id: the id of the job to be scheduled
    :param job_name: the name of the job to be scheduled
    :param job_cron: the CRON expression
    :param job_start: the start timestamp
    :param job_args: the positional argumens for the scheduled job
    :param job_kwargs: the named argumens for the scheduled job
    :return: True if the job was successfully scheduled, or None otherwise
    """
    global __scheduler

    # initialize the return variable
    result: bool = False

    # has a valid CRON expression been provided ?
    if job_cron is not None and re.search(__REGEX_VERIFY_CRON, job_cron) is None:
        # no, report the error
        errors.append(f"Invalid CRON expression: '{job_cron}'")
    else:
        # yes, proceed with the scheduling
        try:
            __scheduler.schedule_job(job, job_id, job_name, job_cron, job_start, job_args, job_kwargs)
            result = True
        except Exception as e:
            errors.append(f"Error scheduling the job '{job_name}', id '{job_id}', "
                          f"with CRON '{job_cron}': {exc_format(e, sys.exc_info())}")

    return result


def scheduler_add_jobs(errors: list[str],
                       jobs: list[tuple[callable, str, str, str, datetime, tuple, dict]]) -> int:
    """
    Schedule the jobs described in *jobs*, starting at the given *start*.
    Each element in the job list is a *tuple* with the corresponding job data:
    *(callable function, job id, job name, CRON expression, start timestamp, job args, job kwargs)*.
    Only the first three data items are required.

    :param errors: incidental errors
    :param jobs: list of tuples containing the jobs to schedule
    :return: the number of jobs effectively scheduled
    """
    global __scheduler

    # initialize the return variable
    result: int = 0

    # traverse the job list and attempt the scheduling
    for job in jobs:
        # process the optional arguments
        job_cron: str = job[3] if len(job) > 3 else None
        job_start: datetime = job[4] if len(job) > 4 else None
        job_args: tuple = job[5] if len(job) > 5 else None
        job_kwargs: dict = job[6] if len(job) > 6 else None
        # add to the return valiable, if scheduling was successful
        if scheduler_add_job(errors, job[0], job[1], job[2], job_cron, job_start, job_args, job_kwargs):
            result += 1

    return result


def scheduler_start(errors: list[str]):
    """
    Start the scheduler.

    :param errors: incidental errors
    :return: True if the scheduler has started, False otherwise
    """
    global __scheduler

    # initialize the return variable
    result: bool = False

    try:
        __scheduler.start()
        result = True
    except Exception as e:
        errors.append(f"Error starting the scheduler': {exc_format(e, sys.exc_info())}")

    return result


def scheduler_stop():
    """
    Stop the scheduler.
    """
    global __scheduler

    __scheduler.stop()
