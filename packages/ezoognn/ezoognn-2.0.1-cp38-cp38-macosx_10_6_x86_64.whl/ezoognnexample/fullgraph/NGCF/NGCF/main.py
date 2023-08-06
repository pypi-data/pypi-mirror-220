from ezoognn.loader.dataset.gowalla_ezoo_data_graph import GowallaEzooGraphDataset, EzooShapeGraphEnum
from ezoognnexample.fullgraph.NGCF.NGCF.utility import metrics
from ezoognnexample.fullgraph.NGCF.NGCF.utility.parser_ngcf import parse_args
from ezoognnexample.fullgraph.NGCF.NGCF.utility.load_data import *
from ezoognnexample.fullgraph.NGCF.NGCF.utility.helper import early_stopping
from ezoognnexample.fullgraph.NGCF.NGCF.model import NGCF
import torch.optim as optim
import torch
from ezoognn.nni.nni_params_handler import MetricsReporter
import heapq
import multiprocessing
from time import time
import numpy as np
import os


def ranklist_by_heapq(user_pos_test, test_items, rating, Ks):
    item_score = {}
    for i in test_items:
        item_score[i] = rating[i]

    K_max = max(Ks)
    K_max_item_score = heapq.nlargest(K_max, item_score, key=item_score.get)

    r = []
    for i in K_max_item_score:
        if i in user_pos_test:
            r.append(1)
        else:
            r.append(0)
    auc = 0.0
    return r, auc


def get_auc(item_score, user_pos_test):
    item_score = sorted(item_score.items(), key=lambda kv: kv[1])
    item_score.reverse()
    item_sort = [x[0] for x in item_score]
    posterior = [x[1] for x in item_score]

    r = []
    for i in item_sort:
        if i in user_pos_test:
            r.append(1)
        else:
            r.append(0)
    auc = metrics.auc(ground_truth=r, prediction=posterior)
    return auc


def ranklist_by_sorted(user_pos_test, test_items, rating, Ks):
    item_score = {}
    for i in test_items:
        item_score[i] = rating[i]

    K_max = max(Ks)
    K_max_item_score = heapq.nlargest(K_max, item_score, key=item_score.get)

    r = []
    for i in K_max_item_score:
        if i in user_pos_test:
            r.append(1)
        else:
            r.append(0)
    auc = get_auc(item_score, user_pos_test)
    return r, auc


def get_performance(user_pos_test, r, auc, Ks):
    precision, recall, ndcg, hit_ratio = [], [], [], []

    for K in Ks:
        precision.append(metrics.precision_at_k(r, K))
        recall.append(metrics.recall_at_k(r, K, len(user_pos_test)))
        ndcg.append(metrics.ndcg_at_k(r, K))
        hit_ratio.append(metrics.hit_at_k(r, K))

    return {
        "recall": np.array(recall),
        "precision": np.array(precision),
        "ndcg": np.array(ndcg),
        "hit_ratio": np.array(hit_ratio),
        "auc": auc,
    }


def test_one_user(x):
    # user u's ratings for user u
    rating = x[0]
    # uid
    u = x[1]
    # user u's items in the training set
    try:
        training_items = data_generator.train_items[u]
    except Exception:
        training_items = []
    # user u's items in the test set
    user_pos_test = data_generator.test_set[u]

    all_items = set(range(ITEM_NUM))

    test_items = list(all_items - set(training_items))

    if g_args.test_flag == "part":
        r, auc = ranklist_by_heapq(user_pos_test, test_items, rating, Ks)
    else:
        r, auc = ranklist_by_sorted(user_pos_test, test_items, rating, Ks)

    return get_performance(user_pos_test, r, auc, Ks)


def test(model, g, users_to_test, batch_test_flag=False):
    result = {
        "precision": np.zeros(len(Ks)),
        "recall": np.zeros(len(Ks)),
        "ndcg": np.zeros(len(Ks)),
        "hit_ratio": np.zeros(len(Ks)),
        "auc": 0.0,
    }

    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(cores)

    u_batch_size = 5000
    i_batch_size = BATCH_SIZE

    test_users = users_to_test
    n_test_users = len(test_users)
    n_user_batchs = n_test_users // u_batch_size + 1

    count = 0

    for u_batch_id in range(n_user_batchs):
        start = u_batch_id * u_batch_size
        end = (u_batch_id + 1) * u_batch_size

        user_batch = test_users[start:end]

        if batch_test_flag:
            # batch-item test
            n_item_batchs = ITEM_NUM // i_batch_size + 1
            rate_batch = np.zeros(shape=(len(user_batch), ITEM_NUM))

            i_count = 0
            for i_batch_id in range(n_item_batchs):
                i_start = i_batch_id * i_batch_size
                i_end = min((i_batch_id + 1) * i_batch_size, ITEM_NUM)

                item_batch = range(i_start, i_end)

                u_g_embeddings, pos_i_g_embeddings, _ = model(
                    g, "user", "item", user_batch, item_batch, []
                )
                i_rate_batch = (
                    model.rating(u_g_embeddings, pos_i_g_embeddings)
                    .detach()
                    .cpu()
                )

                rate_batch[:, i_start:i_end] = i_rate_batch
                i_count += i_rate_batch.shape[1]

            assert i_count == ITEM_NUM

        else:
            # all-item test
            item_batch = range(ITEM_NUM)
            u_g_embeddings, pos_i_g_embeddings, _ = model(
                g, "user", "item", user_batch, item_batch, []
            )
            rate_batch = (
                model.rating(u_g_embeddings, pos_i_g_embeddings).detach().cpu()
            )

        user_batch_rating_uid = zip(rate_batch.numpy(), user_batch)
        batch_result = pool.map(test_one_user, user_batch_rating_uid)
        count += len(batch_result)

        for re in batch_result:
            result["precision"] += re["precision"] / n_test_users
            result["recall"] += re["recall"] / n_test_users
            result["ndcg"] += re["ndcg"] / n_test_users
            result["hit_ratio"] += re["hit_ratio"] / n_test_users
            result["auc"] += re["auc"] / n_test_users

    assert count == n_test_users
    pool.close()
    return result


def set_global_var(in_args, in_ks, in_item_num, in_batch_size, in_data_generator):
    global g_args
    g_args = in_args
    global Ks
    Ks = in_ks
    global ITEM_NUM
    ITEM_NUM = in_item_num
    global BATCH_SIZE
    BATCH_SIZE = in_batch_size
    global data_generator
    data_generator = in_data_generator


def main(args):
    # Step 1: Prepare graph data and device ================================================================= #
    if args.gpu >= 0 and torch.cuda.is_available():
        device = "cuda:{}".format(args.gpu)
    else:
        device = "cpu"

    g = data_generator.g
    g = g.to(device)

    # Step 2: Create model and training components=========================================================== #
    model = NGCF(
        g, args.embed_size, args.layer_size, args.mess_dropout, args.regs[0]
    ).to(device)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)

    # Step 3: training epoches ============================================================================== #
    n_batch = data_generator.n_train // args.batch_size + 1
    t0 = time()
    cur_best_pre_0, stopping_step = 0, 0
    loss_loger, pre_loger, rec_loger, ndcg_loger, hit_loger = [], [], [], [], []
    for epoch in range(args.epoch):
        t1 = time()
        loss, mf_loss, emb_loss = 0.0, 0.0, 0.0
        for idx in range(n_batch):
            users, pos_items, neg_items = data_generator.sample()
            u_g_embeddings, pos_i_g_embeddings, neg_i_g_embeddings = model(
                g, "user", "item", users, pos_items, neg_items
            )

            batch_loss, batch_mf_loss, batch_emb_loss = model.create_bpr_loss(
                u_g_embeddings, pos_i_g_embeddings, neg_i_g_embeddings
            )
            optimizer.zero_grad()
            batch_loss.backward()
            optimizer.step()

            loss += batch_loss
            mf_loss += batch_mf_loss
            emb_loss += batch_emb_loss

        if (epoch + 1) % 10 != 0:
            if args.verbose > 0 and epoch % args.verbose == 0:
                perf_str = "Epoch %d [%.1fs]: train==[%.5f=%.5f + %.5f]" % (
                    epoch,
                    time() - t1,
                    loss,
                    mf_loss,
                    emb_loss,
                )
                print(perf_str)
            continue  # end the current epoch and move to the next epoch, let the following evaluation run every 10 epoches

        # evaluate the model every 10 epoches
        t2 = time()
        users_to_test = list(data_generator.test_set.keys())
        users_to_test = [int(x) for x in users_to_test]
        ret = test(model, g, users_to_test)
        t3 = time()

        loss_loger.append(loss)
        rec_loger.append(ret["recall"])
        pre_loger.append(ret["precision"])
        ndcg_loger.append(ret["ndcg"])
        hit_loger.append(ret["hit_ratio"])
        MetricsReporter.report_intermediate_result(ret["precision"])
        if args.verbose > 0:
            perf_str = (
                "Epoch %d [%.1fs + %.1fs]: train==[%.5f=%.5f + %.5f], recall=[%.5f, %.5f], "
                "precision=[%.5f, %.5f], hit=[%.5f, %.5f], ndcg=[%.5f, %.5f]"
                % (
                    epoch,
                    t2 - t1,
                    t3 - t2,
                    loss,
                    mf_loss,
                    emb_loss,
                    ret["recall"][0],
                    ret["recall"][-1],
                    ret["precision"][0],
                    ret["precision"][-1],
                    ret["hit_ratio"][0],
                    ret["hit_ratio"][-1],
                    ret["ndcg"][0],
                    ret["ndcg"][-1],
                )
            )
            print(perf_str)

        cur_best_pre_0, stopping_step, should_stop = early_stopping(
            ret["recall"][0],
            cur_best_pre_0,
            stopping_step,
            expected_order="acc",
            flag_step=100,
        )

        # early stop
        if should_stop == True:
            break

        if ret["recall"][0] == cur_best_pre_0 and args.save_flag == 1:
            torch.save(model.state_dict(), args.weights_path + args.model_name)
            print(
                "save the weights in path: ",
                args.weights_path + args.model_name,
            )

    recs = np.array(rec_loger)
    pres = np.array(pre_loger)
    ndcgs = np.array(ndcg_loger)
    hit = np.array(hit_loger)

    MetricsReporter.report_final_result(pres)

    best_rec_0 = max(recs[:, 0])
    idx = list(recs[:, 0]).index(best_rec_0)

    final_perf = (
        "Best Iter=[%d]@[%.1f]\trecall=[%s], precision=[%s], hit=[%s], ndcg=[%s]"
        % (
            idx,
            time() - t0,
            "\t".join(["%.5f" % r for r in recs[idx]]),
            "\t".join(["%.5f" % r for r in pres[idx]]),
            "\t".join(["%.5f" % r for r in hit[idx]]),
            "\t".join(["%.5f" % r for r in ndcgs[idx]]),
        )
    )
    print(final_perf)

    return best_rec_0

# Open the file for writing


if __name__ == "__main__":
    args = parse_args()
    if args.ezoo_fullgraph is not None and args.ezoo_fullgraph:
        data_generator = GowallaEzooGraphDataset(cfg_file=args.cfg_file)[
            EzooShapeGraphEnum.WHOLE]
        data_generator.batch_size = args.batch_size
    else:
        data_generator = Data(
            path=args.data_path + args.dataset, batch_size=args.batch_size
        )

    Ks = eval(args.Ks)

    ITEM_NUM = data_generator.n_items
    BATCH_SIZE = args.batch_size

    set_global_var(args, Ks, ITEM_NUM, BATCH_SIZE, data_generator)

    if not os.path.exists(args.weights_path):
        os.mkdir(args.weights_path)
    args.mess_dropout = eval(args.mess_dropout)
    args.layer_size = eval(args.layer_size)
    args.regs = eval(args.regs)
    print(args)
    main(args)
