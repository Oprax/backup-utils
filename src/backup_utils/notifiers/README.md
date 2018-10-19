# List of drivers for Notifier task

### Print

Driver name: `print`
Automatically output errors to `stderr`.

### Email

Driver name : `email`
List of all options :
you can use hostname and date as a variable.
 - `subject`: Email subject, i.e: `Panic at {hostname}`
 - `from`: for example `backup@ng.example.org` 
 - `to`: your email adress
 - `host`: SMTP server address
 - `port`: SMTP port, `587` by default.
 - `login`: User login for SMTP
 - `pswd`: Password for SMTP
 