#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of Flower.
#
# Copyright ©2018 Nicolò Mazzucato
# Copyright ©2018 Antonio Groza
# Copyright ©2018 Brunello Simone
# Copyright ©2018 Alessio Marotta
# DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
# 
# Flower is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Flower is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flower.  If not, see <https://www.gnu.org/licenses/>.

#Script that import pcap into flower dg
import json
import pyshark
import sys
import string
from datetime import datetime

from configurations import containsFlag
from db import DB

# Get filename
def main():
    filename = ""
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if "./" in filename:
            filename = filename[2:]
        print("Importing file %s." % filename)
    else:
        print("pcap file required!")
        exit(1)
    
    db = DB()
    # Do nothing if file is already imported
    if db.isFileAlreadyImported(filename):
        print("File %s already imported!" % filename)
        exit()
    
    # Loop over all packets and populate flows_to_import
    packets = pyshark.FileCapture(filename)
    streams = {}
    for pkt in packets:
        # Skip non TCP packets
        if pkt.transport_layer != "TCP":
            continue
    
        # Skip packets without payload 
        if "payload" not in pkt.tcp.field_names:
            continue
    
        # Check if this is the first packet of the stream
        stream_id = pkt.tcp.stream
        if stream_id not in streams:
            init_stream = {"inx": stream_id, #TODO hmm?
                    "filename": filename,
                    "src_ip": pkt.ip.src,
                    "src_port": int(pkt.tcp.srcport),
                    "dst_ip": pkt.ip.dst,
                    "dst_port": int(pkt.tcp.dstport),
                    "time": round(datetime.timestamp(pkt.sniff_time)*1000),
                    "duration": -1,
                    "contains_flag": False,
                    "starred": 0,
                    "flow": []
                    }
            streams[stream_id] = init_stream
    
        # Update the stream
        stream = streams[stream_id]
        # Update the duration 
        stream["duration"] = round(float(pkt.tcp.time_relative) * 1000);
        
        # Parse the payload
        raw_data = pkt.tcp.payload.split(":")
        printable_data = ''.join([chr(int(i, 16)) if chr(int(i, 16)) in string.printable else "x%s" % i for i in raw_data])
    
        # Check if flag is contained
        if not stream["contains_flag"] and containsFlag(printable_data):
                stream["contains_flag"] = True
    
        # Name of sender "c" == client, "s" == server
        name = "s" if stream["src_ip"] == pkt.ip.src and stream["src_port"] == int(pkt.tcp.srcport) else "c"
    
        # Create new entry if flow is empty or previous sender does not match current sender.
        # Otherwise concatenate it.
        flow = stream["flow"]
        if not flow or flow[-1]["from"] != name:
            flow_data = {"from": name,
                         "data": printable_data,
                         "hex": "".join(raw_data), 
                         "time": round(datetime.timestamp(pkt.sniff_time)*1000)
                        }
            flow.append(flow_data)
        else:
            flow[-1]["data"] += printable_data
            flow[-1]["hex"] += "".join(raw_data)
            
    # Insert into DB
    db.insertFlows(filename, list(streams.values()))
    db.setFileImported(filename)
    print("Imported %s successfully." % filename)

if __name__ == "__main__":
    main()
