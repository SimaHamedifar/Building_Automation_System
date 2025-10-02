
# 2) Docker Compose (Postgres + pgAdmin)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  db:
    image: postgres:15
    restart: unless-stopped
    environment:
      POSTGRES_USER: bms
      POSTGRES_PASSWORD: bms_pass
      POSTGRES_DB: bms_db
    ports:
      - "5432:5432"
    volumes:
      - db_data:/var/lib/postgresql/data
      - ./db/init_db.sql:/docker-entrypoint-initdb.d/init_db.sql:ro

  pgadmin:
    image: dpage/pgadmin4
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@local
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "8080:80"
    depends_on:
      - db

volumes:
  db_data:
