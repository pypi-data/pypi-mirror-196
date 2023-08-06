# These are the list of modules needed to run the program
import mailbox
import re


# This function will read the MBOX file and search for emaill address
def mboxwriter(mbox, output):
    mbox = mailbox.mbox(mbox)
    file = open(output, 'a')
    for message in mbox:
        file.write(message['from']+'\n')


def createmailerlist(output, dir, filename):
    file_in = open(output,'r')
    addr_lines = file_in.read()
    addr_list = re.findall('\S+@\S+', addr_lines)
    addr_set = set()
    # Remove no reply addresses and remove duplicates
    for elem in addr_list:
        elem = elem[1:-1]
        addr_set.add(elem)
    # store all addresses in a file
    clean_addr = open(dir + filename, 'a')
    for elem in addr_set:
        clean_addr.write(elem+'\n')
    clean_addr.close()