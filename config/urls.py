from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

# Tilga bog'liq bo'lmagan URL'lar (prefikssiz)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # set_language shu yerda
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('rosetta/', include('rosetta.urls')),  # <-- Rosetta mana bu yerga qo'shiladi
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Ochiq sayt: /uz/..., /ru/..., /en/...
urlpatterns += i18n_patterns(
    path('', include('main.urls')),
)