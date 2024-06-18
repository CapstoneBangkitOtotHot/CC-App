# Bangkit Capstone C241-PS005 Cloud Computing API

## Flow diagram

![CC](https://github.com/CapstoneBangkitOtotHot/CC-App/assets/43638783/0228b504-19b3-4250-801e-1a3f52e0f157)

## Installation

**NOTE**: Before installing you will need to install Python 3.10 with Pip

Clone the repository first 

```
git clone https://github.com/CapstoneBangkitOtotHot/CC-App.git
git pull
git submodule update --init --recursive
git submodule update --remote
```

And then install the dependencies

```sh
pip install -r requirements.txt
```

After that you will require to create `firebase-web-api.key` file, you can [read it here](https://firebase.google.com/docs/projects/api-keys) to get API keys for firebase

And lastly, you need to create file `serviceaccountkey.json`, you can grab it from [here](https://console.cloud.google.com/iam-admin/serviceaccounts)

## Usage

```sh
python run.py
```

