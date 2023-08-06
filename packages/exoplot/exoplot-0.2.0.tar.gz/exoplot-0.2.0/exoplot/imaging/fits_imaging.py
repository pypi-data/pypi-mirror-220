import os
import math
import json

from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord, get_constellation
from astropy.coordinates import Angle, Latitude, Longitude  # Angles

import astropy.units as u
from PIL import Image, ImageDraw, ImageFont

import pkg_resources
font_name = pkg_resources.resource_filename('exoplot', 'resources/arial.ttf')

def get_world_coordinate_system(path_to_fits_file):

    hdu = fits.open(path_to_fits_file)[0]

    # retrieve some settings from the header
    # First remove the 3rd axis from the header (RGB slices) because WCS works only in 2D.
    my_header = hdu.header
    my_header['NAXIS'] = 2

    ra_reference = my_header['CRVAL1']
    dec_reference = my_header['CRVAL2']
    width = my_header['NAXIS1']
    height = my_header['NAXIS2']

    wcs = WCS(my_header, naxis=2)
    return wcs, width, height, ra_reference, dec_reference


def draw_sky_cross(wcs, draw, ra, dec, size=20, width=2, fill=(255, 255, 0), frame='icrs'):
    sky = SkyCoord(Longitude([ra], unit=u.deg),Latitude([dec], unit=u.deg),frame=frame)
    
    x,y = wcs.world_to_pixel(sky)

    # do not draw offscreen
    if x < 0 or y < 0:
        return

    draw.line(((x-size,y), (x+size,y)), fill=fill, width=width)
    draw.line(((x,y-size), (x,y+size)), fill=fill, width=width)


def draw_sky_circle(wcs, draw, ra, dec, size=20, width=2, outline='yellow', fill=None):
    sky = SkyCoord(Longitude([ra], unit=u.deg), Latitude([dec], unit=u.deg), frame='icrs')

    x, y = wcs.world_to_pixel(sky)

    # do not draw offscreen
    if x < 0 or y < 0:
        return

    draw.ellipse(((x - size, y - size), (x + size, y + size)), outline=outline, fill=fill, width=width)


def draw_degree_grid(wcs, draw, scale, ra, dec, ra_labels, dec_labels, step, frame='icrs'):
    sky1 = SkyCoord(Longitude([ra], unit=u.deg),Latitude([dec], unit=u.deg),frame=frame)
    sky2 = SkyCoord(Longitude([ra+step], unit=u.deg), Latitude([dec], unit=u.deg), frame=frame)
    sky3 = SkyCoord(Longitude([ra+step], unit=u.deg),Latitude([dec+step], unit=u.deg),frame=frame)
    sky4 = SkyCoord(Longitude([ra], unit=u.deg), Latitude([dec+step], unit=u.deg), frame=frame)

    x1,y1 = wcs.world_to_pixel(sky1)
    x2,y2 = wcs.world_to_pixel(sky2)
    x3,y3 = wcs.world_to_pixel(sky3)
    x4,y4 = wcs.world_to_pixel(sky4)

    # do not draw offscreen
    if x1<0 and y1<0 and x2<0 and y2<0 and x3<0 and y3<0 and x4<0 and y4<0:
        return

    xy = ((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1))
    draw.polygon((xy))

    if dec == round(dec_labels):
        a = Angle(ra, u.deg)
        ra_string = a.to_string(unit=u.hour)
        font = ImageFont.truetype(font_name, int(scale/2), encoding="unic")
        draw.text((x1, (y1+y3)/2), str(ra_string), (255, 255, 0),font=font)

    if ra == round(ra_labels):
        dec_string = str(dec)+'deg'
        font = ImageFont.truetype(font_name, int(scale/2), encoding="unic")
        draw.text((x1+10, y1), dec_string, (255, 255, 0),font=font)


def draw_minutes_grid(wcs, draw, scale, ra, dec, ra_labels, dec_labels, step, frame='icrs'):
    sky1 = SkyCoord(Longitude([ra], unit=u.deg), Latitude([dec], unit=u.deg), frame=frame)
    sky2 = SkyCoord(Longitude([ra + step], unit=u.deg), Latitude([dec], unit=u.deg), frame=frame)
    sky3 = SkyCoord(Longitude([ra + step], unit=u.deg), Latitude([dec + step], unit=u.deg), frame=frame)
    sky4 = SkyCoord(Longitude([ra], unit=u.deg), Latitude([dec + step], unit=u.deg), frame=frame)

    x1, y1 = wcs.world_to_pixel(sky1)
    x2, y2 = wcs.world_to_pixel(sky2)
    x3, y3 = wcs.world_to_pixel(sky3)
    x4, y4 = wcs.world_to_pixel(sky4)

    # do not draw offscreen
    if x1<0 and y1<0 and x2<0 and y2<0 and x3<0 and y3<0 and x4<0 and y4<0:
        return

    xy = ((x1, y1), (x2, y2), (x3, y3), (x4, y4), (x1, y1))
    draw.polygon((xy))

    if dec == round(dec_labels):
        a = Angle(ra, u.deg)
        ra_string = a.to_string(unit=u.hour)
        font = ImageFont.truetype(font_name, int(scale/2), encoding="unic")
        draw.text((x1, (y1+y3)/2), str(ra_string), (255, 255, 0),font=font)

    if ra == round(ra_labels):
        dec_string = str(dec)+'deg'
        font = ImageFont.truetype(font_name, int(scale/2), encoding="unic")
        draw.text((x1+10, y1), dec_string, (255, 255, 0),font=font)


def draw_grid(path_to_fits_file, path_to_input_image_file, path_to_output_image_file, title, grid_type="degrees"):

    try:
        print("draw_grid on "+path_to_input_image_file)
        wcs, width, height, ra_reference, dec_reference = get_world_coordinate_system(path_to_fits_file)

        # use the astropy WCS package to convert pixel to world coordinates
        # https://docs.astropy.org/en/stable/wcs/
        # https://docs.astropy.org/en/stable/wcs/wcsapi.html

        coord = wcs.pixel_to_world(0, 0)
        ra_end = (coord.ra.dms.d) + ((coord.ra.dms.m)/60) + ((coord.ra.dms.s)/3600)
        dec_end = (coord.dec.signed_dms.sign) * ((coord.dec.signed_dms.d) + ((coord.dec.signed_dms.m)/60) + ((coord.dec.signed_dms.s)/3600))

        coord = wcs.pixel_to_world(width, height)
        ra_start = (coord.ra.dms.d) + ((coord.ra.dms.m)/60) + ((coord.ra.dms.s)/3600)
        dec_start = (coord.dec.signed_dms.sign) * ((coord.dec.signed_dms.d) + ((coord.dec.signed_dms.m)/60) + ((coord.dec.signed_dms.s)/3600))

        constellation = coord.get_constellation()

        try:
            im = Image.open(path_to_input_image_file)
        except:
            error = "ERROR: " + path_to_input_image_file + ' not found'
            print(error)
            raise (Exception(error))

        im_new = im.copy()
        draw = ImageDraw.Draw(im_new)

        # scale the font based on the image size
        scale = int(width/ 60)
        font_title = ImageFont.truetype(font_name, scale * 2, encoding="unic")
        font_subtitle = ImageFont.truetype(font_name, scale, encoding="unic")

        text_start_x = scale * 2
        text_start_y = scale * 2
        line_spacing = int(scale*2*0.7)

        draw.text((text_start_x, text_start_y), title, (255, 255, 255),font=font_title)
        #draw.text((text_start_x, text_start_y), title, (255, 255, 255),font=font_title)
        # draw.text((text_start_x, text_start_y + (2 * scale)), constellation, (255, 255, 255),font=font_subtitle)

        # draw.text((text_start_x, text_start_y + line_spacing*2), title, (255, 255, 255),font=font_subtitle)
        s1 = round(ra_reference,0)
        s2 = round(dec_reference,0)
        location = 'RA,dec = ' + str(s1) + ',' + str(s2)
        draw.text((text_start_x, text_start_y + line_spacing*2), location, (255, 255, 255),font=font_subtitle)

        draw_sky_cross(wcs, draw, s1, s2, int(scale / 2), width=int(scale / 5), fill=(255, 0, 0), frame='icrs')

        # around the pole the decs could be switched
        if dec_start > dec_end:
            ff = dec_start
            dec_start = dec_end
            dec_end = ff

        if ra_start > ra_end:
            ff = ra_start
            ra_start = ra_end
            ra_end = ff

        # find the field-of-view for both RA and dec
        fov_dec = dec_end - dec_start
        fov_ra = ra_end - ra_start
        fov = str(round(fov_ra,1))+', '+str(round(fov_dec,1))
        
        if fov_ra > 15 or fov_dec > 15:
            # for large field of views, increase the space between the grid lines
            # because of polar distortions, just try to draw the full globe.
            step = 10
            x_start = 0
            x_end = 360
            y_start = -90
            y_end = +90
        else:
            # for smaller fov's, take some extra margin to make sure
            # that the grids cover the full image and not show up as single squares
            step = 1
            x_start = int(ra_start) - 6
            x_end =int(ra_end) + 6
            y_start = int(dec_start) - 6
            y_end = int(dec_end) + 6

        for x in range(x_start, x_end, step):
            # print(x)
            for y in range(y_start, y_end, step):
                try:
                    draw_sky_cross(wcs, draw, x, y, int(scale / 5))
                    draw_degree_grid(wcs, draw, scale, x, y, ra_reference, dec_reference, step)
                except:
                    pass

            # save result
        path_to_new_file = path_to_output_image_file

        if grid_type == "equatorial":
            # calculate rotation
            sky1 = SkyCoord(Longitude([ra_reference], unit=u.deg), Latitude([dec_reference], unit=u.deg), frame='icrs')
            sky2 = SkyCoord(Longitude([ra_reference+1], unit=u.deg), Latitude([dec_reference], unit=u.deg), frame='icrs')
            x1, y1 = wcs.world_to_pixel(sky1)
            x2, y2 = wcs.world_to_pixel(sky2)

            dx = x1 - x2
            dy = y2 - y1
            rotation = math.degrees(math.atan(dy/dx))
            im_new = im_new.rotate(-rotation)

            # save result
            path_to_new_file = path_to_input_image_file.replace(".", "_grid_eq.")

        print("path_to_new_file = " + path_to_new_file)
        im_new.save(path_to_new_file)

        #im_new.show()

        return path_to_new_file, ra_start,ra_end,dec_start,dec_end, fov


    except Exception as error:
        print(str(error))


def get_min_max_ra_dec(path_to_fits_file):

    try:
        wcs, width, height, _, _ = get_world_coordinate_system(path_to_fits_file)

        coord = wcs.pixel_to_world(0, 0)
        ra_end = (coord.ra.dms.d) + ((coord.ra.dms.m)/60) + ((coord.ra.dms.s)/3600)
        dec_end = (coord.dec.signed_dms.sign) * ((coord.dec.signed_dms.d) + ((coord.dec.signed_dms.m)/60) + ((coord.dec.signed_dms.s)/3600))

        coord = wcs.pixel_to_world(width, height)
        ra_start = (coord.ra.dms.d) + ((coord.ra.dms.m)/60) + ((coord.ra.dms.s)/3600)
        dec_start = (coord.dec.signed_dms.sign) * ((coord.dec.signed_dms.d) + ((coord.dec.signed_dms.m)/60) + ((coord.dec.signed_dms.s)/3600))

        # the image could be upside down
        if dec_start > dec_end:
            ff = dec_start
            dec_start = dec_end
            dec_end = ff

        if ra_start > ra_end:
            ff = ra_start
            ra_start = ra_end
            ra_end = ff

        return ra_start,ra_end,dec_start,dec_end

    except Exception as error:
        print(str(error))



def plot_on_image(path_to_fits_file, path_to_input_image_file, path_to_output_image_file, payload):
    try:
        wcs, width, height,_,_ = get_world_coordinate_system(path_to_fits_file)

        im = Image.open(path_to_input_image_file)
        im_new = im.copy()
        draw = ImageDraw.Draw(im_new, 'RGBA')

        font_title = ImageFont.truetype(font_name, 50, encoding="unic")
        font_ticks = ImageFont.truetype(font_name, 25, encoding="unic")

        list_of_symbols = json.loads(payload)
        for symbol in list_of_symbols:
            #print(str(symbol))
            ra = symbol['ra']
            dec = symbol['dec']
            size = abs(symbol['size'])
            sky = SkyCoord(Longitude([ra], unit=u.deg), Latitude([dec], unit=u.deg))

            try:
                x, y = wcs.world_to_pixel(sky)

                if symbol['shape'] == 'cross':
                    draw_sky_cross(wcs, draw, ra, dec, size, width=1, fill=symbol['color'], frame='icrs')
                    draw.text((x, y+size), symbol['label'], symbol['color'], font=font_ticks)

                if symbol['shape'] == 'circle_outline':
                    draw_sky_circle(wcs, draw, ra, dec, size=int(size), width=2, outline=symbol['color'], fill=None)
                    draw.text((x-size,y-(size*2)-50), symbol['label'], symbol['color'], font=font_title)

                if symbol['shape'] == 'circle':
                    draw_sky_circle(wcs, draw, ra, dec, size=int(size), width=2, outline=symbol['color'], fill=None)
                    draw.text((x-size,y-(size*2)-50), symbol['label'], symbol['color'], font=font_title)

                if symbol['shape'] == 'exoplanet':
                    draw_sky_circle(wcs, draw, ra, dec, size=int(size), width=2, outline=symbol['color'], fill=None)
                    draw.text((x-size,y-(size*2)-5), symbol['label'], symbol['color'], font=font_ticks)

            except:
                # something went wrong, don't draw but continue
                pass

        # save result
        path_to_new_file = path_to_output_image_file
        im_new.save(path_to_new_file)
        im_new.show()

        return path_to_new_file

    except Exception as error:
        print(str(error))

