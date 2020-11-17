from easyshop.viewsets import ProductViewset
from rest_framework import routers



router = routers.DefaultRouter()
router.register('products',viewset=ProductViewset)

# localhost:p/api/employee/5
# GET, POST, PUT, DELETE
# list , retrive