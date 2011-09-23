#Copyright 2011 Dan Klinedinst
#
#This file is part of Gibson.
#
#Gibson is free software: you can redistribute it and/or modify it
#under the terms of the GNU General Public License as published by the
#Free Software Foundation, either version 3 of the License, or any
#later version.

#Gibson is distributed in the hope that it will be useful, but WITHOUT
#ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#for more details.
#
#You should have received a copy of the GNU General Public License
#along with Gibson.  If not, see <http://www.gnu.org/licenses/>.
import os

def getPath(pathType, extra=""):
    if os.path.exists(extra):
        return extra
    else:
        if pathType=="conf":
            pathType="CONFIGPATH"
        elif pathType=="image":
            pathType="TEXTUREPATH"
        elif pathType=="model":
            pathType="MODELPATH"
        elif pathType=="xml":
            pathType="XMLPATH"
    filename = os.path.join( os.environ.get(pathType), extra)
    if os.path.exists(filename):
        return filename
    else:
        raise Exception("File %s does not exist"%filename)
