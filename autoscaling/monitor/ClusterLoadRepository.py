import logging
import pydocumentdb.documents as documents
import pydocumentdb.document_client as document_client

class ClusterLoadRepository(object):
    """description of class"""
    def __init__(self, endpoint, key, database, collection, tenantId):
        self.client = document_client.DocumentClient(endpoint, {'masterKey': key})
        self.database = database
        self.collection = collection
        self.tenantId = tenantId
        self.coll_link = self.GetDocumentCollectionLink(self.database, self.collection)

    def GetDatabaseLink(self, database):
        return 'dbs/' + database

    def GetDocumentCollectionLink(self, database, collection):
        return self.GetDatabaseLink(database) + '/colls/' + collection

    def GetDocumentLink(self, database, collection, docId):
        return self.GetDocumentCollectionLink(database, collection) + '/docs/' + docId

    def UpdateDocument(self, doc):
        doc['TenantId'] = self.tenantId
        self.client.UpsertDocument(self.coll_link, doc)

    def DeleteDocument(self, doc):
        options = {}
        options['partitionkey'] = self.tenantId
        self.client.DeleteDocument(self.GetDocumentLink(self.database, self.collection, doc['id']), options)    

    def ListActiveJobs(self, queueName):
        query = 'select * from ClusterLoad l where l.TenantId=\'' + self.tenantId + '\' and l.Type=\'' + 'jobs' + '\' and l.QueueName=\'' + queueName + '\''
        logging.debug(query)
        result_iterable  = self.client.QueryDocuments(self.coll_link, query)
        results = list(result_iterable)
        return results

    def ListActiveNodes(self, queueName):
        query = 'select * from ClusterLoad l where l.TenantId=\'' + self.tenantId + '\' and l.Type=\'' + 'vms' + '\' and l.PoolName=\'' + queueName + '\''
        logging.debug(query)
        result_iterable  = self.client.QueryDocuments(self.coll_link, query)
        results = list(result_iterable)
        return results

