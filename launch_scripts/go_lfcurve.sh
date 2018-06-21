source set_env.sh

DOMAIN=$1
EXP=$2

DATE=`date +"%m_%d_%y"`
TIME=`date +"%H_%M_%S"`
LOGDIR="logs/$DATE"
mkdir -p $LOGDIR

REPORTS_DIR="reports/$DATE/${DOMAIN}_${EXP}/"
mkdir -p $REPORTS_DIR
echo "Saving reports to '$REPORTS_DIR'"
echo ""
echo "Note: If you are not starting at stage 0, confirm database exists already."

# Run tests
for ITER in 1 2 3
do
for MAX_EXP in 5 10 15 20 25 30 35 40
do

RUN="${DOMAIN}_${EXP}_${TIME}_${MAX_EXP}_${ITER}"

DB_NAME="babble_${RUN}"
echo "Using db: $DB_NAME"
cp babble_${DOMAIN}_featurized_tocopy.db $DB_NAME.db

REPORTS_SUBDIR="$REPORTS_DIR/$RUN/"
mkdir -p $REPORTS_SUBDIR
echo "Saving reports to '$REPORTS_SUBDIR'"

LOGFILE="$LOGDIR/$RUN.log"
echo "Saving log to '$LOGFILE'"
echo ""
python -u snorkel/contrib/babble/pipelines/run.py \
    --domain $DOMAIN \
    --reports_dir $REPORTS_SUBDIR \
    --db_name $DB_NAME \
    --start_at 5 \
    --max_explanations $MAX_EXP \
    --supervision majority \
    --disc_model_search_space 10 \
    --disc_model_class lstm \
    --verbose --no_plots |& tee -a $LOGFILE &
sleep 600
done
done
