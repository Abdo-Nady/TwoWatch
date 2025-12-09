هديك **PLAN عملية واضحة** تمشي عليها خطوة بخطوة، من غير كلام زائد، بحيث في النهاية يبقى معك Backend نظيف بـ DRF + JWT + Sharing Feature.
الخطة فيها مراحل، وكل مرحلة لها هدف ونتيجة واضحة.
خلينا نمشي بمنهجية: **Architecture → Core Models → Auth → API → Sharing → Testing → Deploy**

---

# 🟢 المرحلة 0 — Setup & Architecture (يوم واحد)

## 🎯 الهدف

تأسيس المشروع بطريقة صحيحة قبل الكود.

## ✔️ الخطوات

1. تحديد الـ features الأساسية:

   * Users / Auth
   * Movies
   * Watchlist (Private)
   * Shared Watchlist (Couple Mode)

2. اختيار الـ stack:

   * Django + DRF
   * PostgreSQL
   * SimpleJWT
   * Swagger

3. رسم ERD بسيط:

```
User
SharedWatchlist
Movie
WatchlistItem
Rating (optional later)
```

4. إنشاء المشروع:

```
django-admin startproject watchlist
cd watchlist
django-admin startapp accounts
django-admin startapp movies
```

> **نتيجة المرحلة:** عندك مشروع جاهز، Apps جاهزة، صورة واضحة.

---

# 🟢 المرحلة 1 — Auth System (يوم)

## 🎯 الهدف

تجهيز الـ User Management كامل.

## ✔️ الخطوات

1. استخدام Django default User
2. endpoints:

   * /auth/register
   * /auth/login (JWT)
   * /auth/me
3. install/config:

   * djangorestframework
   * simplejwt
4. Permissions أساسية:

   * IsAuthenticated

> **نتيجة:** User يقدر يعمل register + login + يحصل على token.

---

# 🟢 المرحلة 2 — Movies Module (يومين)

## 🎯 الهدف

إدارة الأفلام + Data model صح.

## ✔️ Model

```
Movie:
- title
- description
- release_year
- poster_url
- imdb_url
- created_at
```

## ✔️ API

* GET /movies
* GET /movies/:id
* POST /movies (admin later)
* Search by title
* Filter by year, category (optional later)

> **نتيجة:** Movie CRUD جاهز.

---

# 🟢 المرحلة 3 — Watchlist (Private Mode) (يومين)

## 🎯 الهدف

الفكرة الأساسية بدون sharing.

## ✔️ Model

```
WatchlistItem:
- user (FK)
- movie (FK)
- status (enum)
- rating (optional)
- notes
- added_at
```

### Status enum:

* TO_WATCH
* WATCHED
* DROPPED

## ✔️ API

* GET /watchlist
* POST /watchlist
* PATCH /watchlist/:id (change status)
* DELETE /watchlist/:id

## ✔️ Filters

* /watchlist?status=TO_WATCH

> **نتيجة:** User عنده قائمة أفلام كاملة.

---

# 🟢 المرحلة 4 — Sharing Feature (3 أيام)

## 🎯 الهدف

Shared watchlist بين شخصين.

## ✔️ Model

```
SharedWatchlist:
- user_1
- user_2
- created_at
```

### تعديل WatchlistItem:

بدل user الواحد:

```
WatchlistItem:
- user (nullable)
- shared_watchlist (nullable)
```

2 modes:

* Private mode: user != NULL
* Shared mode: shared_watchlist != NULL

## ✔️ API

* POST /shared/create (invite)
* POST /shared/accept
* GET /shared/:id/watchlist
* POST /shared/:id/add
* PATCH /shared/:id/:item_id (change status)

## ✔️ Permissions

* Allow فقط user_1 أو user_2
* منع user غريب يدخل القائمة

> **نتيجة:** اتنين يضيفوا/يعدلوا نفس القائمة.

---

# 🟢 المرحلة 5 — Recommendation Engine (اختياري لاحقًا)

## 🎯 الهدف

اقتراحات بسيطة بناءً على History.

## ✔️ Logic بسيط

* أعلى Genres تم تقييمها
* أفلام مشابهة
* Random pick من Genre محبوب

> **نتيجة:** Feature ممتعة لكن مش ضرورية للـ MVP.

---

# 🟢 المرحلة 6 — Documentation (يوم)

## 🎯 الهدف

توثيق كامل للـ API.

## ✔️ أدوات

* drf_yasg أو drf-spectacular (Swagger)
* Postman Collection
* README:

  * Auth flow
  * Endpoints
  * Models

> **نتيجة:** Backend جاهز للاستخدام.

---

# 🟢 المرحلة 7 — Testing (يومين)

## 🎯 الهدف

تتعلم Testing في DRF.

## ✔️ أنواع الاختبارات

* Unit Tests:

  * Movies
  * Watchlist
  * Auth

* Permission Tests:

  * Shared watchlist only for couple

> **نتيجة:** testing يضمن جودة الكود.

---

# 🟢 المرحلة 8 — Deployment (يومين)

## 🎯 الهدف

رفع المشروع على الإنترنت.

## ✔️ خطوات

* Dockerfile
* docker-compose (DB + App)
* Deploy على VPS أو Render/GCP
* .env variables
* HTTPS

> **نتيجة:** تطبيق شغال Online (API ready).

---

# 🟣 ملخص الـ Plan (Timeline)

| مرحلة        | أيام       |
| ------------ | ---------- |
| Architecture | 1          |
| Auth         | 1          |
| Movies       | 2          |
| Watchlist    | 2          |
| Sharing      | 3          |
| Docs         | 1          |
| Testing      | 2          |
| Deploy       | 2          |
| **الإجمالي** | **14 يوم** |

لو ضغطتها من غير Testing واختصارات:
**7–9 أيام**.

---

# 🧠 Tips أثناء العمل

## Structure

```
/watchlist
  accounts/
    serializers.py
    views.py
    urls.py
  movies/
    serializers.py
    views.py
    urls.py
  watchlist/
    models.py
    ...
  utils/
```

## لا تبدأ Frontend الآن

ركز في الـ API
ولما تبقى جاهز، React يبقى بسيط جدًا.

---

# 🎯 طريقة التنفيذ المثالية للتعلم

ابدأ من تحت لفوق:

1. ERD
2. Models
3. Serializers
4. Views/Viewsets
5. Permissions
6. URLs
7. Tests
8. Docs

الـ Sharing Feature هي اللي هتعلمك:

* Relations مركبة
* Permissions صح
* Logic
* Filters

---

لو موافق، نبدأ المرحلة الأولى:
**نرسم ERD بالتفصيل ونكتبها clean قبل الكود.**
قولّي: تحب نرسم ERD نصيًا ولا Diagram؟
