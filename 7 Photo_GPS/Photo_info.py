# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 09:58:04 2019

@author: Shaw
"""
from PIL import Image, ImageDraw, ImageFont
import exifread
import fractions
#import pyexiv2
#from pyexiv2.metadata import ImageMetadata
import re
import os

colorkey = 'red'
colors = {}
colors['red'] = (255, 0, 0, 255)
colors['blue'] = (0, 0, 255, 255)
colors['green'] = (0, 255, 0, 255)
colors['white'] = (255, 255, 255, 255)
colors['black'] = (0, 0, 0, 255)
# format long & lat
def format_pos(ref, flag, pos):
    datastr = ''
    if(flag == 'lon' or flag == 'lat'):
        try:
            ideg, imin, isec = [x.replace(' ', '') for x in str(pos)[1:-1].split(',')]
            ideg = int(ideg)
            imin = int(imin)
            if '/' in isec:
                isec = [x.replace('/', ' ') for x in str(isec).split(',')]
                p1, p2 = [x.replace('/', ' ') for x in isec[0].split(' ')]
                isec = int(p1)/int(p2)
            else:
                isec = float(isec)
            datastr = "%(ref)s:   %(deg)02d°%(min)02d'%(sec)08.6f\"" \
                   %{'ref':ref, 'deg':ideg, 'min':imin,'sec':isec}
            if (flag == 'lon'):
                datastr = "%(ref)s: %(deg)03d°%(min)02d'%(sec)08.6f\"" \
                   %{'ref':ref, 'deg':ideg, 'min':imin,'sec':isec}
        except:
            print('no infomation of ', flag)    
    elif(flag == 'h'):
        try:
            datastr = 'heigth: %(h)5dm'%{'h': str(pos)}
        except:
            datastr = '0 m'
    return datastr
        
# get file info
def get_exif_data(filename):
    GPS = {}
    data = {}
    date = ' '
    # initial
    GPS['GPS GPSLatitudeRef'] = ' '
    GPS['GPS GPSLatitude'] = 'none'
    GPS['GPS GPSLongitudeRef'] = ' '
    GPS['GPS GPSLongitude'] = 'none'
    GPS['GPS GPSAltitudeRef'] = ' '
    GPS['GPS GPSAltitude'] = 'none'
    data['lat'] = ' '
    data['lon'] = ' '
    data['h'] = ' '
    fd = open(filename, 'rb')
    tags = exifread.process_file(fd)
    fd.close()
    print(tags)
    # show exif info
    for tag, value in tags.items():
        if re.match('GPS GPSLatitudeRef', tag):
            GPS['GPS GPSLatitudeRef'] = str(value)
        elif re.match('GPS GPSLatitude', tag):
            GPS['GPS GPSLatitude'] = str(value)
            data['lat'] = format_pos(GPS['GPS GPSLatitudeRef'], 'lat', value)
        elif re.match('GPS GPSLongitudeRef', tag):
            GPS['GPS GPSLongitudeRef'] = str(value)
        elif re.match('GPS GPSLongitude', tag):
            GPS['GPS GPSLongitude'] = str(value)
            data['lon'] = format_pos(GPS['GPS GPSLongitudeRef'], 'lon', value)
        elif re.match('GPS GPSAltitudeRef', tag):
            GPS['GPS GPSAltitudeRef'] = str(value)
        elif re.match('GPS GPSAltitude', tag):
            GPS['GPS GPSAltitude'] = str(value)
            data['h'] = format_pos(GPS['GPS GPSAltitudeRef'], 'h', value)
        elif re.match('Image DateTime', tag):
            date = str(value)
    return data, date, GPS

def coordinate2rational(D, M, S):
    return (fractions.Fraction(D, 1), \
            fractions.Fraction(int((M + S / 60) * 100), 100), \
            fractions.Fraction(0, 1))

# get file info
def add_exif_data(filename, date, pos):
    # EXIF template
#    template = ImageMetadata('E:/code/CODE/python/7 Photo_GPS/eg.jpg')
#    template.read() 
    # open file
#    metadata = pyexiv2.ImageMetadata(filename)
 #   metadata.read()
    date_time = None
#    for k in template.exif_keys:
#        metadata[k] = pyexiv2.ExifTag(k, template[k].value)
#    if not None:
 #       date_str=pyexiv2.utils.exif(date_time)
 #       metadata['Exif.Image.DateTime'] = date_str
    # GPS info
#    metadata["Exif.Image DateTime"] = date
#    metadata["Exif.GPSInfo.GPSLatitude"] = coordinate2rational(c_lat[0], c_lat[1], c_lat[2])
#    metadata["Exif.GPSInfo.GPSLatitudeRef"] = c_lat[3]
#    metadata["Exif.GPSInfo.GPSLongitude"] = coordinate2rational(c_lng[0], c_lng[1], c_lng[2])
 #   metadata["Exif.GPSInfo.GPSLongitudeRef"] = c_lng[3]

#    metadata.write()

def add_text_to_pic(image_draw, index, text, text_size_x, text_size_y, font):
    text_xy = (0.5*text_size_x, index*text_size_y)
    image_draw.text(text_xy, text, font=font, fill = colors[colorkey])
#    image_draw.text(text_xy, text, font=font, fill = (255, 255, 255, 255))
       
# add line
def add_info_to_pic(filename):
    text = 'try it'
    pos, date, GPS = get_exif_data(filename)
    # open pic
    image = Image.open(filename)
    image_draw = ImageDraw.Draw(image)
    # set font
    imsize = image.size
    fontsize = int(imsize[0]/20)
#    font = ImageFont.truetype('C:/Windows/Fonts/simhei.ttf', fontsize)
#    font = ImageFont.truetype('C:/Windows/Fonts/ahronbd.ttf', fontsize)
    font = ImageFont.truetype('C:/Windows/Fonts/timesbi.ttf', fontsize)
    # text
    text_size_x, text_size_y = image_draw.textsize(text, font=font)
    add_text_to_pic(image_draw, 1, pos['lat'], text_size_x, text_size_y, font)
    add_text_to_pic(image_draw, 2, pos['lon'], text_size_x, text_size_y, font)
    add_text_to_pic(image_draw, 3, pos['h'], text_size_x, text_size_y, font)
    add_text_to_pic(image_draw, 4, date, text_size_x, text_size_y, font)
    # save pic
    new_file = filename[0:-4]+'_bak'+'.jpg'
    image.save(new_file, 'jpeg')
    # add exif info
    add_exif_data(filename, date, pos)

def all_path(dirname, key):
    # all file
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename) # combine the path
 #           if ext in key:
            if key in apath:
                result.append(apath)
    return result  
    
#=============================================================================
#
#=============================================================================

if __name__ == '__main__':
    with open('./color.txt', 'r') as f:
        lines = f.readlines()  
        first_line = lines[0][0:-1]
        first_line = first_line.replace(' ', '')
    try:
        colorkey = colors[first_line]
        colorkey = first_line
    except:
        colorkey = 'white'
    
    # delete
    results = all_path('./', "bak.jpg")
    for ifile in results:
        os.remove(ifile)
    # add info
    results = all_path('./', ".jpg")
    for ifile in results:
        print(ifile)
        add_info_to_pic(ifile)
        break
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    