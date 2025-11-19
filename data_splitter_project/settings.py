import os

# Configuración para Render
if 'RENDER' in os.environ:
    # Configuración de producción
    DEBUG = False
    ALLOWED_HOSTS = ['your-app-name.onrender.com', 'localhost', '127.0.0.1']
    
    # Configuración de base de datos para Render
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600
        )
    }
    
    # Configuración de archivos estáticos
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Middleware para WhiteNoise
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        # ... el resto de tus middlewares
    ]
else:
    # Configuración de desarrollo
    DEBUG = True
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
