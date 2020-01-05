from datetime import datetime as dt

def timer(t, label):
    duration = dt.now() - t
    duration = duration.total_seconds()
    print("{} took {}".format(label, duration))
    return duration

def write_gcode(output_file_name, data):

    t1 = dt.now()
    with open(output_file_name, 'w+') as output_file:
        for i in data:
            output_file.write(i + "\n")
    timer(t1, "writing file     ")