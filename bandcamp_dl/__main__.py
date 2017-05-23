"""bandcamp-dl

Usage:
    bandcamp-dl [options] [URL]

Arguments:
    URL         Bandcamp album/track URL

Options:
    -h --help               Show this screen.
    -v --version            Show version.
    --artist=<artist>       The artist's slug (from the URL)
    --track=<track>         The track's slug (from the URL)
    --album=<album>         The album's slug (from the URL)
    --template=<template>   Output filename template.
                            [default: %{artist}/%{album}/%{track} - %{title}]
    --base-dir=<dir>        Base location of which all files are downloaded.
    -f --full-album         Download only if all tracks are available.
    -o --overwrite          Overwrite tracks that already exist. Default is False.
    -n --no-art             Skip grabbing album art
    -e --embed-lyrics       Embed track lyrics (If available)
    -g --group              Use album/track Label as iTunes grouping
    -r --embed-art          Embed album art (If available)
    -y --no-slugify         Disable slugification of track, album, and artist names.
"""
"""
Coded by:

Iheanyi Ekechukwu
    http://twitter.com/kwuchu
    http://github.com/iheanyi

Simon W. Jackson
    http://miniarray.com
    http://twitter.com/miniarray
    http://github.com/miniarray

Anthony Forsberg:
    http://evolution0.github.io
    http://github.com/evolution0

Iheanyi:
    Feel free to use this in any way you wish. I made this just for fun.
    Shout out to darkf for writing the previous helper function for parsing the JavaScript!
"""

import os
import ast

from docopt import docopt

from bandcamp_dl.bandcamp import Bandcamp
from bandcamp_dl.bandcampdownloader import BandcampDownloader
from bandcamp_dl.__init__ import __version__


def main():
    arguments = docopt(__doc__, version='bandcamp-dl {}'.format(__version__))

    bandcamp = Bandcamp()

    basedir = arguments['--base-dir'] or os.getcwd()
    session_file = "{}/{}.not.finished".format(basedir, __version__)

    if os.path.isfile(session_file):
        with open(session_file, "r") as f:
            arguments = ast.literal_eval(f.readline())
    elif arguments['URL'] is None and arguments['--artist'] is None:
        print(__doc__)
    else:
        with open(session_file, "w") as f:
            f.write("".join(str(arguments).split('\n')))

    if arguments['--artist'] and arguments['--album']:
        url = Bandcamp.generate_album_url(arguments['--artist'], arguments['--album'], "album")
    elif arguments['--artist'] and arguments['--track']:
        url = Bandcamp.generate_album_url(arguments['--artist'], arguments['--track'], "track")
    else:
        url = arguments['URL']

    if arguments['--no-art']:
        album = bandcamp.parse(url, False)
    else:
        album = bandcamp.parse(url)

    if arguments['--full-album'] and not album['full']:
        print("Full album not available. Skipping...")
    elif arguments['URL']:
        bandcamp_downloader = BandcampDownloader(arguments['--template'], basedir, arguments['--overwrite'],
                                                 arguments['--embed-lyrics'], arguments['--group'],
                                                 arguments['--embed-art'], arguments['--no-slugify'], url)
        bandcamp_downloader.start(album)

if __name__ == '__main__':
    main()