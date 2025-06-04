from database.DB_connect import DBConnect
from model.dtos import Store, Ordine

class DAO():
    def __init__(self):
        pass

    @staticmethod
    def _getAllStores():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            query = f"""SELECT * from stores"""
            cursor.execute(query)
            result = []
            for row in cursor.fetchall():
                result.append(Store(**row))
            return result

        finally:
            cnx.close()
            cursor.close()

    @staticmethod
    def _getAllNodes(store_id):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            query = f"""SELECT * FROM orders WHERE store_id = %s"""
            cursor.execute(query, (store_id,))
            result = []
            for row in cursor.fetchall():
                result.append(Ordine(**row))
            return result

        finally:
            cnx.close()
            cursor.close()

    @staticmethod
    def _getAllEdges(store, k):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            query = f"""select of1.order_id as source, of2.order_id as target, of1.tot+of2.tot as weight
                        from   (select o.order_id as order_id , sum(oi.quantity) as tot, o.order_date as order_date
                                from orders o , order_items oi 
                                where o.order_id = oi.order_id and o.store_id = %s
                                group by o.order_id) of1,
                               (select o1.order_id as order_id , sum(oi1.quantity) as tot, o1.order_date as order_date
                                from orders o1 , order_items oi1 
                                where o1.order_id = oi1.order_id and o1.store_id = %s
                                group by o1.order_id) of2
                        where of1.order_id != of2.order_id and of1.order_date > of2.order_date and
                        DATEDIFF(of1.order_date, of2.order_date) < %s"""
            cursor.execute(query, (store, store, k))
            result = []
            for row in cursor:
                result.append(row)
            return result

        finally:
            cnx.close()
            cursor.close()
