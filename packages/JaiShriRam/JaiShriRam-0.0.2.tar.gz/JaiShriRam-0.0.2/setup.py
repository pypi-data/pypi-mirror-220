from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'This is the compressible version of various libraries of python '
LONG_DESCRIPTION = 'This is the compressible version of various libraries of python '

# Setting up
setup(
    name="JaiShriRam",
    version=VERSION,
    author="Krishna",
    author_email="Krishnavijaywargiya12@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    #install_requires=['turtle','mediapipe','autopy','torch', 'tkinter', 'pyautogui', 'time', 'speech_recognition', 'pyttsx3'],
    keywords=['sum', 'minus', 'product', 'division', 'factorial', 'stone_paper_scissors','random_number_generater', 'random_number_picker','circle','square', 'rectangle', 'root_for_quadratic_equation','quadratic_equation_formation', 'name_of_colour_of_word_game', 'halloween_wish_and_pumpkin_creation', 'text_to_speech', 'get_system_name_and_ip_address', 'eye_track_and_mouse_control_with_eye', 'stopwatch', 'forest_adventure_game', 'zero_cutties_game', 'tic_tac_tor_in_tkinter',''],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
