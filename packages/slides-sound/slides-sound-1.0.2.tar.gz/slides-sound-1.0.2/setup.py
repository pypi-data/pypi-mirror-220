from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("VERSION", "r") as fh:
    version = fh.read().strip()

setup(
    name='slides-sound',
    version=version,
    url='http://github.com/jpfxgood/slides-sound',
    author="James Goodwin",
    author_email="slides-soundc@jlgoodwin.com",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    description='Tools for creating slideshows from images with generated music',
    long_description_content_type='text/markdown',
    long_description=long_description,
    license = 'MIT',
    keywords= [
        'music',
        'slides',
        'images',
    ],
    install_requires=[
        'Pillow',
        'pyfluidsynth',
        'pyaudio',
    ],
    scripts=[
        'scripts/contact_sheet',
        'scripts/list_soundfont',
        'scripts/music',
        'scripts/rotate_resize',
        'scripts/slides',
    ],
    packages=[
        'slides_sound',
    ],
    python_requires='>=3.6',
)
