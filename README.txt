NOTE:
- LINUX DISTRO UBUNTU WAS USED IN THE ENTIRE PROCESS
- this uses pdftotext which requires poppler package
- inorder to install pdftotext package use the following commands:
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python-dev
conda install libgcc
pip install pdftotext

- the python script is named as DataExtractionAndTranslation_pradeep4444.py
- At line 98 change the input_file_location to test folder containing
test pdfs
- function arabic_to_english is the main function which calls other
helper functions
- few temporary folders are created to hold the intermediary pdf and text files, which is deleted at the end
- the final converted english text files are stored in english_converted_files directory.
- this script uses google translate to translate and hence requires active internet connection
- Since i dont have a credit card i was forced to use the google translate python package which bypasses the google API layer authentication and hence the google transtale part (google_trans function) is written as a seperate function to modify it easily
- Create the required environment using the provided environment.yml file or 
requirements.txt file; it is preferable to use yml file since some packages are
installed using conda and some using pip
