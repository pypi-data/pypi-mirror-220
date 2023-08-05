# slides-sound
A set of tools for generating slide shows from images with improvised sound tracks.

This is a project that I've been working on off and on, I'd like to eventually turn it into a web service to allow folks to upload or point to images and then generate the slideshows. The image processing and the music generation is very simplistic and definitely a work in progress.

Installation
==================================================================================

You can install it from pypi by doing:
    
    python3 -m pip install slides-sound

The scripts will end up on your ~/.local/bin directory and you should make sure this is on your path.

OR

You can check out the repo from https://gitub.com/jpfxgood/slides-sound to a directory and put the scripts directory on your path and also put the checkout directory on the PYTHONPATH so that it's package can be found.

Or download the zip file from the github release at the path above and unzip it and do the same thing.

You can install the dependencies by doing:

    python3 -m pip install -r requirements.txt

I recommend upgrading pip before you do any of the above by doing:

    python3 -m pip install --upgrade pip


Slides
==================================================================================

Slides is a program which will take a list of image files either specified by wildcard or by an input file list specified by --file option and create a slideshow as a mp4 video file. If used with the music script the file can also have an improvised sound track based on a chord progression. The script automatically rotates and resizes the images to make them consistent.

    Usage: slides [options] [path with wildcard to the images]

    A tool to create slide show videos from a set of photos

    Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  Read image file paths from a file one full path per
                            line
      -m MUSIC, --music=MUSIC
                            Read music chords from file
      -v, --verbose         Log all activity to console
      -x WIDTH, --width=WIDTH
                            Width of slide show (default 320)
      -y HEIGHT, --height=HEIGHT
                            Height of slide show (default 240)
      -r RATE, --rate=RATE  Frame rate in frames per second (default 1)
      -b BPM, --bpm=BPM     Beats per minute for tempo
      -s, --swing           Swing the notes in the improvisation
      -S SAMPLES, --samples=SAMPLES
                            Add path to additional voice with samples
      -F SOUNDFONTS, --soundfont=SOUNDFONTS
                            Add path to additional voice with soundfont
      -p PATH, --path=PATH  Output path for generated slideshow.

Music
=================================================================================

Music is a program that takes a set of music input files and creates an improvisation based on the input files. The general idea is that it tries to choose a technique and a direction for some number of bars and then applies that technique, it uses linear runs and arpegiation so far. It currently has very simplistic accompanyment in the form of simple bass line and punching chords. It needs lots of work and rewriting, but it's starting to form a framework.

    Usage: music [options]

    A tool to create improvised music based on chord progression, and/or melody
    and rhythm

    Options:
      -h, --help            show this help message and exit
      -c CHORDS, --chords=CHORDS
                            Read chord progression from file
      -m MELODY, --melody=MELODY
                            Read melody from file
      -r RHYTHM, --rhythm=RHYTHM
                            Read rhythm from file
      -n CHORUS, --chorus=CHORUS
                            Number of choruses
      -t TIME, --time=TIME  Total seconds to generate music for
      -o OUTPUT, --output=OUTPUT
                            Output file to save music
      -b BPM, --bpm=BPM     Beats per minute for tempo
      -s, --swing           Swing the notes in the improvisation
      -d DELTAS, --deltas=DELTAS
                            Read the stream of delta values to generate melody
                            from file
      -v, --verbose         Log all activity to console
      -D, --debug           save debug versions of the parts
      -S SAMPLES, --samples=SAMPLES
                            Add path to additional voice with samples
      -f SOUNDFONTS, --soundfonts=SOUNDFONTS
                            Add soundfont to use for a voice, format is {bank
                            number}:{preset number}:{full path to soundfont} will
                            default to 0:0:{first soundfont we find}
      -V VOICES, --voices=VOICES
                            Voice numbers
                            {chord_voice},{melody_voice},{rhythm_voice}
      -T TRANSPOSE, --transpose=TRANSPOSE
                            Transpose voices {chord_transpose},{melody_transpose},
                            {rhythm_transpose}

Music input files look like this:

    [
    C("F3Maj",1),C("F3Maj",1),C("F3Maj",1),C("Bb3Maj",1),
    C("Bb3Maj",1),C("Bb3Maj",1),C("Bb3Maj",1),C("Bb3Maj",1),
    C("Bb3Maj",1),C("Bb3Maj",1),C("Bb3Maj",1),C("Bb3Maj",1),
    C("G3Min",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),
    C("A3Maj",1),C("F3Maj",1),C("F3Maj",1),C("F3Maj",1),C("D3Min",1),C("Bb3Maj",1),C("Bb3Maj",1), C("Bb3Maj",1), C("Bb3Maj",1), C("Bb3Maj",1),
    C("G3Min",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),
    C("A3Maj",1),C("F3Maj",1),C("F3Maj",1),C("F3Maj",1),C("D3Min",1),C("Bb3Maj",1),C("Bb3Maj",1), C("Bb3Maj",1), C("Bb3Maj",1), C("Bb3Maj",1),
    C("G3Min",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),
    C("A3Maj",1),C("F3Maj",1),C("F3Maj",1),C("F3Maj",1),C("D3Min",1),C("Bb3Maj",1),C("Bb3Maj",1), C("Bb3Maj",1), C("Bb3Maj",1), C("Bb3Maj",1),
    C("G3Min",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),C("Eb3Maj",1),
    C("A3Maj",1),C("F3Maj",1)
    ]

The syntax is a list initialization in Python, the C class represents a chord  C( name, value ) where name is "{Key}{octave}{Maj|Min|7|Maj7|Min7|Min6|Min7b5|-Maj7|7b9|7#11}", the N class represents a note N( name, value ) where name is "{Key}{octave}. In both cases value is 1 for whole note, 2 for half note, 4 for quarter note, 8 for eighth note.

Here's an example of a melody line encoded in this way, note the *3 at the end this creates 3 copies of the preceding list and thus three choruses:

    [
    N("G#3",4),N("G#3",4),N("E3",4),N("F#3",4),N("R",8),N("G#3",4),N("E3",8),N("G#3",4),N("E3",8),N("E3",8),
    N("E3",1),N("R",2),N("R",4),N("E3",8),N("F#3",8),
    N("G3",4),N("G3",4),N("E3",4),N("F#3",4),N("R",8),N("G3",4),N("E3",8),N("G3",4),N("F#3",4),
    N("E3",1),N("R",2),N("R",4),N("E3",8),N("E3",8),
    N("F#3",4),N("D#2",4),N("B2",8),N("B2",4.5),N("R",8),N("G3",4),N("E3",8),N("G3",4),N("F#3",4),
    N("E3",1),N("R",1)
    ] * 3

There is a new experimental structure called a Section represented by class S( "name", [ list of chords or notes ] ):

    [
    S("A", [ C("D3Maj",2),C("D3Maj",2),C("A3Maj",2),C("B3Min",2),C("G3Maj",2),C("G3Maj",2)]),
    S("B", [ C("A3Maj",2),C("A3Maj",2),C("B3Min",2),C("B3Min",2),C("G3Maj",2),C("G3Maj",2)]),
    S("C", [ C("D3Maj7",2),C("D3Maj7",2),C("A3Maj7",2),C("B3Min7",2),C("G3Maj7",2),C("G3Maj7",2)]),
    S("D", [ C("A3Maj7",2),C("A3Maj7",2),C("B3Min7",2),C("B3Min7",2),C("G3Maj7",2),C("G3Maj7",2)])
    ]

The script will automatically try to generate a structure like "ABBCA" or the like to give the generated composition more structure.

The script will search the /usr/share and subdirectores for soundfonts and use the first one it encounterss to create the samples for the music generation. It uses bank 0 and preset 0. If you use the -f option you can have it use any specific soundfont, bank and preset you want. Each -f option creates a new voice numbered from 0 you can use the -V option to assign them to the different parts of the music generation.

If you are looking for soundfonts there are a number of them available packaged for linux: musecore-general-soundfont, timgm6mb-soundfont, fluid-soundfont-gm, fluid3mono-gm-soundfont are just a few such packages.

Contact Sheet
=================================================================================

Contact sheet is a script that collects a number of images and rotates and pads them and then lays them out in a sequence of contact sheets with a configurable size and number of rows and columns and outputs those contact sheets as .jpg files.

    Usage: contact_sheet [options] [path with wildcard to the images]

    A tool to resize all photos to a common size and rotate and pad any camera
    rotated images and create a series of contact sheets as .jpg files

    Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  Read image file paths from a file one full path per
                            line
      -v, --verbose         Log all activity to console
      -l, --labels          Put labels on images
      -x WIDTH, --width=WIDTH
                            Width of each image (default 320)
      -y HEIGHT, --height=HEIGHT
                            Height of each image (default 240)
      -r ROWS, --rows=ROWS  Rows in contact sheet (default 6)
      -c COLUMNS, --columns=COLUMNS
                            Columns in contact sheet (default 8)
      -p PATH, --path=PATH  Output path for transformed images

Rotate Resize
=================================================================================

Rotate resize is a script that collects a number of images and rotates and pads them and outputs them to the output directory path

    Usage: rotate_resize [options] [path with wildcard to the images]

    A tool to resize all photos to a common size and rotate and pad any camera
    rotated images

    Options:
      -h, --help            show this help message and exit
      -f FILE, --file=FILE  Read image file paths from a file one full path per
                            line
      -v, --verbose         Log all activity to console
      -x WIDTH, --width=WIDTH
                            Width of slide show (default 320)
      -y HEIGHT, --height=HEIGHT
                            Height of slide show (default 240)
      -p PATH, --path=PATH  Output path for transformed images
