DOMAIN=$1
EXP=$2
PROJECT="qalf"
RELATION="org_top_members_employees"

DATE=`date +"%m_%d_%y"`
TIME=`date +"%H_%M_%S"`

LOGDIR="logs/$DATE"
mkdir -p $LOGDIR

REPORTS_DIR="reports/$DATE"
mkdir -p $REPORTS_DIR

echo ""
echo "<TEST:>"
echo ""

for MAX_TRAIN in 8000
do
for ITER in 1 2 3
do

RUN="${PROJECT}_${DOMAIN}_${EXP}_${TIME}_${MAX_TRAIN}_${ITER}"

BASE_DB="${PROJECT}_${DOMAIN}_${RELATION}"
DB_NAME=$RUN
cp $BASE_DB.db $DB_NAME.db
echo "Copying db: $BASE_DB.db"
echo "Using db: $DB_NAME.db"

REPORTS_SUBDIR="$REPORTS_DIR/$RUN/"
mkdir -p $REPORTS_SUBDIR
echo "Saving reports to '$REPORTS_SUBDIR'"

LOGFILE="$LOGDIR/$RUN.log"
echo "Saving log to '$LOGFILE'"

python -u snorkel/contrib/pipelines/run.py \
    --domain $DOMAIN \
    --project $PROJECT \
    --relation $RELATION \
    --db_name $DB_NAME \
    --reports_dir $REPORTS_SUBDIR \
    --start_at 7 \
    --end_at 10 \
    --supervision traditional \
    --max_train $MAX_TRAIN \
    --disc_model_search_space 10 \
    --verbose --no_plots |& tee -a $LOGFILE &

sleep 3

done
done
