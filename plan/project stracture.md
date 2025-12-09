watchlist_project/
│
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── accounts/
│   ├── models.py        # User + Profile
│   ├── serializers.py
│   ├── views.py         # signup/login/profile
│   ├── urls.py
│   ├── permissions.py   # IsOwner
│   ├── tests/
│   └── admin.py
│
├── movies/
│   ├── models.py        # Movie
│   ├── serializers.py
│   ├── views.py         # Movie search + list
│   ├── urls.py
│   ├── admin.py
│   └── tests/
│
├── watchlists/
│   ├── models.py        # Watchlist + Item + Member
│   ├── serializers.py
│   ├── views.py         # CRUD + invite
│   ├── urls.py
│   ├── permissions.py
│   ├── signals.py
│   ├── admin.py
│   └── tests/
│
├── notifications/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── signals.py
│   ├── admin.py
│   └── tests/
│
└── core/
    ├── utils.py
    ├── pagination.py
    ├── mixins.py
    ├── constants.py
    └── exceptions.py
