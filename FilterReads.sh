# This shows you how to call the Filter_Reads.py script.
ExperimentDirectory=$(pwd)"/experiment_id"
BarcodeList="09,10,13,14,90"

python Filter_Reads.py --inputdirectory=$ExperimentDirectory --barcode=$BarcodeList --minlen="3000" --maxlen="4000"

