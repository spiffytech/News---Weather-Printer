import string


def split(text, cwidth=50):
    maxLength = 0

    # Calculate the length of the longest paragraph
    for i in xrange(0, len(text)):
        if len(text[i].split("\n")) > maxLength:
            maxLength = len(text[i].split("\n"))
#
#    # Join and print the lines from each paragraph
#    for i in xrange(0, maxLength):
#        line = ""
#        for j in range(0, len(text)):
#            try:
#                line += text[j].split("\n")[i] + " | "
#            except: 
#                line += " | "
#        print line


    for i in xrange(0, maxLength):
        line = []
        for j in xrange(0, len(text)):
            try: 
                line.append(text[j].split("\n")[i])
            except:
                line.append("")

        tplate =  string.Template("$first | $second")
        print tplate.substitute(first=line[0], second=line[1])
