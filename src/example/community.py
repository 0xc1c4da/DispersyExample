import logging

from .conversion import Conversion
from .payload import TextPayload

from dispersy.authentication import MemberAuthentication
from dispersy.community import Community
from dispersy.conversion import DefaultConversion
from dispersy.destination import CommunityDestination
from dispersy.distribution import FullSyncDistribution
from dispersy.message import BatchConfiguration, Message, DelayMessageByProof
from dispersy.resolution import PublicResolution

# from twisted.internet.task import LoopingCall


class ExampleCommunity(Community):

    # @property
    # def dispersy_auto_download_master_member(self):
    #     # there is no dispersy-identity for the master member, so don't try to download (???)
    #     return False

    def initialize(self, msg='hmmmMm'):
        "Called After init_community is called"

        super(ExampleCommunity, self).initialize()
        logging.info("ExampleCommunity Initalized")

        self.send_text(msg)

        # self.register_task("send_text",
        #                    LoopingCall(self.create_channelcast)).start(CHANNELCAST_FIRST_MESSAGE, now=True)

    def initiate_meta_messages(self):
        '''
        Create the packaging for your message payloads,
        in this case we have one message type that is distributed to all peers
        '''

        return super(ExampleCommunity, self).initiate_meta_messages() + [
            Message(self, u"text",
                    MemberAuthentication(encoding="sha1"),
                    PublicResolution(),
                    FullSyncDistribution(enable_sequence_number=False, synchronization_direction=u"ASC", priority=128),
                    CommunityDestination(node_count=10),
                    TextPayload(),
                    self.check_text,
                    self.on_text,
                    batch=BatchConfiguration(max_window=5.0))
        ]

    def initiate_conversions(self):
        return [DefaultConversion(self), Conversion(self)]

    def send_text(self, text='testing'):
        '''
        Inject a message into the community by;
        - Creating an implementation of a meta message
        - Telling dispersy to store the message, update and forward the message
        '''

        meta = self.get_meta_message(u"text")
        message = meta.impl(authentication=(self.my_member,),
                          distribution=(self.claim_global_time(),),
                          payload=(unicode(text),))
        self.dispersy.store_update_forward([message], True, True, True)
        logging.info('send_text sent %s ' % (text))

    def check_text(self, messages):
        "Authentication of our Meta Message happens here, in this case every message is authorized"

        for message in messages:
            yield message
            # allowed, _ = self._timeline.check(message)
            # if allowed:
                # yield message
            # else:
            #     yield DelayMessageByProof(message)

    def on_text(self, messages):
        "Called after check_text, we can now display our message to the user"

        for message in messages:
            print 'someone says', message.payload.text
            logging.info("someone says '%s'", message.payload.text)
