from django.contrib import admin
from django.urls import path, include
from employees.views import charts_view
from rest_framework import routers
from employees.views import EmployeeViewSet, DepartmentViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import obtain_auth_token
from performance.models import Performance

   

router = routers.DefaultRouter()
router.register(r'employees', EmployeeViewSet)
router.register(r'departments', DepartmentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Employee Management API",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # DRF router
    path("api/", include(router.urls)),

    # Token Auth
    path("api/token/", obtain_auth_token, name="api_token"),

    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),

    # Charts
    path('charts/', charts_view, name='charts'),

    # Performance API
    path('api/performance/', include('performance.urls')),

    # Attendance API
    path('api/attendance/', include('attendance.urls')),
]


from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Employee Management API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
)

# Add token auth security
swagger_security = [
    {
        "Token": []
    }
]

