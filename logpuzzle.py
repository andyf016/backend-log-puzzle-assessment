#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = """Andrew Fillenwarth. Thanks to Janelle Kuhns for
                helping me with the correct URL and thanks as
                always to Daniel for the Study Halls and everything else!"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    first_part = 'http://code.google.com/'
    puzzle_urls = []
    with open(filename) as logs:
        pattern = re.compile(r'edu\S+.jpg')
        sort_pattern = re.compile(r'edu\S+(\w{4}).jpg')
        line_list = logs.readlines()
        for line in line_list:
            match = pattern.findall(line)
            # print(match)
            if match:
                final = ''.join(match)
                puzzle_urls.append(first_part + final)
        puzzle_urls = list(set(puzzle_urls))
        # sort list based on specified group
        sorted_urls = sorted(
            puzzle_urls, key=lambda x: sort_pattern.search(x).group(1))
    return sorted_urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    template_start = "<html><body>"
    template_end = "</body></html>"
    # create dest_dir if it does not exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    os.chdir(dest_dir)
    # set counter for image names
    count = 0
    # create index.html and open it for writing
    with open('index.html', 'w') as f:
        f.write(template_start)
        # download the image from each url in the list
        for url in img_urls:
            img_name = f'img{count}.jpg'
            urllib.request.urlretrieve(url, img_name)
            count += 1
            f.write(f'<img src="{os.path.abspath(img_name)}">')
        f.write(template_end)
    return


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


# download_images(read_urls('place_code.google.com'), 'imgdir')


if __name__ == '__main__':
    main(sys.argv[1:])
