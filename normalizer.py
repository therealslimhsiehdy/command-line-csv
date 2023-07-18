
import csv
from datetime import datetime, timedelta
import pytz
import sys

'''
INPUT: Date string (string)
OUTPUT: Date string converted from UTF-8 format to RFC3339 (string)
'''
def convert_to_rfc3339(date_str):
    # Parse the date string using the appropriate format
    date_obj = datetime.strptime(date_str, "%m/%d/%y %I:%M:%S %p")

    # Set the timezones
    pacific_tz = pytz.timezone('US/Pacific')
    eastern_tz = pytz.timezone('US/Eastern')

    # Convert date from PT to ET
    pacific_date_obj = pacific_tz.localize(date_obj)
    eastern_date_obj = pacific_date_obj.astimezone(eastern_tz)

    # Convert the ET date object to RFC3339 format
    rfc3339_date_str = eastern_date_obj.isoformat()

    return rfc3339_date_str

'''
INPUT: Zipcode (string)
OUTPUT: For zipcodes that are shorter than len(zip), then add 0's to the front (string)
'''
def convert_zipcode(zip):
    result = 5 - len(zip)
    if result > 0:
        return f"{result * '0'}{zip}"
    else:
        return zip

'''
INTPUT: Full name (string)
OUTPUT: Full name, but in ALL CAPS (string)
Note: I have not tested this with all languages (seemed fine for Japanese)
'''
def convert_name_upper(fullname):
    return fullname.upper()

'''
INPUT: Address (string)
OUTPUT: I printed it out normally, but the issue started here that I was not able to convert
the broken characters into UTF-8 (string)
'''
def convert_address(address):
    return address

'''
INPUT: Time w/ hours, minutes, seconds and ms (string)
OUTPUT: Seconds (integer)
Note: Returns the error "ValueError: time data '111:23:32.123' does not match format '%H:%M:%S.%f'"
If I were to redo this with more time, I'd split the hours / minutes / seconds up and do the math from there
'''
# def convert_time_total(timeduration):
#     time_duration = datetime.strptime(timeduration, "%H:%M:%S.%f")

#     # Calculate the total number of seconds
#     total_seconds = timedelta(hours=time_duration.hour, minutes=time_duration.minute, seconds=time_duration.second, microseconds=time_duration.microsecond).total_seconds()
#     return total_seconds

'''
INPUT: The processed stdin (reader object)
OUTPUT: Row that we want to write to the stdout (technically there's zero output but iykyk)
'''
def process_csv(reader):
    fieldnames = ['Timestamp', 'Address', 'ZIP', 'FullName', 'FooDuration', 'BarDuration', 'TotalDuration', 'Notes']

    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        converted_row = {
            "Timestamp": convert_to_rfc3339(row['Timestamp']),
            "ZIP": convert_zipcode(row['ZIP']),
            "FullName": convert_name_upper(row['FullName']),
            "Address": convert_address(row['Address']),
            # "FooDuration": convert_time_total(row['FooDuration']),
            # "BarDuration": convert_time_total(row['BarDuration'])
        }
        writer.writerow(converted_row)


'''
INPUT: stdin which is given from the command line 
OUTPUT: N/A
Note: The commented out code is the process I tried to do to convert sample-with-broken-utf-8.csv
to utf-8. There are different types of encoding so we have to go byte by byte.
'''
def main():
    # row_array = []
    # for line in sys.stdin.buffer:
    #     # Prints out each character separately in an array
    #     bytes = [chr(d) for d in line]
    #     row = ""
    #     # Each character is a diff encoding so we have to detect what "type" it is and convert
    #     for byte in bytes:
    #         try:
    #             str_char = byte.encode('utf-8')
    #             row += str_char.decode('utf-8')
    #         except UnicodeEncodeError:
    #             row += "\uFFFD"
    #     row_array.append(row)

    # csv_file_object = io.StringIO("".join(row_array))
    # reader = csv.DictReader(csv_file_object, delimiter=",")
    # process_csv(reader)

    reader = csv.DictReader(sys.stdin)
    process_csv(reader)

if __name__ == '__main__':
    main()