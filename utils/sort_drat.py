import sys

if __name__ == "__main__":
    line_no = 0
    sorted_lines = []
    tags = []
    with open(sys.argv[1],"r") as f:
        for line in f:
            line_no += 1
            if not line[0] == 'd':
                tag = line.split(" ")[-1:][0]
                if not tag[0] == '0':
                    if not (line.split(" ")[-2:-1][0] == '0'):
                        print("zero = ",line.split(" ")[-2:-1])
                    assert(line.split(" ")[-2:-1][0] == '0')
                    clause = line.split(" ")[:-2]
                    tag = " 0 " + tag[:-1] + " : " + str(line_no)
                else:
                    clause = line.split(" ")[:-1]
                    tag = " " +tag[0] + " : " + str(line_no)
                tags.append(tag)
                sorted_lines.append( \
                    (" ".join(list(map(str,sorted(list(map(int,clause))))))) \
                    +tag)
    sorted_lines = sorted(sorted_lines)
    sorted_file = "sorted_"+sys.argv[1]
    with open(sorted_file,"w+") as f:
        total_lines = 0
        unique_lines = 0
        last_line = ""
        for line in sorted_lines:
            if last_line.split(" 0")[0] != line.split(" 0")[0]:
                unique_lines += 1
            last_line = line
            f.write(line)
            #f.write(" "+tags[total_lines])
            total_lines += 1
            f.write('\n')
    print("Unique learnt clauses : %.2f percent" % (100*unique_lines/total_lines))
