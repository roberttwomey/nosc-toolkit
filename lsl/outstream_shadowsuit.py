#
# outstream_shadow.py
#
# streams a single shadow suit to LSL
# to do: update for multiple shadow suits
#
# Robert Twomey | Clarke Center UCSD | November 2018

import sys
from MotionSDK import *
from pylsl import StreamInfo, StreamOutlet

PortConfigurable = 32076
doPrint = False

def shadow_client(host, port, lsl_outlet):

    client = Client(host, port)

    print("Connected to %s:%d" % (host, port))

    if PortConfigurable == port:
        # xml_string = \
        #     "<?xml version=\"1.0\"?>" \
        #     "<configurable>" \
        #     "<preview><Gq/></preview><sensor><a/></sensor>" \
        #     "</configurable>"

        # this data string is copied from the ShadowStream.cs Unity example, 
        # it is what is used for their rigged skeleton in Unity.
        xml_string = \
            "<?xml version=\"1.0\"?>" \
            "<configurable inactive=\"1\">" \
            "<Lq/> <!-- Local quaternion. -->" \
            "<c/> <!-- Position contraint with unit weight. Shadow plugin only. -->" \
            "</cofnigurable>"

        if client.writeData(xml_string):
            print("Sent active channel definition to Configurable service")


    if client.waitForData():
        while True:
            data = client.readData()
            if None == data:
                continue

            new_sample = []

            container = Format.Configurable(data)
            for key in container:
                line = "data({}) = (".format(key)
                for i in range(container[key].size()):
                    element = container[key].value(i)
                    new_sample.append(element)
                    if i > 0:
                        line += ", "
                    line += "{}".format(element)
                line += ")"
                if doPrint:
                    print(line)

            lsl_outlet.push_sample(new_sample)                    


def main(argv):
    # Set the default host name parameter. The SDK is socket based so any
    # networked Motion Service is available.
    host = ""
    if len(argv) > 1:
        host = argv[1]


    # Setup outlet stream infos
    mocap_channels = 32
    sample_size = 8

    stream_info_mocap = StreamInfo('ShadowSuit', 'MOCAP', mocap_channels * sample_size, 200)
    # channels = stream_info_mocap.desc().append_child("channels")
    # channels.append_child('rr')

    # Create outlets
    outlet_mocap = StreamOutlet(stream_info_mocap)

    print("Outlets created")

    shadow_client(host, PortConfigurable, outlet_mocap)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
