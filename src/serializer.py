import struct

FS_CHAR = 0x1C # Record
GS_CHAR = 0x1D # Field
RS_CHAR = 0x1E # Subfield 
US_CHAR = 0x1F # Item

# position code wrappers
posEncoding =   {
                    '1':b'\x01\x01\x01',
                    '2':b'\x02\x01\x02',
                    '3':b'\x03\x01\x03',
                    '4':b'\x04\x01\x04',
                    '5':b'\x05\x01\x05',
                    '6':b'\x06\x01\x06',
                    '7':b'\x07\x01\x07',
                    '8':b'\x08\x01\x08',
                    '9':b'\x09\x01\x09',
                    '10':b'\x0A\x01\x0A',
                    '11':b'\x0B\x00\x0B',
                    '12':b'\x0C\x00\x0C',
                    '13':b'\x0D\x00\x0D',
                    '14':b'\x0E\x00\x0E'
                }

# fingerprint thing
FINGER_SEPARATOR = b'\xFF\xFF\xFF\xFF\xFF\x00'

# wrapper for NIST file
class NISTFile:
    def __init__(self):
        self.records = []
        self.output = ''
    def add_record(self, record):
        self.records.append(record)
    def clear_records(self):
        self.records.clear()
    def serialize(self):
        data = b""
        for record in self.records:
            data += record.serialize()
        return data

# will hold record data that has user input 
# in the case of fingerprints, type 1 and 2
class Record:
    def __init__(self, recordType, data, positionCode=0, params=[0,0]):
        self.recordType = recordType
        self.data = data
        self.positionCode = positionCode
        self.params = params

    def serialize(self):  # placeholder for header size
        if self.recordType == 4:
            return self.serialize_fingerprint()
        else:
            return self.serialize_other()
        
    def serialize_fingerprint(self):
        recordData = bytearray()
        # add encoded position
        recordData += posEncoding[self.positionCode] + FINGER_SEPARATOR
        # add encoded HLL and VLL by getting width, length
        recordData += bytes.fromhex(format(self.params[0], '04x'))
        recordData += bytes.fromhex(format(self.params[1], '04x'))
        # mark as encoded using WSQ-20
        recordData += b'\x01'
        # temporary record data
        recordData += self.data
        # get record header
        tempHeader = f"{len(recordData)}".encode() 
        totalLength = format((len(tempHeader) + len(recordData) - 1), '08x')
        finalData = bytearray()
        finalData += bytes.fromhex(totalLength) + recordData
        return finalData
    
    def serialize_other(self):
        recordData = bytearray()
        if self.recordType == 1:
            temp = []
            for x in self.data['1.03:']:
                temp.append((chr(US_CHAR)).join(x))
            self.data['1.03:'] = (chr(RS_CHAR)).join(temp)
        # separation prevents us from unnecessary gs at end of record
        keys = list(self.data.keys())
        lastkey = keys.pop(-1)
        if lastkey == '2.084:':
            if len(self.data['2.084:']) > 0:
                temp = []
                for x in self.data['2.084:']:
                    temp.append((chr(US_CHAR)).join(x))
                self.data['2.084:'] = (chr(RS_CHAR)).join(temp)
            else:
                lastkey = keys.pop(-1)
        for key in keys:
            print(key)
            value = self.data[key]
            recordData += f"{key}{value}".encode() + bytes(chr(GS_CHAR), 'UTF-8')
        recordData += f"{lastkey}{self.data[lastkey]}".encode()
        recordData += bytes(chr(FS_CHAR), 'UTF-8')
        tempHeader = f"{self.recordType}.01:".encode() + f"{len(recordData)}".encode() + bytes(chr(GS_CHAR), 'UTF-8')
        totalLength = len(tempHeader) + len(recordData)
        finalData = f"{self.recordType}.01:".encode() + f"{totalLength}".encode() + bytes(chr(GS_CHAR), 'UTF-8') + recordData
        
        return finalData
        
# utility to export file from data
# records is an ordered list of the data collected from the gui
# each record is a dictionary in {type:data} format
def create_nist_file(outputPath, records):
    # create empty file
    nistOut = NISTFile()
    # iterate through records and add to file in order
    for record in records:
        for key, value in records.items():
            recordType = int(key)
            data = None
            positionCode = None
            if recordType == 4:
                data = value['data']
                positionCode = value['pos']
            else:
                data = value
            nistOut.add_record(Record(recordType, data, positionCode))
    # Write the ANSI/NIST file
    with open(outputPath, 'wb') as f:
        f.write(nistOut.serialize())