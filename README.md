# BIOS Files Verification for Batocera
The aim of this script is to offer a way to verify quickly the md5 sums of bios files uploaded in Batocera.

## How to use it manually ?
### Requirements

- Python 3

### Usage

1. Copy the `bios_verification_batocera.py` script to the BIOS folder in your Batocera installation.
2. Open a terminal in Batocera either locally or by SSH (recommended).
3. Navigate to the BIOS folder using the `cd` command.
4. Execute the script by running the following command:
```
python bios_verification_batocera.py
```


## To Do

- Automate the verification process.
- Add an option to suppress output.
