#NOTE: you must create oauth_tokens your self... It must include the constants
#shown below
from oauth_tokens import *
import twitter
import time 
import re
import send_event
import traceback

REAL_TIME_PAUSE = True
REAL_TIME_SCALEFACTOR = 10 # time moves faster if this < 1

def findMentions(tweet):
    iter =  re.finditer(r'(\A|\s)@(\w+)', tweet)
    return iter
class TwitterReader():

    def __init__(self, ip, port):
        self._port  = port
        self._ip = ip
    def format(self, u):
        if self.since_id==None or u.GetId() > self.since_id:
            self.since_id = u.GetId()
        timesent = u.GetCreatedAtInSeconds()
        if u.text.find("@") > 0:
            type = "Mention"
            mentions = list()
            for m in findMentions(u.text):
                mentions.append(m.group(0))
                
            mentions = ",".join(mentions)
        else:
            type = "Status"
            mentions = ""
            
        
        return "|".join([str(timesent), type, "ALARM", u.user.screen_name, "N/A", mentions, "N/A", u.text])

    def run(self):
        a = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, USER_ACCESS_TOKEN,
        ACCESS_TOKEN_SECRET)
        self.since_id = None
        socket = send_event.EncapsulateForPanda()
        while 1:
            try:
                statuses = a.GetFriendsTimeline(since_id=self.since_id)
                startTime = statuses[-1].GetCreatedAtInSeconds()
                totalWait = 0
                for status in range(len(statuses)-1, 0, -1):
                    status = statuses[status]
                    message = self.format(status)
                    socket.send_event(self._ip, self._port, message.encode("ascii", 'replace'))
                    print message
                    #print status.GetCreatedAtInSeconds() - startTime
                    if REAL_TIME_PAUSE:
                        print "Wating %i seconds"%((status.GetCreatedAtInSeconds() - startTime)/REAL_TIME_SCALEFACTOR)
                        time.sleep( (status.GetCreatedAtInSeconds() - startTime)/REAL_TIME_SCALEFACTOR)
                        totalWait += ((status.GetCreatedAtInSeconds() - startTime)/REAL_TIME_SCALEFACTOR)
                    startTime = status.GetCreatedAtInSeconds()
            except:
                traceback.print_exc()
                pass # most likely a connection error...so lets try again later...
            print "sleeping..."
            if totalWait < 60:
                time.sleep(60 - totalWait)
if __name__=="__main__":
    reader = TwitterReader()
    reader.run()


        
