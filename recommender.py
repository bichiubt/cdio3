import redis
from django.conf import settings
from .models import Product, OrderItem

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

class Recommender(object):
    def get_product_key(self, id):
        return "product:{}:purchased_with".format(id)

    def products_bought(self, order_items):
        # Lấy danh sách các sản phẩm từ các món hàng trong đơn hàng
        product_ids = [item.product.id for item in order_items]
        for product_id in product_ids:
            for with_id in product_ids:
                # Lấy các sản phẩm khác đã được mua cùng với sản phẩm hiện tại
                if product_id != with_id:
                    # Tăng điểm cho sản phẩm được mua cùng nhau
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            # Nếu chỉ có một sản phẩm
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0, -1, desc=True)[:max_results]
        else:
            # Tạo một khóa tạm thời cho nhiều sản phẩm
            flat_ids = "".join([str(id) for id in product_ids])
            tmp_key = "tmp_{}".format(flat_ids)
            # Kết hợp điểm của tất cả các sản phẩm
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # Loại bỏ các sản phẩm đang được khuyến nghị khỏi danh sách gợi ý
            r.zrem(tmp_key, *product_ids)
            # Lấy các sản phẩm theo điểm (sắp xếp giảm dần)
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_results]
            # Xóa khóa tạm thời
            r.delete(tmp_key)
        
        suggested_product_ids = [int(id) for id in suggestions]

        # Lấy các sản phẩm gợi ý và sắp xếp theo thứ tự xuất hiện
        suggested_products = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        # Xóa thông tin mua hàng của tất cả sản phẩm
        for product in Product.objects.all():
            r.delete(self.get_product_key(product.id))
