from google.appengine.ext import db

def make_seq(lst, n=3):
    seq_total = []
    seq_temp = []

    for s in range(n):
        seq_total.append(list())
    for i in lst:
        seq_temp.append(i)

    new_list = []
    old_list = seq_temp

    while (len(old_list) > 0):
        max_count = -100
        for data in old_list:
            num_data = db.get(data.key())
            if max_count < num_data.count_plus - num_data.count_minus:
                max_count = num_data.count_plus - num_data.count_minus
                max_tweet = data
        new_list.append(max_tweet)
        old_list.remove(max_tweet)
    seq_temp = new_list[:]

    while len(seq_temp) > 0:
        try:
            for s in range(n):
                seq_total[s].append(seq_temp.pop(0))
        except:
            pass

    return seq_total


def make_msg(lst, n=3):
    msg_total = []
    for s in range(n):
        msg_total.append(list())
        for i in lst[s]:
            uploaded = db.get(i.key())
            msg_total[s].append(uploaded.text)
    return msg_total


def make_p_n(lst, n=3):
    p_n_total = []
    for s in range(n):
        p_n_total.append(list())
        for i in lst[s]:
            uploaded = db.get(i.key())
            p_n_total[s].append(uploaded.count_plus)
    return p_n_total

def make_m_n(lst, n=3):
    m_n_total = []
    for s in range(n):
        m_n_total.append(list())
        for i in lst[s]:
            uploaded = db.get(i.key())
            m_n_total[s].append(uploaded.count_minus)
    return m_n_total

