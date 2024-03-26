
# Welcome to TTVG (tiktok video generator)

Generate r/amitheasshole, r/TIFU, and r/relationship advice subwaysurfer/minecraft/genshinimpact reddit storytime posts with just the click of a button. 
## How to install:
Use a conda environment: Python 3.10 and 3.11 work, other versions not tested.

Conda preferred because of the installation of MFA (Montreal Forced Aligner). This is the hardest part of the whole installation.

Once in your conda environment, run in your terminal: 

```
conda config --add channels conda-forge
conda install montreal-forced-aligner
```
Run `mfa` in your environment to see if it is installed. If that doesn't work consult [here](https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html) because idk how to fix it lol.

Once installed, run
```
mfa model download dictionary english_us_arpa 
mfa model download acoustic english_us_arpa
```
You are now finished with MFA installtion.

Next, run `pip install pillow==9.5.0` in your terminal to install that specific version of pillow.

Once those two are installed, you should be able to just run `python3 main.py` and install the missing packages until the code works. 

## Downloading the background videos/images and sample audio files

Download [here](https://cmu.box.com/s/ylgguvmk2a5u81ygndsvn9tvhfve602m).

## Using your reddit API information
```pip install python-dotenv``` if you don't have the package already. 
The reddit API requires you to use your reddit account username, password, client ID, and client secret. Our code reads them from a local file so we don't leak the information.
Create a file named ".env" in the TTVG directory. In the file, put:

```
REDDIT_USERNAME=<your_username>
REDDIT_PASSWORD=<your_password>
CLIENT_ID=<your_ID>
CLIENT_SECRET=<your_secret>
```
Replace <your_username> and <your_password> etc. with your username and password etc. without quotes. 

## How do I get the reddit API Info?

Follow [these instructions](https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/).

## How do I get a tiktok session_id?

Follow [these instructions](https://github.com/Steve0929/tiktok-tts?tab=readme-ov-file#get-tiktok-session-id-).


## Authors

by jason, kaiya, mark, bryan

