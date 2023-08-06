"""
    File name: service_do_data_monitor.py
    Author: Nico Vermaas
    Date created: 2019-10-14
    Description: - checks for new images in a given directory (_locallanding_pad)
                 - new images are then added as observation and dataproduct to the astrobase backend
"""


import os
import platform
import urllib.request

from .service_submit import get_submission, get_job_id

def get_fits_header(filename):

    fits_dict = {}
    with open(filename, "r") as fits_file:

        # read the file as a long line
        line = fits_file.readline()

        # split the long line in 80 character chunks
        n = 80
        chunks = [line[i:i + n] for i in range(0, len(line), n)]

        for chunk in chunks:
            try:
                # retrieve the key/value apier
                key,value_comment = chunk.split("=")

                # split off the comments from the value
                value,comment = value_comment.split("/")

                fits_dict[key.strip()]=value.strip()
            except:
                pass
        #print(str(fits_dict))
        return fits_dict


#-------------------------------------------------------------------------------------
def do_handle_processed_jobs(submission_id, args):

    def do_create_dataproducts(submission_id, args):

        def add_dataproduct(job_id, sub_url,file_end, dataproduct_type):
            url = args.astrometry_url + sub_url + job_id
            destination = os.path.join(args.output_dir, job_id + file_end)
            if not os.path.exists(destination):
                urllib.request.urlretrieve(url, destination)
                print(f"added {destination}")

        submission = get_submission(submission_id,args)

        try:
            job_id = str(submission['job_calibrations'][0][0])
            skyplot_id = str(submission['job_calibrations'][0][1])
        except:
            print('job_calibrations has no data yet, waiting a heartbeat...')

            # check if there is something wrong with the job
            # job_results = get_job_results(submission_id, True)

            return False

        # create a directory per job to store all the results
        if not os.path.exists(args.output_dir):
            os.makedirs(args.output_dir)

        # retrieve images and store as dataproducts
        # http://nova.astrometry.net/sky_plot/zoom0/2390269
        dataproducts = ""

        url = args.astrometry_url + "/sky_plot/zoom0/" + skyplot_id
        destination = os.path.join(args.output_dir, job_id + "_sky_globe.jpg")
        if not os.path.exists(destination):
            urllib.request.urlretrieve(url, destination)
            print(f"added {destination}")

        # http://nova.astrometry.net/sky_plot/zoom1/2390269
        url = args.astrometry_url + "/sky_plot/zoom1/" + skyplot_id
        destination = os.path.join(args.output_dir, job_id + "_sky_plot.jpg")
        if not os.path.exists(destination):
            urllib.request.urlretrieve(url, destination)
            print(f"added {destination}")

        add_dataproduct(job_id,"/annotated_full/", "_annotated.jpg", "annotated")
        add_dataproduct(job_id, "/new_fits_file/", ".fits", "fits")

        # the following files are also available for download, but are not used in this exoplanet tool
        #add_dataproduct(job_id,"/red_green_image_full/", "_redgreen.jpg", "redgreen")
        #add_dataproduct(job_id,"/extraction_image_full/", "_extraction.jpg", "extraction")
        #add_dataproduct(job_id,"/rdls_file/", "_rdls_file.fits", "nearby_stars_fits")
        #add_dataproduct(job_id,"/wcs_file/", "_wcs_file.fits", "wcs_fits")
        #add_dataproduct(job_id,"/axy_file/", "_axy_file.fits", "stars_fits")
        #add_dataproduct(job_id, "/corr_file/", "_corr_file.fits", "corr_fits")

        return job_id


    # --- start of function body ---
    job_id = do_create_dataproducts(submission_id, args)
    return job_id

# --- Main Service -----------------------------------------------------------------------------------------------

def do_processor(submission_id, args):

    # handle the results
    job_id = do_handle_processed_jobs(submission_id, args)
    return job_id