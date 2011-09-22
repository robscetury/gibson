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
