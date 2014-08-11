#/usr/bin/env python

import os, signal, logging, sys

from twisted.internet import reactor
from twisted.python.log import addObserver

logging.basicConfig(format="%(asctime)-15s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# see boostrap.py for how dispersy joins the network,
# on first run it joins these trackers

# _DEFAULT_ADDRESSES = (
#     # DNS entries on tribler.org
#     (u"dispersy1.tribler.org", 6421),
#     (u"130.161.211.245"      , 6421),
#     (u"dispersy2.tribler.org", 6422),
#     (u"130.161.211.245"      , 6422),
#     (u"dispersy3.tribler.org", 6423),
#     (u"95.211.198.141"       , 6423),
#     (u"dispersy4.tribler.org", 6424),
#     (u"95.211.198.143"       , 6424),

#     # DNS entries on st.tudelft.nl
#     (u"dispersy1.st.tudelft.nl", 6421),
#     (u"dispersy2.st.tudelft.nl", 6422),
#     (u"dispersy3.st.tudelft.nl", 6423),
#     (u"dispersy4.st.tudelft.nl", 6424),
# )

from dispersy.dispersy import Dispersy
from dispersy.endpoint import StandaloneEndpoint
from example.community import ExampleCommunity


class DispersyExample(Dispersy):
    "Initialize and Setup Communication Network"

    def signal_handler(self, sig, frame):
        "Gracefully shuts down system, i hope ;)"

        print '' # empty line to make info logging cleaner
        key = ''
        for i in signal.__dict__.keys():
            if i.startswith("SIG") and getattr(signal, i) == sig:
                key = i
                break
        logger.info("Received signal '%s', shutting down.", key)
        self.stop()
        reactor.stop()

    def bind_signals(self):
        "Binds to terminating signals"
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)

    def setup_communities(self):
        "Define a Master Member for unique instance of the ExampleCommunity"

        # Master Key is a crypto keypair member, members use the public key to identify an instance of a community
        # This key was created using the createkey.py tool found in dispersy
        master_key = "3081a7301006072a8648ce3d020106052b810400270381920004076bb2b34a80bc0ff658016c4ee964efd3006c66cbe1f8b4cb75b531e6d9cbc62531156007855cd2ad4985d1f1f9336fd0a2dc0b76ce35351115f20a6637aa76b0bf090ea47df88d029a844f26d0d689463cff7052f0d3b3288113a025164394e8eaed37fb2e9d8afd2275e0fb0ad7c503d9595eb3c1a8c6c8c2f4c5ee6044f2834854a753c8b0317c8a8c37bd2c6d08".decode("HEX")
        master = self.get_member(public_key=master_key)

        # Create Instance of the Community, using our master key and our personal key
        # in this case we pass our message to it but this is not necessary, only for this example.
        self.example_community = ExampleCommunity.init_community(self, master, self.me, self.msg)

        # Attach the Community to Dispersy
        self.attach_community(self.example_community)

    def init(self):
        '''Twisted Reactor is now running, we will now;
        - Start Dispersy
        - Create a Member keypair for ourselves
        - and join Communities'''

        # Automatically Join the Dispersy Discovery Community
        self.start(autoload_discovery=True) 
        logger.info('Dispersy started')

        # Create a new crypto keypair member
        self.me = self.get_new_member() 

        self.setup_communities()


    def __init__(self, port, data_dir, msg):
        "Startup Dispersy, Bind to Termination Signals and start Twisted reactor"

        # super(DispersyExample, self).(self, StandaloneEndpoint(12345, '0.0.0.0'), u'../data', u'dispersy.db')
        super(DispersyExample, self).__init__(StandaloneEndpoint(port, '0.0.0.0'), unicode(data_dir), u'dispersy.db')
        self.statistics.enable_debug_statistics(True)

        self.msg = msg

        self.bind_signals()

        from dispersy.util import unhandled_error_observer
        addObserver(unhandled_error_observer)

        logger.info('Starting Twisted Reactor')
        reactor.exitCode = 0
        reactor.callWhenRunning(self.init)
        reactor.run()


if __name__ == "__main__":
    # Port, Data directory, and message(string) to inject into the community
    DispersyExample(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    exit(reactor.exitCode)