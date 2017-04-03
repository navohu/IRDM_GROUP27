import json

fname = "../sitegraph/graphs/trans.json"
with open(fname) as f:
    content = f.readlines()

with open("../sitegraph/graphs/trans.json") as data_file:    
    data = json.load(data_file)

print data


def makeJSON(item):
    # item = [x.strip() for x in item]
    new_item = {}
    url_remove = '{"url": '
    link_remove= ', "linkedurls"'
    return item[0]
    # for i in item:
    #     if url_remove or link_remove in i:
    #         new_item.append(i.replace(url_remove, "").replace(link_remove, ""))
    #     else:
    #         new_item.append(i)
    
    # return new_item



# print makeJSON(content)

# with open('../sitegraph/graphs/new_result.json', 'w') as fp:
#     json.dump(content, fp)