TimeVortex (2.1.2) stable; urgency=low

* Add snap folder into TV v2 project
* Add snap folder into TV v2 project
* Load initial data without erasing user modification
* Fix energy model problem
* Pass log error if no currentcost settings to 60 seconds, Log into system site_id
* Migrate command parameter of currentcost to DB settings
* Fix lint problem
* Fix migration problem
* Improve daily_report to read settings from DB, send report every day at 4:00 AM
* Migrate abstract command to infinite loop and update job to run new abstract command architecture
* Fix lint problem
* Move Settings weather value DateField to Charfield
* Move BACKUP_TARGET_FOLDER in DB + add initial_data + fix funtional test for backup command
* Move SETTINGS_METEAR_START_DATE in DB + add initial_data + fix funtional test + fix bad url problem in metear command
* Remove useless log from timevortex model, Add todo for backup and metear command
* Move METEAR command to infinite loop
* Try to export static files
* Try to export static files
* Try to export static files
* Add initial_data and test to start server on deployment
* Add initial_data and test to start server on deployment
* Add energy and weather command
* Fix lint problemp
* Try to export energy folder
* Try to export energy folder
* Remove stubs app form production, only launch stubs url in testing mode
* Remove stubs app form production, only launch stubs url in testing mode
* Reimport stubs in base.py
* Change DB settings to try to migrate
* Fix lint problem
* Fix base.py and local.py settings to add unit test only on local and not in production
* Add dependency dev in setup.py for test
* Add djnago_nose for test
* Exclude stubs package
* Exclude stubs package
* Modify production settings to target snap common path
* Modify production settings to target snap common path
* Modify python file to use python3
* Start release v2.1.2

Pierre Leray <pierreleray64@gmail.com>  2016-09-20 12:52:29

TimeVortex (2.1.1) stable; urgency=low

* Finish release v2.1.1 on 2016-09-20 12:51:40
* Modify setup.py to export manage.py
* Start release v2.1.1

Pierre Leray <pierreleray64@gmail.com>  2016-09-15 11:38:49

TimeVortex (2.1.0) stable; urgency=low

* Finish release v2.1.0 on 2016-09-15 11:38:49
* Add setup.py
* Start release v2.1.0

Pierre Leray <pierreleray64@gmail.com>  2016-09-09 13:28:56

TimeVortex (2.0.1) stable; urgency=low

* Finish release v2.0.1 on 2016-09-09 13:28:56
* Fix pep8 error
* Fix pep8 error
* Fix behave error
* Fix pylint error
* Modify travis.yml to create folder
* Add local.py for testing, modify gitignore
* Fix Django version in requirements
* Modifiy requirements to pass travis test, update test to fix path problem
* Fix requirements in travis.yml
* Fix requirements in travis.yml
* Fix lint, test and directory on local branch
* Add Snap creation command on readme, update travis.yml to read settigns from local
* Start release v2.0.1

Pierre Leray <pierreleray64@gmail.com>  2016-07-18 00:36:18

TimeVortex (2.0.0) stable; urgency=low

* Finish release v2.0.0 on 2016-07-18 00:36:18
* Migrate TimeVortex application to Django
* Create timevortex app for utils and timeserieslogger
* Create energy app for currentcost command
* Create weather app for METEAR command
* Migrate pavement utils to timevortex command

Pierre Leray <pierreleray64@gmail.com>  2016-07-17 23:18:43


