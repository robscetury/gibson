#!/bin/bash
curl http://peak.telecommunity.com/dist/ez_setup.py > ez_setup.py
ppython ez_setup.py
easy_install simplejson
easy_install httplib2
easy_install simplegeo
easy_install python-twitter