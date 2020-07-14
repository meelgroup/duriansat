import sys

if __name__ == "__main__":
    sorted_lines = []
    with open(sys.argv[1],"r") as f:
        for line in f:
            if not line[0] == 'd':
                sorted_lines.append(" ".join(list(map(str,sorted(list(map(int,line.split(" ")[:-1])))))))
    sorted_lines = sorted(sorted_lines)
    sorted_file = "sorted_"+sys.argv[1]
    with open(sorted_file,"w+") as f:
        for line in sorted_lines:
            f.write(line)
            f.write('\n')
