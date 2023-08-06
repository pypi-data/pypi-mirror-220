"""
    File name: service_submet.py
    Author: Nico Vermaas
    Date created: 2023-07-16
    Description: - submit job to astrometry.net
"""
import time
from exoplot.astrometry.astrometry_client import Client


def get_job_id(submission_id, args):

    client = Client(apiurl=args.astrometry_url+"/api/")
    client.login(apikey=args.astrometry_api_key)
    submission_result = client.sub_status(submission_id, justdict=True)
    print("submission_result :" + str(submission_result))

    try:
        job_id = str(submission_result['jobs'][0])
        return job_id
    except:
        return None


def check_submission_status(submission_id, args):
    """
    check of the pipeline at astrometry is done processing the submitted image
    :param submission_id:
    :return:
    """

    try:
        job_id = get_job_id(submission_id, args)
        job_results = get_job_results(job_id, args, False)
        print("job_results: " + str(job_results))
        if job_results['job']['status']=='success':
            radius = job_results['calibration']['radius']
            return 'success',radius
        if job_results['job']['status']=='failure':
            return 'failure',0
    except:
        return 'unfinished',0
    return "unknown"

def get_job_results(job_id, args, justdict):
    """
    {'objects_in_field':
        ['The star 61Leo', 'The star υ2Hya', 'The star φLeo', 'The star υ1Hya',
         'The star γCrt', 'The star Alkes (αCrt)', 'The star μHya', 'The star λHya',
         'The star δCrt', 'The star νHya', 'Part of the constellation Hydra (Hya)',
         'Part of the constellation Crater (Crt)'],
     'machine_tags':
        ['The star 61Leo', 'The star υ2Hya', 'The star φLeo', 'The star υ1Hya', 'The star γCrt',
         'The star Alkes (αCrt)', 'The star μHya', 'The star λHya', 'The star δCrt', 'The star νHya',
         'Part of the constellation Hydra (Hya)', 'Part of the constellation Crater (Crt)'],
     'status': 'success',
     'tags':
        ['The star 61Leo', 'The star υ2Hya', 'The star φLeo', 'The star υ1Hya',
         'The star γCrt', 'The star Alkes (αCrt)', 'The star μHya', 'The star λHya',
         'The star δCrt', 'The star νHya', 'Part of the constellation Hydra (Hya)',
         'Part of the constellation Crater (Crt)'],
     'calibration':
            {'orientation': 180.47305689878488,
            'dec': -11.294944542800003,
            'pixscale': 541.8204596987174,
            'radius': 20.721878048048463,
            'parity': 1.0,
            'ra': 166.270006359},
            'original_filename': 'SouthPoleTransformed/1565.png'
            }

    :param job_id:
    :return:
    """
    # astrobaseIO.report("---- get_job_results(" + str(job_id) + ")", "print")
    # login to astrometry with the API_KEY
    client = Client(apiurl=args.astrometry_url+"/api/")
    client.login(apikey=args.astrometry_api_key)

    result = client.job_status(job_id, justdict=justdict)
    return result


def get_submission(submission_id, args):
    """
    check of the pipeline at astrometry is done processing the submitted image
    :param submission_id:
    :return:
    """
    # login to astrometry with the API_KEY

    client = Client(apiurl=args.astrometry_url+"/api/")
    client.login(apikey=args.astrometry_api_key)

    result = client.sub_status(submission_id, justdict=True)
    return result

#-------------------------------------------------------------------------------------
def do_submit_jobs(args):

    def submit_job_to_astrometry(path_to_image):
        """
        http://astrometry.net/doc/net/api.html
        :param path_to_file:
        :return:
        """

        # login to astrometry with the API_KEY
        client = Client(apiurl=args.astrometry_url+"/api/")
        client.login(apikey=args.astrometry_api_key)

        result = client.upload(fn=path_to_image)

        print(result)
        job = result['subid']
        job_status = result['status']
        return job, job_status

    # --- start of function body ---

    # do the magic!
    # when using files
    submission_id, submission_status = submit_job_to_astrometry(args.path_to_image)
    print(submission_id, submission_status)

    return submission_id

#-------------------------------------------------------------------------------------
def do_check_submission_status(submission_id, args):

    job_status = None
    while job_status != "success":
        print(f"checking status of {submission_id}")
        job_status, radius = check_submission_status(submission_id, args)

        if job_status != "success":
            # not successful yet, wait for 5 seconds
            print(f"job_status: {job_status}, sleep for 5 seconds...")
            time.sleep(5)

# --- Main Service -----------------------------------------------------------------------------------------------

def do_submit(args):

    # submit new jobs to astrometry.net
    if args.submission_id == None:
        submission_id = do_submit_jobs(args)
    else:
        submission_id = args.submission_id

    # check if the job is ready and handle results on success.
    do_check_submission_status(submission_id, args)
    print(f"https://nova.astrometry.net/status/{submission_id}")

    return submission_id