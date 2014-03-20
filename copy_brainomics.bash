cubes="brainomics questionnaire neuroimaging genomics medicalexp card bootstrap comment jqplot file"

brainomics_tag="cubicweb-brainomics-debian-version-0.8.0"
questionnaire_tag="cubicweb-questionnaire-debian-version-0.5.0"
neuroimaging_tag="cubicweb-neuroimaging-debian-version-0.5.0"
genomics_tag="cubicweb-genomics-debian-version-0.7.0"
medicalexp_tag="cubicweb-medicalexp-debian-version-0.8.0"
card_tag="cubicweb-card-debian-version-0.5.3-1"
bootstrap_tag="cubicweb-bootstrap-debian-version-0.6.0-1"
comment_tag="cubicweb-comment-debian-version-1.10.0-1"
jqplot_tag="cubicweb-jqplot-debian-version-0.4.0-1"
file_tag="cubicweb-file-debian-version-1.16.0-1"

dest="$PWD"
tmp=`mktemp --directory`
for cube in $cubes; do
    echo "---------- $cube ----------"
    hg --cwd "$tmp" clone http://hg.logilab.org/review/cubes/$cube
    v=$cube_tag
    hg --cwd "$tmp/$cube" update "${!v}"
    hg --cwd "$tmp/$cube" archive "$dest/$cube"
done
rm -Rf "$tmp"
