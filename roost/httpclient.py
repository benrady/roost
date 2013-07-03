from zope.interface import implements
from twisted.web import client
from twisted.internet import reactor
from twisted.internet import defer 
from twisted.internet.defer import succeed
from twisted.web.iweb import IBodyProducer

import json

class StringProducer(object):
  implements(IBodyProducer)

  def __init__(self, body):
    self.body = body
    self.length = len(body)

  def startProducing(self, consumer):
    consumer.write(self.body)
    return succeed(None)

  def pauseProducing(self):
    pass

  def stopProducing(self):
    pass

def post(url, body):
  agent = client.Agent(reactor)
  return agent.request('POST', url, bodyProducer=StringProducer(body))
