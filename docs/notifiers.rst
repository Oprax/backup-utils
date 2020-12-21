==============================
 List of drivers for Notifier
==============================

.. note::
    You can specify a configuration list to send the notification through multiple notifiers.

Print
=====

Driver name: ``print`` Automatically output errors to ``stderr``.

Email
=====

Driver name : ``email`` List of all options : you can use hostname and
date as a variable.

-  ``subject``: Email subject, i.e: ``Panic at {hostname}``
-  ``from``: for example ``backup@ng.example.org``
-  ``to``: your email adress
-  ``host``: SMTP server address
-  ``port``: SMTP port, ``587`` by default.
-  ``login``: User login for SMTP
-  ``pswd``: Password for SMTP


Vonage SMS
==========

Driver name : ``vonage``

Use `Vonage <https://www.vonage.com/communications-apis/sms/>`_ API to send an SMS.

.. warning::
    Attachments cannot be sent by SMS.
    You can combine multiple notifiers with e.g. SMS and email.
    This way you will be notified by SMS and find the logs in the email.

List of all options :

-  ``from``: name of the send, default is ``BackupUtils``
-  ``to``: phone number of the recipient, use E.164 format without leading +.
-  ``vonage_key``: Vonage API key
-  ``vonage_secret``: Vonage API secret key
