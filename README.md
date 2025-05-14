Pre lokálnu inštaláciu backendu aplikácie je potrebné postupovať následovne:

1. Nainstalovať python
2. (Odporúčané) vytvoriť virtualny enviroment pre python. Napríklad pomocov venv : `python -m venv "nazov venv"` následne je potrebné enviromet aktivovať pomocou `source "nazov venv"/bin/activate`
3. Je potrebné nainštalovať všetky potrebné súčasti pomocou príkazu `pip install -r requirements.txt`
4. Je potrebné prejst do adresára `/GaifikaceVUT` a spustit server pomocou príkazu `python manage.py runserver`

---

Backend bude v následujúcich 3 mesiacoch bežať aj online na stránke https://gamifikace.ink/api. Táto stránka poskytuje endpointy ku ktorým pristupuje frontend. Taktiež sa tu nachádza administrátorský mód https://gamifikace.ink/admin. Pristúpit je k nemu možné pomocou týchto prihlasovacích udajov :

- Užívateľské meno : admin
- Heslo : Heslo123123!

---

Zložka systemd-units obsahuje príklad súborov na spustenie služieb pri nasadení backendu do produkcie.
Pre periodické generovanie výzvy je potrebné aby bola spustená služba `celery` a `celery-beat`.
Aby mohli byť tieto služby spustené je potrebné mať taktiež na serveri nainstalovaný `Redis` v ktorom sa ukladajú naplanované úlohy.

---

V zložke `GamifikaceVUT/build` sa nachádza vygenerovaná dokumentácia pomocou nástroja `Sphinx`. Niektoré jej časti sú po anglicky keďže nástroj sám osebe nepodporuje slovenčinu. Komentovaná časť kódu je po slovensky.
