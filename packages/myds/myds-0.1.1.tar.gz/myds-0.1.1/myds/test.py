import myds
url = "myds://ml.category.cifar10/../mnist"

q=myds.HttpQuerier()
print(q.getQueryUrl(url))
print(myds.HttpQuerier().query(url))

print(myds.getDb(dbName='ml.category.cifar10',port=5149,charset='UTF-8'))