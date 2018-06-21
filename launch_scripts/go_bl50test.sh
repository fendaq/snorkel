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

#echo "Make starter db..."
#python -u snorkel/contrib/babble/pipelines/run.py \
#    --domain $DOMAIN \
#    --db_name babble_${DOMAIN}_bl50_featurized_tocopy \
#    --start_at 0 \
#    --end_at 5 \
#    --BL50_test true \
#    --supervision majority \
#    --verbose --no_plots


# Run tests
for ITER in 1 2 3 4 5
do

RUN="${DOMAIN}_${EXP}_${TIME}_${ITER}"

DB_NAME="babble_${RUN}"
echo "Using db: $DB_NAME"
cp babble_${DOMAIN}_bl50_featurized_tocopy.db $DB_NAME.db

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
    --start_at 0 \
    --max_explanations 30 \
    --BL50_test true \
    --supervision majority \
    --disc_model_search_space 10 \
    --disc_model_class lstm \
    --verbose --no_plots |& tee -a $LOGFILE &
sleep 3
done

