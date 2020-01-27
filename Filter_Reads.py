# This file is part of read_filter.
#
# read_filter is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# read_filter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with read_filter. If not, see <http://www.gnu.org/licenses/>.


# This script is written by Ben Matern.
# It filters reads based on length.
# The main method (starting point) is at the bottom.

from sys import argv
from getopt import getopt, GetoptError

from os.path import isfile, isdir, join, split
from os import listdir, makedirs

def prepareReads(inputGuppyBarcodeDirectory, outputFileName, minLength, maxLength):

    print('Filtering reads in:' + inputGuppyBarcodeDirectory)
    # Loop input files in directory.
    fileList = [f for f in listdir(inputGuppyBarcodeDirectory) if isfile(join(inputGuppyBarcodeDirectory, f))]

    # Should be only one file in this list....
    # TODO: This is a bug if there is more than one file in the directory. The outputfile should be created outside this loop.
    for inputFileName in fileList:
        if('.fastq' in inputFileName):
            # Open Input File
            inputFile = open(join(inputGuppyBarcodeDirectory,inputFileName), 'r')

            # Create Output File
            outputFile = createOutputFile(outputFileName)

            # Brilliant Exception Handling
            try:

                readID=None
                readSequence=None
                readQuality=None
                readCount = 0
                filteredReadCount = 0


                # Loop while there are still lines
                for index,line in enumerate(inputFile):

                    readType = index % 4 # Modulus. Fastq files have 4 lines per read.

                    if(readType == 0):
                        readID = line # Includes the initial @ character
                    elif (readType == 1):
                        readSequence = line
                    elif (readType == 2):
                        pass
                    elif (readType == 3):
                        readQuality = line

                        if(readID is None):
                            raise Exception('Missing Read ID')
                        elif(readSequence is None):
                            raise Exception('Missing Read Sequence')
                        elif(readQuality is None):
                            raise Exception('Missing Read Qualities')
                        else:
                            # Everything is ready, filter the read length.
                            readCount += 1

                            readLength = len(readSequence)
                            if(readLength >= int(minLength) and readLength <= int(maxLength)):
                                filteredReadCount += 1

                                outputFile.write(readID)
                                outputFile.write(readSequence)
                                outputFile.write('+\n')
                                outputFile.write(readQuality)

                        # Reset variables.
                        readID = None
                        readSequence = None
                        readQuality = None

                    else:
                        raise Exception('Somehow there is a wrong read type, I dont know how you did that.')

                outputFile.close()

                print('File ' + inputFileName + ' contained ' + str(readCount) + ' reads.\n'
                      + str(filteredReadCount) + ' were the correct length ('
                      + str(minLength) + ':' + str(maxLength) + ')\n')

            except Exception as e:
                print('Oh no! An exception!')
                print(str(e))


def readArgs():
    # Trying to be consistent and global with my parameter inputs.

    global inputDirectory
    global minimumReadLength
    global maximumReadLength
    global barcodeList

    inputDirectory = None
    minimumReadLength = None
    maximumReadLength = None
    barcodeList = None

    if (len(argv) < 3):
        print ('I don\'t think you have enough arguments.\n')
        # usage()
        return False

    print('Attempting to load commandline arguments')
    # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
    try:
        opts, args = getopt(argv[1:]
                            , "m:M:b:i:"
                            , ["minlen=", "maxlen=", "barcode=", "inputdirectory="])

        print (str(len(opts)) + ' arguments found.')

        for opt, arg in opts:

            if opt in ("-b", "--barcode"):
                barcodeList = arg

            elif opt in ("-m", "--minlen"):
                minimumReadLength = int(arg)

            elif opt in ("-M", "--maxlen"):
                maximumReadLength = int(arg)

            elif opt in ("-i", "--inputdirectory"):
                inputDirectory = arg

            else:
                print('Unknown Commandline Option:' + str(opt) + ':' + str(arg))
                raise Exception('Unknown Commandline Option:' + str(opt) + ':' + str(arg))


    except GetoptError as err:
        print ('Something seems wrong with your commandline parameters.')
        print (str(err.msg))
        print ('Unknown option: ' + str(err.opt))
        # print (errorMessage)
        # usage()
        return False

    return True

def createOutputFile(outputfileName):
    tempDir, tempFilename = split(outputfileName)
    if not isdir(tempDir):
        print('Making Directory:' + tempDir)
        makedirs(tempDir)
    resultsOutput = open(outputfileName, 'w')
    return resultsOutput


# MAIN METHOD
if __name__=='__main__':
    readArgs()

    barcodeArray = barcodeList.split(',')
    print('Filtering Barcodes. You gave me a list of ' + str(len(barcodeArray)) + ' barcodes to filter.\n')

    # Loop each barcode
    for barcodeString in barcodeArray:

        guppyBarcodeReadDir = join(join(inputDirectory,'DemultiplexedGuppy'),'barcode' + str(barcodeString))
        outputFileName = join(join(inputDirectory, 'Demultiplexed'),'BC' + str(barcodeString) + '.fastq')

        prepareReads(guppyBarcodeReadDir
            ,outputFileName
            ,minimumReadLength
            ,maximumReadLength )

    print('Done Filtering Reads.')



