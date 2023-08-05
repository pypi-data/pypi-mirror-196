#######################################################
#
# ClientReceptionHandler.py
# Python implementation of the Class ClientReceptionHandler
# Generated by Enterprise Architect
# Created on:      19-May-2020 7:17:21 PM
# Original author: Natha Paquette
#
#######################################################
import time
import socket
import errno
import copy
import re

from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from defusedxml import ElementTree as etree

# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

loggingConstants = LoggingConstants(log_name="FTS_ClientReceptionHandler")
logger = CreateLoggerController("FTS_ClientReceptionHandler", logging_constants=loggingConstants).getLogger()
from FreeTAKServer.core.configuration.ClientReceptionLoggingConstants import ClientReceptionLoggingConstants

loggingConstants = ClientReceptionLoggingConstants()
BUFF_SIZE = config.DataReceptionBuffer

class ClientReceptionHandler:
    def __init__(self):
        self.dataPipe = []
        self.socketCount = 0

    def startup(self, clientInformationArray):
        try:
            self.clientInformationArray = clientInformationArray  # create copy of client information array so it cant be changed during iteration
            '''logger.propagate = False
            logger.info(loggingConstants.CLIENTRECEPTIONHANDLERSTART)
            logger.propagate = True'''
            output = self.monitorForData(self.dataPipe)
            if output == 1:
                return self.dataPipe
            else:
                return -1
            '''
            time.sleep(600)
            # temporarily remove due to being unnecessary and excessively flooding logs
            logger.info('the number of threads is ' + str(threading.active_count()) + ' monitor event process alive is ' + str(monitorEventProcess.is_alive()) +
                        ' return data to Orchestrator process alive is ' + str(monitorForData.is_alive()))
            '''
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERSTARTUPERROR + str(e))

    def monitorForData(self, queue):
        '''
        updated receive all
        '''
        try:
            keys = copy.deepcopy(list(self.clientInformationArray.keys()))  # this prevents changes to the clientInformationArray from having any severe effects on this method
            for user_id in keys:
                sock = self.clientInformationArray[user_id][0]
                client = user_id
                #client = self.clientInformationArray[user_id][1]
                try:
                    sock.settimeout(0.001)
                    try:
                        xmlstring = self.recv_until(sock).decode()
                        if xmlstring == b'' or xmlstring == '' or xmlstring is None: 
                            self.returnReceivedData(client, b'', queue)
                            logger.debug("empty string sent, standard disconnect")
                            continue
                        xmlstring = "<multiEvent>" + xmlstring + "</multiEvent>"  # convert to xmlstring wrapped by multiEvent tags
                        xmlstring = re.sub(r'(?s)\<\?xml(.*)\?\>', '', xmlstring)  # replace xml definition tag with empty string as it breaks serilization
                        events = etree.fromstring(xmlstring)  # serialize to object
                        for event in events.findall('event'):
                            self.returnReceivedData(client, etree.tostring(event), queue)  # send each instance of event to the core
                    except socket.timeout as e:
                        continue
                    except BrokenPipeError as e:
                        self.returnReceivedData(client, b'', queue)
                        continue
                    except Exception as e:
                        import traceback
                        if hasattr(e, "errno") and e.errno == errno.EWOULDBLOCK:  # this prevents errno 11 from spontanieously disconnecting clients due to the socket blocking set to 0
                            logger.debug("EWOULDBLOCK error passed " + str(e))
                            continue
                        logger.error(
                            "Exception other than broken pipe in monitor for data function " + str(e) + ''.join(traceback.format_exception(None, e, e.__traceback__)))
                        self.returnReceivedData(client, b'', queue)
                        continue

                except Exception as e:
                    logger.error(loggingConstants.CLIENTRECEPTIONHANDLERMONITORFORDATAERRORD + str(e))
                    self.returnReceivedData(client, b'', queue)
                    # return -1 commented out so entire run isn't stopped because of one disconnect
            return 1
        except Exception as e:
            logger.error('exception in monitor for data ' + str(e))
            return -1

    def returnReceivedData(self, clientInformation, data, queue):
        try:
            from FreeTAKServer.model.RawCoT import RawCoT
            RawCoT = RawCoT()
            RawCoT.clientInformation = clientInformation
            RawCoT.xmlString = data.replace(b'\n', b'')  # replace all newlines with empty
            self.dataPipe.append(RawCoT)
            logger.debug("data received "+ str(data))
            return 1
        except Exception as e:
            logger.error(loggingConstants.CLIENTRECEPTIONHANDLERRETURNRECEIVEDDATAERROR + str(e))
            return -1

    def recv_until(self, client):
        start_receive_time = time.time()
        message = client.recv(BUFF_SIZE)
        while time.time() - start_receive_time <= config.MaxReceptionTime:
            try:
                message = message + client.recv(BUFF_SIZE)
            except Exception as e:
                break
        return message