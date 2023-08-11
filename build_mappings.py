from collections import defaultdict, Counter

users = defaultdict(lambda: len(users) + 1)
items = defaultdict(lambda: len(items) + 1)

item_counter = Counter() 

for line in open ("ratings.dat"):
    res = line.strip().split("::")
    item_id = res[1]
    user_id = res[0]
    item_counter[item_id] += 1

users_counter = Counter()    
user_items = defaultdict(list)
user_item_interaction_time = defaultdict(dict)

for line in open ("ratings.dat"):
    res = line.strip().split("::")
    item_id_raw = res[1]
    user_id_raw = res[0]
    timestamp = res[3]
    if item_counter[item_id_raw] >= 5:
        users_counter[user_id_raw] += 1
        user_items[user_id_raw].append(item_id_raw)
        user_item_interaction_time[user_id_raw][item_id_raw] = timestamp

item_users = defaultdict(list)

cnt = 0 
for line in open ("ratings.dat"):
    res = line.strip().split("::")
    item_id_raw = res[1]
    user_id_raw = res[0]
    timestamp = res[3]
    if item_counter[item_id_raw] >= 5:
        item_users[item_id_raw].append(users_counter[user_id_raw])
        cnt +=1 

mapping = {} 
for item in item_users:
    item_users[item].sort()
    item_users_key = "_".join(str(cnt) for cnt in item_users[item])
    mapping[item_users_key] = item

key2user = {} 
for user in user_items:
    user_items[user].sort()
    user_items_key = "_".join(str(item) for item in user_items[user])
    key2user[user_items_key] = user

users_counter_sas = Counter()
cnt_sas = 0
for line in open ("ml-1m_sas.txt"):
    res = line.strip().split(" ")
    item_id = res[1]
    user_id = res[0]
    users_counter_sas[user_id] += 1
    cnt_sas += 1

item_users_sas = defaultdict(list)
for line in open ("ml-1m_sas.txt"):
    res = line.strip().split(" ")
    item_id_raw = res[1]
    user_id_raw = res[0]
    item_users_sas[item_id_raw].append(users_counter_sas[user_id_raw])

sas_to_original = {}
with open("sas_to_original_items.txt", "w") as out: 
    for item in item_users_sas:
        item_users_sas[item].sort()
        item_users_key = "_".join(str(cnt) for cnt in item_users_sas[item])
        out.write(f"{item} {mapping[item_users_key]}\n")
        sas_to_original[item] = mapping[item_users_key]

user_items_sas = defaultdict(list)
for line in open ("ml-1m_sas.txt"):
    res = line.strip().split(" ")
    item_id_original = sas_to_original[res[1]]
    user_id_raw = res[0]
    user_items_sas[user_id_raw].append(item_id_original)

sas_users_to_original = {}
with open("sas_to_original_users.txt", "w") as out: 
    for user in user_items_sas:
        user_items_sas[user].sort()
        user_items_key = "_".join(str(item) for item in user_items_sas[user])
        out.write(f"{user} {key2user[user_items_key]}\n")
        sas_users_to_original[user] = key2user[user_items_key]

with open("decoded.csv", "w") as out:
    out.write("sas_user_id;sas_item_id;original_user_id;original_item_id;timestamp\n")
    for line in open ("ml-1m_sas.txt"):
        res = line.strip().split(" ")
        item_id = res[1]
        user_id = res[0]
        users_counter_sas[user_id] += 1
        cnt_sas += 1
        item_id_original = sas_to_original[item_id]
        user_id_original = sas_users_to_original[user_id]
        out.write(f"{user_id};{item_id};{user_id_original};{item_id_original};{user_item_interaction_time[user_id_original][item_id_original]}\n")
