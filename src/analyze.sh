#!/bin/sh
###### options processing ######
TEMP=`getopt -o Ai:h -n 'test_getopt.sh' -- "$@"`

if [ $? != 0 ] ; then TEMP="-h --" ; fi
eval set -- "$TEMP"
while true ; do
        case "$1" in
           -A ) shift; OPT_A="-A" ;;
           -i ) shift;  INPUT_FILE=$1; shift ;;
           -h ) cat <<EOT
Usage: $0 -i <input file> [-A]
Options:
  -A     print non-printable characters
  -i     specify input file name
  -h     this help
EOT
                shift; exit;;
           --) shift ; break ;;
        esac
done
if [ -z "$INPUT_FILE" ]; then echo "Must specify -i <filename>"; $0 -h; exit 1; fi
###### end of options processing ######
cat $OPT_A $INPUT_FILE