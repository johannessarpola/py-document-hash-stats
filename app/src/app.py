from app.src import input_output, logger_factory
from app.src.util import Stopwarch
from app.src.adapter import document_hashes_from_jsons, aggregate_stats_to_json
from app.src.models import DocumentProcessingStats, DocumentHash, DocumentProcessingAggregateStats
from concurrent.futures import ThreadPoolExecutor
import os
from app.src.aggregation import group_by_attribute

log_factory = logger_factory.LoggerFactory()
app_logger = log_factory.instance(__name__)


def hash_to_stats(document_hash: DocumentHash):
    prior_features = document_hash.original().split(' ')
    after_features = document_hash.content.split(' ')
    return DocumentProcessingStats(document_hash.id, after_features, prior_features, document_hash.category())


def average_reduction_in_stat_lst(lst, pool: ThreadPoolExecutor):
    return sum(list(pool.map(lambda s: 1 - s.num_features_after_processing / s.num_features_prior_processing, lst))) / len(
        lst)


def average_reduction_in_stat_lst_by_cat(by_cats, pool: ThreadPoolExecutor):
    futs = {}
    for k, v in by_cats.items():
        futs[k] = pool.submit(average_reduction_in_stat_lst, v, pool)
    avg_reduc = {}
    for c, f in futs.items():
        avg_reduc[c] = f.result()
    return avg_reduc


def aggregate_stats( id, stat_list, pool: ThreadPoolExecutor):
    taf = set()
    tpf = set()
    if pool is not None:
        taf_sets = list(pool.map(lambda stat: stat.unique_features_after_processing(), stat_list))
        tpf_sets = list(pool.map(lambda stat: stat.unique_features_prior_processing(), stat_list))
        pool.map(lambda lst: taf.update(lst), taf_sets)
        pool.map(lambda lst: tpf.update(lst), tpf_sets)

    by_cats = group_by_attribute(stat_list, 'category')
    reduction_by_cats = average_reduction_in_stat_lst_by_cat(by_cats, pool)

    aggr_stats = DocumentProcessingAggregateStats(id, stat_list, len(tpf), len(taf), reduction_by_cats)
    return aggr_stats


def evaluate_futures(futs):
    res = []
    for f in futs:
        res.append(f.result())
    return res


def measure_hashes(id, document_hashes):
    pool = ThreadPoolExecutor(max_workers=10)
    futures = []
    for dh in document_hashes:
        f = pool.submit(hash_to_stats, dh)
        futures.append(f)
    stats = evaluate_futures(futures)
    return aggregate_stats(id, stats, pool)


def main(input, output, input_id = None):
    sw = Stopwarch().and_start()

    out_f = os.path.dirname(output)
    if not os.path.exists(out_f):
        os.makedirs(out_f)

    jsons = input_output.get_jsons_from_folder(input)
    iter = 0
    for json in jsons:
        document_hashes = document_hashes_from_jsons(json)
        if input_id is None:
            id = f"{os.path.basename(os.path.normpath(input))}_{iter}"
        else:
            id = f"{input_id}_{iter}"
        aggregate_stats = measure_hashes(id, document_hashes)
        iter += 1
        aggregate_stats_json_strs = aggregate_stats_to_json(aggregate_stats)
        input_output.write_and_close(os.path.join(out_f, f"{id}.json"), aggregate_stats_json_strs)

    duration, unit = sw.time_with_unit()
    app_logger.info(f"Main took {duration} {unit}")
