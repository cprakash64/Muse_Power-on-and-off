from muselsl import list_muses, stream, record

muses = list_muses()
if not muses:
    print("No MUSE headbands found")
else:
    # Stream data from the first MUSE found
    stream(muses[0]['address'])
    record(60)  # Record for 60 seconds
