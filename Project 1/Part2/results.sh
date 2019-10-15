#!/bin/bash
#####################################
## COMP211 @ TUC                   ##
## Grigoriades Ioannis: 2014030007 ##
## Manesis Athanasios : 2014030061 ##
## LAB21142503                     ##
## Bash scripting PART 2           ##
#####################################

#Some function declarations
function FillArrays(){
  if [[ " ${TEAMS_ARRAY[*]} " != *" $1 "* ]]                                    #The way we reading the file, on each line we get 4 variables (TEAM_A-TEAM_B:SCORE_A-SCORE_B)
  then                                                                          #We search if the TEAM_A is on the array if it is NOT we add the team on it and we update the
    if [ $2 -gt $3 ]                                                            #rest of the arrays accordint to the match result
    then                                                                        #
      POINTS_ARRAY[$COUNTER]=$(( ${POINTS_ARRAY[$COUNTER]} + 3 ))               #If the team exist on the array then we only update the rest of the arrays
    fi                                                                          #We do the same thing twice to fix the arrays for the TEAM_B
                                                                                #
    if [ $2 -lt $3 ]
    then
      POINTS_ARRAY[$COUNTER]=$(( ${POINTS_ARRAY[$COUNTER]} + 0 ))
    fi

    if [ $2 -eq $3 ]
    then
      POINTS_ARRAY[$COUNTER]=$(( ${POINTS_ARRAY[$COUNTER]} + 1 ))
    fi

    GOAL_SCORES_ARRAY[$COUNTER]=$(( ${GOAL_SCORES_ARRAY[$COUNTER]} + $2 ))
    GOAL_TAKEN_ARRAY[$COUNTER]=$(( ${GOAL_TAKEN_ARRAY[$COUNTER]} + $3 ))

    TEAMS_ARRAY[$COUNTER]=$1
    ((COUNTER++))
  else
    for((k=0; k<${#TEAMS_ARRAY[@]}; k++))
    do
      if [[ "${TEAMS_ARRAY[$k]}" = "${1}" ]]
      then
        POSITION_OF_TEAM=$k
        break
      fi
    done

    if [ $2 -gt $3 ]
    then
      POINTS_ARRAY[$POSITION_OF_TEAM]=$(( ${POINTS_ARRAY[$POSITION_OF_TEAM]} + 3 ))
    fi

    if [ $2 -lt $3 ]
    then
      POINTS_ARRAY[$POSITION_OF_TEAM]=$(( ${POINTS_ARRAY[$POSITION_OF_TEAM]} + 0 ))
    fi

    if [ $2 -eq $3 ]
    then
      POINTS_ARRAY[$POSITION_OF_TEAM]=$(( ${POINTS_ARRAY[$POSITION_OF_TEAM]} + 1 ))
    fi

    GOAL_SCORES_ARRAY[$POSITION_OF_TEAM]=$(( ${GOAL_SCORES_ARRAY[$POSITION_OF_TEAM]} + $2 ))
    GOAL_TAKEN_ARRAY[$POSITION_OF_TEAM]=$(( ${GOAL_TAKEN_ARRAY[$POSITION_OF_TEAM]} + $3 ))

  fi
}

function Swap(){
  TMP_NAME=${TEAMS_ARRAY[$1]}                                                   #Keeping the old values for the swap on 4 different arrays
  TMP_POINTS=${POINTS_ARRAY[$1]}
  TMP_GOALS_SCORES=${GOAL_SCORES_ARRAY[$1]}
  TMP_GOALS_TAKEN=${GOAL_TAKEN_ARRAY[$1]}

  TEAMS_ARRAY[$j]=${TEAMS_ARRAY[$1+ 1]}                                         #Swapping on four arrays
  TEAMS_ARRAY[$1 + 1]=$TMP_NAME

  POINTS_ARRAY[$j]=${POINTS_ARRAY[$1+ 1]}
  POINTS_ARRAY[$1 + 1]=$TMP_POINTS

  GOAL_SCORES_ARRAY[$j]=${GOAL_SCORES_ARRAY[$1 + 1]}
  GOAL_SCORES_ARRAY[$1 + 1]=$TMP_GOALS_SCORES

  GOAL_TAKEN_ARRAY[$j]=${GOAL_TAKEN_ARRAY[$1 + 1]}
  GOAL_TAKEN_ARRAY[$1+ 1]=$TMP_GOALS_TAKEN
}

BubbleSort () {                                                                 #$1 = Array to be sort $2 = lenght of array
  for (( i=0; i<${#TEAMS_ARRAY[@]}-1; i++ ))                                    #This is the good old bubble sort converted to bash, is this the fastest? Absolutly not
  do                                                                            #But it is simple and IF IT WORKS IT AIN'T STUPID!
    for(( j=0; j<${#TEAMS_ARRAY[@]}-$i-1 ;j++))                                 #Also it comes with a twist that covers the sortnig on the name of the team
    do
      if (( ${POINTS_ARRAY[j]} == ${POINTS_ARRAY[$((j + 1))]} ))                #if the points are equal we sort on names
      then
        if [[ ${TEAMS_ARRAY[j]} > ${TEAMS_ARRAY[$((j + 1))]} ]]                 #Checking for alphanumeric equality
        then
          Swap "$j"
        fi
      fi
      if (( ${POINTS_ARRAY[j]} < ${POINTS_ARRAY[$((j + 1))]} ))
      then
        Swap "$j"
      fi
    done
  done
}
#
TEAMS_ARRAY=()                                                                  #Initializing four arrays to keep the the names, points and goals of each team (scored and taken).
POINTS_ARRAY=()
GOAL_SCORES_ARRAY=()
GOAL_TAKEN_ARRAY=()
LINE_NUMBER=0                                                                   #This is a pointer that shows the current line from the lines that the file has.
COUNTER=0                                                                       #This is count the teams from the file e.g if counter is 5 there are 5 indivitual teams on the file.
FILE_LINES=$(wc -l < $1)                                                        #wc command counts the lines of the file provided.
LINE_TEAMS_CONTENT=""                                                           #Temporary string to keep the names from the scores appart
LINE_SCORE_CONTENT=""                                                           #they are ovverwritten each time

for ((i=0; i<$FILE_LINES; i++))                                                 #We reading the file one time line by line
do
  ((LINE_NUMBER++))                                                                    #Is initialized to 0 so we incresing it at the start of the for-loop
  LINE_TEAMS_CONTENT=$( echo $( tail -n+$LINE_NUMBER $1 | head -n1 ) | cut -f 1 -d":") #Tail and head (tail outputs the last NUM lines starting with the number we provide)
  TEAM_A=$( echo $( echo $LINE_TEAMS_CONTENT | cut -d "-" -f 1 ))                      #piping it to the head that just takes the first from it we manage to get any line from the file
  TEAM_B=$( echo $( echo $LINE_TEAMS_CONTENT | cut -d "-" -f 2 ))                      #by providing the line number. The cut command keeps the field before the delimeter (that we provide e.g ':', '-').

  LINE_SCORE_CONTENT=$( echo $( tail -n+$LINE_NUMBER $1 | head -n1 ) | cut -f 2 -d":") #The same method is used for the score. This time
  SCORE_A=$( echo $( echo $LINE_SCORE_CONTENT | cut -d "-" -f 1 ))                     #we take the second field after the ':' which is the score
  SCORE_B=$( echo $( echo $LINE_SCORE_CONTENT | cut -d "-" -f 2 ))                     #

  FillArrays "$TEAM_A" "$SCORE_A" "$SCORE_B"                                    # $1 = TEAM_A $2 = SCORE_A $3 = SCORE_B
  FillArrays "$TEAM_B" "$SCORE_B" "$SCORE_A"                                    # $1 = TEAM_B $2 = SCORE_B $3 = SCORE_A
done

BubbleSort                                                                      #

for((i=0; i<${#TEAMS_ARRAY[@]}; i++))                                           #Printing the results using tabs is not an eye candy but...
do
  echo -e "$(($i + 1)).\t${TEAMS_ARRAY[$i]}\t${POINTS_ARRAY[$i]}\t${GOAL_SCORES_ARRAY[$i]}:${GOAL_TAKEN_ARRAY[$i]}" >> tmpfile #A better solution for printing                                                                                                                               #Comment out ">> tmpfile" to be more accurate
done
column -t tmpfile                                                                                                              #Using column try man column for details
rm tmpfile
