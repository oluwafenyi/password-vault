## password-vault - pv.py
A script that manages and generates passwords from the command line, passwords are stored in a sqlite db.
***
#### How to Install
`pip install pvault==1.0.9a0`

#### Basic Usage

Generate random password for an account:  
    `pv generate [accountname]`

Generate random password:  
    `pv generate`

Access stored account password:  
    `pv account [accountname]`

Get list of all stored account passwords:  
    `pv accounts`

Save password manually:  
    `pv save [accountname]`

Update password by random generation:  
    `pv generate [accountname]`

Update password by manual entry:  
    `pv save [accountname]`

Delete account password:  
    `pv delete [accountname]`

Delete all accounts:  
    `pv delete`

