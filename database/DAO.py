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
            query = f"""select o1.order_id as source, o2.order_id as target, sum(oi1.quantity)+sum(oi2.quantity) as weight
                        from orders o1, orders o2, order_items oi1, order_items oi2
                        where o2.store_id = o1.store_id and o1.order_id != o2.order_id
                            and o1.order_id = oi1.order_id and o2.order_id = oi2.order_id
                            and o1.order_date > o2.order_date
                            and o1.store_id = %s and DATEDIFF(o1.order_date, o2.order_date) < %s
                        group by o1.order_id, o2.order_id"""
            cursor.execute(query, (store, k))
            result = []
            for row in cursor:
                result.append(row)
            return result

        finally:
            cnx.close()
            cursor.close()
