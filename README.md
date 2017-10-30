# Security-Dashboard #


[![Test Build Status](https://travis-ci.org/bsab/security-dashboard.svg?branch=master)](https://travis-ci.org/bsab/security-dashboard/builds#)

A dashboard that shows the status of security features on .gov.it websites

Select a domain from the search bar or directly by clicking on the chart. Each domain has been assigned a score from A to F.

The score calculation is based on 3 characteristics:
- Security: guaranteed by the use of HTTPS or HTS protocol.
- Performance: Analyzing the loading times for pages and assets.
- Reliable: Verifing MX, SPF, and DMARC usage.

The domain that gets the highest value in all three of these features can be considered a highly secure domain.

Check out the [Live Demo](https://security-dashboard.herokuapp.com/security-dashboard).

![Alt desc](https://raw.githubusercontent.com/bsab/security-dashboard/master/screenshots/Screenshot_1.png)

Requirements
----
Python 2.7

Usage
----

Check [Live Demo](https://security-dashboard.herokuapp.com/security-dashboard) or open the dashboard in your web browser :

 http://localhost/security-dashboard/


Install on local
-----

If you prefer to run it directly on your local machine, I suggest using
[virtualenv](https://virtualenv.pypa.io/en/stable/) (maybe have a look at
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/stable/)),
anyway here the commands you have to enter:

    git clone https://github.com/bsab/security-dashboard
    cd security-dashboard
    pip install -r requirements.txt

To update the data-set, overwrite the files pageload.csv, pshtt.csv and trustymail.csv inside direcotry data/csv

Running Your Application
------------------------

Now, you can run the application locally.

    python app.py


## Authors

* [Sabatino Severino](https://about.me/the_sab), @bsab

* [Marco Izzo](https://github.com/marcoizzo), @marcoizzo

* [Francesco Amato](https://github.com/airciccio83), @airciccio83


