import os


def write_to_file(folder, file_name, data):
    os.umask(0)
    suffix = 0
    while os.path.exists(folder + file_name + '_' + str(suffix) + '.txt'):
        suffix += 1

    with open(folder + file_name + '_' + str(suffix) + '.txt', 'w+') as file_writer:
        file_writer.write(data)
        file_writer.close()
