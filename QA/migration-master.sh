#! /bin/bash
#sets debugging
set -x
###################
#### QA SCRIPT ####
###################
ABSOLUTEPATH="OXES_ANNOTATIONS_QA_CHECK"
############################################################
#### find oxes file to transform to sfm, copy to source ####
############################################################
#for logging
LOGFILEOUTPUT=""$ABSOLUTEPATH"/workingdirectory/logfile"
{
echo
echo "******************************************************"
echo
if [[ $# -eq 0 ]] ; then echo "No project specificed in script. Place project number as parameter when you run the script. E.g. bash migration-master.sh 1665. Exiting..." ; exit 1 ; fi
PROJECTNUM="$1"
workingdir=$(pwd)
#QUBESINCOMINGSRCFILE="/home/user/QubesIncoming/win7/"$PROJECTNUM""
OXESSRCFILE=""$ABSOLUTEPATH"/source/"$PROJECTNUM""
OXESSRCFILEJAVA="OXES_ANNOTATIONS_QA_CHECK\source\\$PROJECTNUM"

echo "Processing QA check on $PROJECTNUM"
echo
# if [[ -f "$QUBESINCOMINGSRCFILE" ]] && [[ -f "$OXESSRCFILE" ]]
# then 
	# while true; do
	    # read -p "source file found in Qubesincoming folder, do you want to overwrite the source folder oxes file with the file in Qubesincoming? (answer y or n)" yn
	    # case $yn in
		# [Yy]* ) mv "$QUBESINCOMINGSRCFILE" "./source/" && echo "moving and overwriting..."; break;;
		# [Nn]* ) echo "keeping original file in project source folder, not overwriting"; break;;
		# * ) echo "Please answer y or n.";;
	    # esac
	# done
# elif [[ -f "$QUBESINCOMINGSRCFILE" ]] && [[ ! -f "$OXESSRCFILE" ]]
# then
	# echo "source file found in Qubesincoming folder, copying to source folder..."
	# mv "$QUBESINCOMINGSRCFILE" "source/"
# elif [[ ! -f "$QUBESINCOMINGSRCFILE" ]] && [[ -f "$OXESSRCFILE" ]]
# then 
	# echo "source file found in project source folder, continuing..."
# elif [[ ! -f "$QUBESINCOMINGSRCFILE" ]] && [[ ! -f "$OXESSRCFILE" ]] 
# then
	# echo "source file not found in Qubesincoming folder, transfer it from win7 machine. Exiting..."
	# exit 1
# fi
##########################################
#### count how many notes/annotations ####
##########################################

echo
OXESANNOTTOTAL=$(pcregrep -o "<annotation" "$OXESSRCFILE" | wc -l)
OXESANNOTNONOTE=$(pcregrep -o "<category xml:lang=\"tr\">NoNote" "$OXESSRCFILE" | wc -l)
OXESANNOTMISC=$(pcregrep -o "<category xml:lang=\"tr\">Misc" "$OXESSRCFILE" | wc -l)
#finds number of annotations where notationCategories doesn't exist
OXESANNOTNONOTCAT=$(xmllint --shell "$OXESSRCFILE"<<< "xpath (//annotation[not(notationCategories)])" | grep -Po "(?<=content=)[A-Z]{3}\.\d+\.\d+" | wc -l)
#found edge case where nonote and misc are both indicated for same annotation so are counted twice but should only count once therefore adding it rather than subtracting
OXESANNOTNONOTMISCSAME=$(pcregrep -M "<notationCategories>\\n\\s+<category xml:lang=\"[a-z]+\">(Misc|NoNote)<\/category>\n\s+<category xml:lang=\"[a-z]+\">(Misc|NoNote)<\/category>" "$OXESSRCFILE" | grep notationCategories | wc -l)
OXESANNOTNUMB=$(($OXESANNOTTOTAL - $OXESANNOTNONOTE - $OXESANNOTMISC - $OXESANNOTNONOTCAT + $OXESANNOTNONOTMISCSAME))
echo "Total Annotations to process in oxes file: $OXESANNOTNUMB"

##################################################################
# cleanup commands // run python and XSLT transform scripts   ####
##################################################################

echo
echo "Initial transformation from .oxes to .sfm..."
#remove wycliffe namespace, doesn't work otherwise
sed -i "s/ xmlns=\"http:\/\/www.wycliffe.net\/scripture\/namespace\/version_1.1.4\"//" "$OXESSRCFILE"
#combine some tags per Steve Woodard
sed -i "s/OsmLugat2/OsmLugat/" "$OXESSRCFILE"
sed -i "s/OsmLugat3/OsmLugat/" "$OXESSRCFILE"
sed -i "s/BTSozluk2/BTSozluk/" "$OXESSRCFILE"
sed -i "s/BTSozluk3/BTSozluk/" "$OXESSRCFILE"
#removing following character sequence so it doesn't conflict with python script
sed -i "s/==//g" "$OXESSRCFILE"
#fixing weird issue with weird annotation
sed -i "s/eyyâm (-ı ikâmeti)/eyyâmıikâmeti/g" "$OXESSRCFILE"

#cleaning out working directory
rm -rf "$ABSOLUTEPATH"/workingdirectory/*.txt
rm -rf "$ABSOLUTEPATH"/workingdirectory/*.sfm

SFMOUTPUT=""$ABSOLUTEPATH"/workingdirectory/sfmoutput"$1"_1.sfm"
SFMOUTPUTJAVA="OXES_ANNOTATIONS_QA_CHECK\workingdirectory\sfmoutput"$1"_1.sfm"
XSLT=""$ABSOLUTEPATH"/scripts/TE-Paratext-XSLT_main_text_conversion_and_annotations_v2_filtering_misc_categories_forannotationQA.xsl"
XSLTJAVA="OXES_ANNOTATIONS_QA_CHECK\scripts\TE-Paratext-XSLT_main_text_conversion_and_annotations_v2_filtering_misc_categories_forannotationQA.xsl"
##XSLT transformation - need to install libsaxonb-java in ubuntu
#saxonb-xslt -o:"$SFMOUTPUT" -s:"$OXESSRCFILE" -xsl:"$XSLT"
export PATH=$PATH:"/cygdrive/C/Program\ Files/Java/jre1.8.0_301/bin/"
java -jar saxon9he.jar -o:"$SFMOUTPUTJAVA" -s:"$OXESSRCFILEJAVA" -xsl:"$XSLTJAVA"
#java -jar saxon9he.jar -o:result.sfm  -s:joined1886allbooks.oxes  -xsl:TE-Paratext-XSLT_main_text_conversion_and_annotations_v2_filtering_misc_categories_forannotationQA.xsl
# grep '\\p' result.sfm |wc -l
#24849 \p in orig
#find regex:
#(\n)(\s+)(\\p.*$)
#replace with:
#$3

#more cleanup after transformation script
#removes white space
sed -i "s/^ *//" "$SFMOUTPUT"
#remove 1st line which is blank for some reason
sed -i "1d" "$SFMOUTPUT"
#remove last line which is blank for some reason
sed -i "$d" "$SFMOUTPUT"
#gnome-open "$SFMOUTPUT"
echo

##########################################################
# in new file count how many annotations/notes it has ####
##########################################################

SFMANNOTNUMB=$(pcregrep -o ".\\\\f \+ \\\\fr" "$SFMOUTPUT" | wc -l)
#SFMANNOTMISSING=$(($OXESANNOTNUMB - $SFMANNOTNUMB))
echo "Total Annotations in .sfm file: $SFMANNOTNUMB"
#echo "Total Annotations not in .sfm file: $SFMANNOTMISSING"
echo

SFMSORTEDDIFFOUTPUT=""$ABSOLUTEPATH"/workingdirectory/sfmoutput"$1"_1_sortedfordiff.sfm"
rm -f "$SFMSORTEDDIFFOUTPUT"
cat "$SFMOUTPUT" | perl -CSA -MUnicode::Normalize=NFD -ne 'print NFD($_)' | pcregrep -o "(?<=\\\\f \+ \\\\fr )[A-Z0-9]{3}\.\d+\.\d+ .+?(?=\d)" | sort -t " " -k2 -k1 | sort > "$SFMSORTEDDIFFOUTPUT"

################################################################
# run QA scripts to identify which ones aren't being caught ####
################################################################

#nested annotations only 0 and 1 are probably nested, 2+ probably not
#QANESTEDANNOTATIONSCHECK=""$ABSOLUTEPATH"/workingdirectory/"$1"_possible_nested_annotations_QA.csv"
#QANESTEDANNOTATIONSSCRIPT=""$ABSOLUTEPATH"/scripts/possible_nested_annotations_QA_to_csv.py"
#rm -f "$QANESTEDANNOTATIONSCHECK"
#python3 "$QANESTEDANNOTATIONSSCRIPT" "$PROJECTNUM" > "$QANESTEDANNOTATIONSCHECK"

#running script to determine to identify the annotations that aren't being matched with the verse for various reasons
#reasons: misspelling, duplicate same annotations, nonexisting text to match up with annotation, double nested annotations (valid need to do manually)
QAUNMATCHEDANNOTATIONS=""$ABSOLUTEPATH"/scripts/oldpythonscript_template_works_beginnging_end_updated.py"
echo
echo "Generating list of annotations in transformed .sfm file"
echo "Comparing lists, generating list of annotations with misspellings..."
#python3 "$QAUNMATCHEDANNOTATIONS" "$PROJECTNUM" > /dev/null 2>&1
python3 "$QAUNMATCHEDANNOTATIONS" "$PROJECTNUM" > ""$ABSOLUTEPATH"/workingdirectory/pythonlogfile" 2>> pythonerrorlogfile
PYTHONSFMANNOTNUMB=$(grep -o "\\\f + \\\fr" ""$ABSOLUTEPATH"/workingdirectory/"$1"_pythonoutput.sfm" | wc -l)
MISSINGANNOTS=$(($OXESANNOTNUMB - $PYTHONSFMANNOTNUMB))
PYTHONSFMSORTEDDIFFOUTPUT=""$ABSOLUTEPATH"/workingdirectory/pythonsfmoutput"$1"_sortedfordiff.sfm"
rm -fr "$PYTHONSFMSORTEDDIFFOUTPUT"
UNMATCHEDANNOTATIONS="/tmp/"$1"_unmatchedannotations.txt"
UNMATCHEDANNOTATIONSWITHVERSE=""$ABSOLUTEPATH"/workingdirectory/"$1"_unmatchedannotationswithverse.txt"
#comparing and sorting unmatched annotations into a list
cat ""$ABSOLUTEPATH"/workingdirectory/"$1"_pythonoutput.sfm" | perl -CSA -MUnicode::Normalize=NFD -ne 'print NFD($_)' | pcregrep -o "(?<=\\\\f \+ \\\\fr )[A-Z0-9]{3}\.\d+\.\d+ .+?(?=\d)" | sort -t " " -k2 -k1 | sort > "$PYTHONSFMSORTEDDIFFOUTPUT"
comm -3 <(sort "$PYTHONSFMSORTEDDIFFOUTPUT") <(sort "$SFMSORTEDDIFFOUTPUT") | sort -t " " -k2 > "$UNMATCHEDANNOTATIONS"
echo "**************************************************************"
numberofunmatchedannots=$(cat "$UNMATCHEDANNOTATIONS" | wc -l)
echo "analyzing $numberofunmatchedannots problematic annotations..."
echo "**************************************************************"
echo "**************************************************************"
echo "**************************************************************"
echo "**************************************************************"
echo "**************************************************************"
#need to convert file to UTf8 or grep doesn't work
SFMOUTPUTUTF8="/tmp/sfmoutput"$1"_1.sfm"
cat "$SFMOUTPUT" | perl -CSA -MUnicode::Normalize=NFD -ne 'print NFD($_)' > "$SFMOUTPUTUTF8"
#output final list of terms,references,and verse text with all \p
#cat "$UNMATCHEDANNOTATIONS" | while read line; do grep "$line" "$SFMOUTPUTUTF8" ; done > "$UNMATCHEDANNOTATIONSWITHVERSE"

#formatting for csv
rm -rf "$UNMATCHEDANNOTATIONSWITHVERSE".csv
touch "$UNMATCHEDANNOTATIONSWITHVERSE".csv
echo "Reference,Annotation Term,Notes,Status,All annotations in verse" >> "$UNMATCHEDANNOTATIONSWITHVERSE".csv
echo "" >> "$UNMATCHEDANNOTATIONSWITHVERSE".csv
cat "$UNMATCHEDANNOTATIONS" | while read line
do
	ref=$(echo "$line" | cut -d " " -f 1 | sed 's/\t//')
	annot=$(echo "$line" | cut -d " " -f 2-)
	versetext=$(grep "$line" "$SFMOUTPUTUTF8" | pcregrep -Mo "(?<===####).*$")
	allannots=$(grep "$line" "$SFMOUTPUTUTF8" | pcregrep -Mo '(?<===).+?(?=\*\*)' | tr '\n' '*')
	dups=$(grep "$line" "$SFMOUTPUTUTF8" | pcregrep -Mo '(?<===).+?(?=\*\*)' | sort -u | wc -l)
	allannotsnum=$(echo "$allannots" | grep -o '\*' | wc -l)
	dupsargument=$(if [ $allannotsnum -ne $dups ] ; then echo "$annot exact duplicate" ; fi)
	nested=$(echo $allannots | tr '*' '\n' | sort -u | while read annotterm; do nestedannotsnum=$(echo "$allannots" | grep -io "$annotterm" | wc -l); if [ $nestedannotsnum -eq 2 ] ; then echo "$annotterm found nested another annotation in $allannots: $nestedannotsnum"; fi ; done )  

	echo "$ref,$annot,,$versetext,$allannots,$dupsargument,$nested" >> "$UNMATCHEDANNOTATIONSWITHVERSE".csv
done
#filter out exact matches and nested ones that I will do manually
grep -n 'found nested' "$UNMATCHEDANNOTATIONSWITHVERSE".csv | cut -d ":" -f 1 | tac |  while read line ; do sed -i ""$line"d" "$UNMATCHEDANNOTATIONSWITHVERSE".csv ;done #comment back
totalnummispelledterms1=$(echo "$numberofunmatchedannots" | wc -l)
totalnummispelledterms2=$(($totalnummispelledterms1 - 2))
echo "Total number of annotations that need to corrected: $totalnummispelledterms1"
echo 
cp "$UNMATCHEDANNOTATIONSWITHVERSE".csv OXES_ANNOTATIONS_QA_CHECK/RESULTS/
echo "QA script finished"

#editing back weird annotation issue, so far only in 1877:
#sed -i "s/eyyâmıikâmeti/eyyâm (-ı ikâmeti)/g" ""$ABSOLUTEPATH"/workingdirectory/"$1"_pythonoutput.sfm"

#gnome-open ""$UNMATCHEDANNOTATIONSWITHVERSE".csv"
#gedit code for find/replace all footnotes
# \\f \+ \\fr [A-Z0-9]{3}\.\d+\.\d+ .+?(?=\d)\d+:\d+( |( \\ft)).*?\\f\*

##############
# logging ####
##############

} 2>&1 | tee -a "$LOGFILEOUTPUT"
#adding date stamps to logfile
cat "$LOGFILEOUTPUT" | sed -e "s/^/$(date -R) /" >> "$LOGFILEOUTPUT".log
rm -f "$LOGFILEOUTPUT"


