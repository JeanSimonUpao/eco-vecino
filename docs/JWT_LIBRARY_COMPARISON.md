# SP-001: Comparativa de Librerías JWT para FastAPI

## Contexto

Para el sistema Eco-Vecino necesitamos autenticación segura basada en JWT (JSON Web Tokens). Se evaluaron las principales opciones del ecosistema Python/FastAPI.

---

## Librerías Evaluadas

### 1. `python-jose[cryptography]`

| Criterio | Detalle |
|---|---|
| **Mantenimiento** | Activo — última release 2023 |
| **Algoritmos** | HS256, RS256, ES256 y más |
| **Integración FastAPI** | Nativa — es la librería oficial en la doc de FastAPI |
| **Dependencias** | `cryptography` (estándar en la industria) |
| **Facilidad de uso** | Alta — API simple para encode/decode |
| **Seguridad** | Alta — soporta expiración, claims personalizados |

```python
from jose import JWTError, jwt

token = jwt.encode({"sub": "user@mail.com", "exp": ...}, SECRET_KEY, algorithm="HS256")
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

---

### 2. `PyJWT`

| Criterio | Detalle |
|---|---|
| **Mantenimiento** | Muy activo — release frecuentes |
| **Algoritmos** | HS256, RS256, PS256, ES256 |
| **Integración FastAPI** | Manual — requiere más boilerplate |
| **Dependencias** | Mínimas |
| **Facilidad de uso** | Media — API ligeramente diferente |
| **Seguridad** | Alta |

```python
import jwt

token = jwt.encode({"sub": "user@mail.com"}, SECRET_KEY, algorithm="HS256")
payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

---

### 3. `authlib`

| Criterio | Detalle |
|---|---|
| **Mantenimiento** | Muy activo |
| **Algoritmos** | Soporte completo OAuth2, OpenID |
| **Integración FastAPI** | Requiere configuración OAuth2 completa |
| **Dependencias** | Pesada — diseñada para OAuth2 completo |
| **Facilidad de uso** | Baja para casos simples de JWT |
| **Seguridad** | Muy alta |

---

## Tabla Comparativa

| Criterio | python-jose | PyJWT | authlib |
|---|---|---|---|
| Facilidad FastAPI | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Documentación oficial FastAPI | ✅ Sí | ❌ No | ❌ No |
| Peso/dependencias | Ligera | Muy ligera | Pesada |
| Algoritmos soportados | Suficientes | Suficientes | Extensos |
| Curva de aprendizaje | Baja | Baja | Alta |
| Adecuado para MVP | ✅ Sí | ✅ Sí | ❌ Exceso |

---

## ✅ Decisión: `python-jose[cryptography]`

**Justificación:**

1. **Es la librería recomendada oficialmente en la documentación de FastAPI** — garantiza compatibilidad total con los patrones `OAuth2PasswordBearer` y `Depends`.
2. **Menor curva de aprendizaje** para el equipo — API intuitiva y ejemplos directamente aplicables.
3. **Suficiente para el alcance del MVP** — no necesitamos OAuth2 completo ni SSO por ahora.
4. **Integración con `passlib[bcrypt]`** para hash de contraseñas es directa y está documentada.

### Configuración adoptada:
- **Algoritmo:** `HS256` (simétrico, suficiente para backend monolítico)
- **Expiración:** 30 minutos (configurable vía `.env`)
- **Hash de contraseñas:** `passlib` con `bcrypt`

---

## Referencias

- [FastAPI Security - JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [python-jose GitHub](https://github.com/mpdavis/python-jose)
- [PyJWT Docs](https://pyjwt.readthedocs.io/)
