from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve

# Tilga bog'liq bo'lmagan URL'lar (prefikssiz)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # set_language shu yerda
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('rosetta/', include('rosetta.urls')),  # <-- Rosetta mana bu yerga qo'shiladi
]

# Ochiq sayt: /uz/..., /ru/..., /en/...
urlpatterns += i18n_patterns(
    path('', include('main.urls')),
)

# Media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif not getattr(settings, 'USE_CLOUDINARY', False):
    # Productionda Cloudinary ishlatilmasa (masalan, media git ichida bo'lsa) fayllarni xizmat qilish
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# Static files fallback: WhiteNoise yoki collectstatic ishlamay qolsa ham CSS/JS ochiladi
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.BASE_DIR / 'static'}),
]