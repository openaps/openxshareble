
import uuid

class Attrs:
    CradleService = uuid.UUID("F0ABA0B1-EBFA-F96F-28DA-076C35A521DB");

    # Share Characteristic Strings
    AuthenticationCode  = uuid.UUID("F0ABACAC-EBFA-F96F-28DA-076C35A521DB");
    ShareMessageReceiver = uuid.UUID("F0ABB20A-EBFA-F96F-28DA-076C35A521DB"); #  Max 20 Bytes - Writable
    ShareMessageResponse = uuid.UUID("F0ABB20B-EBFA-F96F-28DA-076C35A521DB"); #  Max 20 Bytes
    Command = uuid.UUID("F0ABB0CC-EBFA-F96F-28DA-076C35A521DB");
    Response = uuid.UUID("F0ABB0CD-EBFA-F96F-28DA-076C35A521DB"); #  Writable?
    HeartBeat = uuid.UUID("F0AB2B18-EBFA-F96F-28DA-076C35A521DB");

    # Possible new uuids????  60bfxxxx-60b0-4d4f-0000-000160c48d70
    CradleService2 = uuid.UUID("F0ACA0B1-EBFA-F96F-28DA-076C35A521DB");
    AuthenticationCode2  = uuid.UUID("F0ACACAC-EBFA-F96F-28DA-076C35A521DB"); #  read, write
    ShareMessageReceiver2 = uuid.UUID("F0ACB20A-EBFA-F96F-28DA-076C35A521DB"); #  read, write
    ShareMessageResponse2 = uuid.UUID("F0ACB20B-EBFA-F96F-28DA-076C35A521DB"); #  indicate, read
    Command2 = uuid.UUID("F0ACB0CC-EBFA-F96F-28DA-076C35A521DB"); #  read, write
    Response2 = uuid.UUID("F0ACB0CD-EBFA-F96F-28DA-076C35A521DB"); #  indicate, read, write
    HeartBeat2 = uuid.UUID("F0AC2B18-EBFA-F96F-28DA-076C35A521DB"); #  notify, read

    # Device Info
    DeviceService = uuid.UUID("00001804-0000-1000-8000-00805f9b34fb");
    PowerLevel = uuid.UUID("00002a07-0000-1000-8000-00805f9b34fb");

    VENDOR_UUID = uuid.UUID("F0ACA0B1-EBFA-F96F-28DA-076C35A521DB")

