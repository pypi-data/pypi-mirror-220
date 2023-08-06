import argparse
from clean_epigraphia import processor

# This file is the command line tool to make use of processor
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-lang", help="script/language of text. Supports kn (Kannada)", required=True, choices=('kn', ))
    parser.add_argument("-a", help="whether to find and replace ā. Boolean", action='store_true', default=False)
    parser.add_argument("-e", help="whether to find and replace ē. Boolean", action='store_true', default=False)
    parser.add_argument("-o", help="whether to find and replace ō. Boolean", action='store_true', default=False)
    parser.add_argument("-s", help="whether to find and replace ś and Ś. Boolean", action='store_true', default=False)
    parser.add_argument("-sri", help="whether to find and replace the sequence śrī. Boolean", action='store_true', default=False)
    parser.add_argument("-n", help="whether to find and replace consonant clusters involving anunasika", action='store_true', default=False)
    parser.add_argument("-jn", help="whether to find and replace (probable) ñ", action='store_true', default=False)
    parser.add_argument("-m", help="whether to find and replace (probable) ṁ", action='store_true', default=False)
    parser.add_argument("-f", help="path of file containing unclean text")
    parser.add_argument("-i", help="for providing text in(command)line. Don't forget to enclose in double quotes")
    args = parser.parse_args()
    input = None
    if args.f:
        with open(args.f, 'r') as file:
            input = file.read()
    elif args.i:
        input = args.i
    else:
        print("One of -f or -i must be specified")
        exit(1)

    if not input:
        print("input is null")
        exit(1)

    output = processor(input, args.lang, args.a, args.e, args.o, args.s, args.sri, args.n, args.jn, args.m)
    if not output:
        print("An error occurred. Aborting")
        exit(1)

    if args.f:
        with open("output.txt", 'w') as file:
            file.write(output)
    else:
        print(output)
