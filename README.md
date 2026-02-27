# HARE Pro v2.0

**Hair Analysis Recommendation Engine** – Version professionnelle pour salon de coiffure haut de gamme (~100 produits).

---

## Stack

| Couche   | Technologie |
|----------|-------------|
| Frontend | Vue 3, TypeScript, Vite, Pinia, Vue Router, TailwindCSS, Headless UI |
| Backend  | FastAPI, SQLModel, PostgreSQL |
| DB       | PostgreSQL (Neon en prod) |
| Infra    | Docker, docker-compose | 
| Déploiement | Vercel (frontend) + Railway/Render (backend) |

---

## Thème

- **Rouge bordeaux** : `#800000` / `#9B1C2C`
- **Beige / crème** : fonds et cartes
- **Or** : accents (boutons, bordures)

---

## Lancer en local

```bash
cd HARE-Pro
docker compose up --build
```

- Frontend : http://localhost:5173  
- Backend API : http://localhost:8000  
- Docs API : http://localhost:8000/docs  

**Premier admin** (une fois les tables créées) :

```bash
cd hare-backend
ADMIN_INITIAL_PASSWORD=votre-mot-de-passe python -m app.utils.seed_admin
```

Puis se connecter à `/admin` avec `admin` / le mot de passe choisi. **Import produits** : depuis le dashboard Admin, importer un CSV (colonnes : name, brand, price, category, description, image_url, tags). Un fichier modèle est disponible : **Télécharger modèle CSV** dans l’admin ou `hare-frontend/public/export-template.csv`.

---

## Test Flow Client (démo livraison)

Scénario à suivre pour montrer l’application au client avant livraison.

### 1. Côté client (site public)

1. **Accueil** : Ouvrir http://localhost:5173 (ou l’URL de démo).
2. **Quiz** : Cliquer sur « Démarrer le quiz » (ou équivalent), répondre à toutes les questions (type de cheveux, objectifs, etc.).
3. **Résultats** : Vérifier l’affichage des recommandations produits et du rapport.
4. **Newsletter** : Saisir une adresse email dans le formulaire de capture après les résultats, valider. Vérifier qu’un message de succès s’affiche.
5. **Chatbot** : Ouvrir le bouton d’aide (💬), choisir une question FAQ ou poser une question libre, vérifier la réponse et le défilement de la zone de discussion.

### 2. Côté admin

1. **Connexion** : Aller sur `/admin`, se connecter avec les identifiants fournis (ex. `admin@salon.com` / `change-me-123` si données de démo chargées).
2. **Premier login** : Si demandé, **changer le mot de passe** (minimum 8 caractères, confirmation).
3. **Données de démo** (optionnel) : Cliquer sur **« Charger données de démo »**, confirmer. Vérifier le toast de succès et que les stats / liste des produits se mettent à jour (25 produits + 1 admin si créé).
4. **Modèle CSV** : Cliquer sur **« Télécharger modèle CSV »** et vérifier que le fichier `export-template.csv` se télécharge avec les colonnes attendues.
5. **Import CSV** : Glisser-déposer ou choisir un fichier CSV conforme au modèle, vérifier le message de succès et la mise à jour des produits.
6. **Stats & tableaux** : Vérifier les cartes (Quiz aujourd’hui, Leads, Produits), la pagination des produits, les filtres de recherche.
7. **Leads** : Filtrer par date / recherche, puis **Exporter CSV** et ouvrir le fichier exporté.
8. **Questions chatbot** : Cliquer sur « Charger les questions » et vérifier la liste des questions libres posées par les visiteurs.

### 3. Points de vigilance

- Responsive : tester sur une largeur réduite (mobile) pour le dashboard et le chatbot.
- Toasts : chaque action importante (connexion, import, seed, export, changement de mot de passe) doit afficher un message de succès ou d’erreur clair.

---

## Roadmap V2

| Sprint | Contenu |
|--------|---------|
| **Sprint 0** | Structure propre (fait) |
| **Sprint 1** | Design bordeaux + import CSV produits (100+) |
| **Sprint 2** | Newsletter (capture après recommandations) + dashboard admin (stats, produits, leads) |
| **Sprint 3** | Chatbot FAQ + aide, sécurisation admin (JWT / password) |
| **Sprint 4** | Tests, polish, déploiement production |

---

## Déploiement

### Frontend → Vercel

1. Root Directory : `hare-frontend`
2. Build : `npm run build`, Output : `dist`
3. Variables : `VITE_API_BASE_URL=https://votre-backend.railway.app`

### Backend → Railway / Render

- Build : `pip install -r requirements.txt` (ou image Docker)
- Start : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Variables : `DATABASE_URL` (Neon), `SECRET_KEY`, `ALLOWED_ORIGINS`

### Base de données → Neon

- Créer un projet, copier la connection string PostgreSQL.
- Renseigner `DATABASE_URL` dans le backend (format `postgresql://...?sslmode=require`).

---

## Devis client (section à personnaliser)

- **Prestation** : HARE Pro v2.0 – Quiz capillaire + recommandations + rapport PDF + newsletter + dashboard admin.
- **Livrables** : Code source, déploiement Vercel + backend + Neon, formation admin (1h).
- **Maintenance** : Option annuelle (mises à jour, correctifs, évolution mineure).

---

## Structure du projet

```
HARE-Pro/
├── hare-backend/          # FastAPI
│   ├── app/
│   │   ├── core/          # config, security, limiter, admin
│   │   ├── models/        # Product, QuizSubmission, NewsletterLead, AdminUser
│   │   ├── schemas/
│   │   ├── crud/
│   │   ├── api/v1/endpoints/  # quiz, products, admin, newsletter
│   │   ├── services/      # scoring, pdf_generator, csv_import
│   │   └── utils/
│   ├── alembic/
│   ├── Dockerfile
│   └── requirements.txt
├── hare-frontend/         # Vue 3 TS
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── composables/
│   │   └── router/
│   ├── Dockerfile
│   └── tailwind.config.js
├── docker-compose.yml
├── .gitignore
└── README.md
```
