#!/bin/bash
#####################################
## COMP211 @ TUC                   ##
## Grigoriades Ioannis: 2014030007 ##
## Manesis Athanasios : 2014030061 ##
## LAB21142503                     ##
## Bash scripting PART 1           ##
#####################################
NUMBER_OF_ARGUMENTS=$#                                                          #Passing the number of arguments (number of files) in the variable.
NUM_OF_ARGS=$NUMBER_OF_ARGUMENTS                                                #Keeping a copy of the variable
FILE_TO_ARRAY=()                                                                #Initializing some array
XY_ARRAY=()
LINES_IN_FILES=()
FILE_NAMES=()
while [ $NUM_OF_ARGS -gt 0 ]                                                    #Reading the files line by line into an array containing both of X and Y
do                                                                              #in the specific order of [Xfile1.1 Yfile1.1, Xfile1.2 Yfile1.2 ... Xfile1.N Yfile1.N ... XfileN.M YfileN.M
  COUNTER1=0                                                                    #Just a regular counter
  XY_ARRAY=()                                                                   #Re-Initializing the array
  OLDIFS="$IFS"                                                                 #Dont mess with the old IFS... Keep track of it
  IFS=$'\n:'                                                                    #IFS now will change element after new line or the character ":"
  for line in $(cat $1)                                                         #Read the current file into the array line by line ( or :)
  do
    XY_ARRAY[$COUNTER1]=$line
    ((COUNTER1++))
  done
  FILE_TO_ARRAY+=("${XY_ARRAY[@]}")                                             #Stacking the array with the current file into THE ONE array that rules them all
  LINES_IN_FILES+=($(wc -l < $1))                                               #An array keeping the lines of each file in order arg1, arg2, arg3 ... (using wc command)
  FILE_NAMES+=("$1")                                                            #An array keeping the names of the files before shift occures
  shift                                                                         #Reject the $n argument and it place takes the $n+1
  IFS="$OLDIFS"                                                                 #Restore the IFS
  ((NUM_OF_ARGS--))                                                             #Exit condition for the while loop (when all the files are read)
done

SIZE_OF_FILE_TO_ARRAY=${#FILE_TO_ARRAY[@]}                                      #Figuring out the size of the ONE array
X_ARRAY=()
Y_ARRAY=()
COUNTER2=0
while [ $COUNTER2 -le $SIZE_OF_FILE_TO_ARRAY ]                                  #Because of X and Y are comming in pair we know that there is un even number of Xs and Ys.
do                                                                              #Because of the way we fill our array the pair always starts with un X followed by Y.
  if [ $(($COUNTER2%2)) -eq 0 ]                                                 #So if the pointer is on an even # of cell that mast be an X otherwise Y.
  then                                                                          #In this way we creating two arrays that containing all the Xs and Ys.
    X_ARRAY+=("${FILE_TO_ARRAY[$COUNTER2]}")                                    #The two arrays are in form of X_ARRAY[X1.1 .. X1.N X2.1 .. X2.N Xn.1 .. Xn.n ] Y_ARRAY[...]
  else
    Y_ARRAY+=("${FILE_TO_ARRAY[$COUNTER2]}")
  fi
  ((COUNTER2++))
done


COUNTER3=0
FIXER=0
while [ $COUNTER3 -lt $NUMBER_OF_ARGUMENTS ]                                    #The algorythms to calculate the coefficients are running in while loop
do                                                                              #for each file provided
  SUMX=0                                                                        #The for-loop is running the equations on each file according to the
  SUMX2=0                                                                       #number of lines the file has it may be deferent on each file.
  SUMY=0
  SUMXY=0
  A=0                                                                           #The A, B and ERR coefficients are calculated inside the loop
  B=0                                                                           #by overwritting their values until they get their final value.
  ERR=0
  ERR1=0                                                                        #A FIXER variable used to jumb the pointer to the apropriate
  ERR2=0                                                                        #cell (for the next file) after the for-loop resets.
  for ((i=0; i<${LINES_IN_FILES[$COUNTER3]}; i++))
  do
    SUMX=$(echo "scale=2; ${SUMX} + ${X_ARRAY[$((i + FIXER))]}" | bc)
    SUMX2=$(echo "scale=2; ${SUMX2} + ${X_ARRAY[$((i + FIXER))]} * ${X_ARRAY[$((i + FIXER))]}" | bc)
    SUMY=$(echo "scale=2; ${SUMY} + ${Y_ARRAY[$((i + FIXER))]}" | bc)
    SUMXY=$(echo "scale=2; ${SUMXY} + ${X_ARRAY[$((i + FIXER))]} * ${Y_ARRAY[$((i + FIXER))]}" | bc)

    B=$(echo "scale=2; (${LINES_IN_FILES[$COUNTER3]} * ${SUMXY} - ${SUMX} * ${SUMY}) / (${LINES_IN_FILES[$COUNTER3]} * ${SUMX2} - ${SUMX} * ${SUMX})" | bc)
    A=$(echo "scale=2; (${SUMY} - ${B} * ${SUMX}) / ${LINES_IN_FILES[$COUNTER3]}" | bc)
    ERR1=$(echo "scale=2; ${SUMY}/1" | bc)
    ERR2=$(echo "scale=2; (${A} * ${SUMX} + ${B})/1" | bc )
    ERR=$(echo "scale=2; (${ERR1} - ${ERR2}) * (${ERR1} - ${ERR2})" | bc )      #In manual pages of bc explained that subtraction won't read scale variable so we divide by 1

  done
  FIXER=$FIXER+${LINES_IN_FILES[$COUNTER3]}



  echo "FILE: ${FILE_NAMES[$COUNTER3]}, a=$A b=$B c=1 err=$ERR"
  ((COUNTER3++))
done
