if __name__=="__main__":
    with open("./demo.txt") as fin:
        for l in fin:
            words = l.strip().split()
            if len(words)!=0:
                print l.strip()

