# Migrations

1. Modify the schema by rewriting the ORMs (add a column, rename a column, add constraints, drop constraints, add an ORM, etc.)
2. Generate the migration script: `lnhub migrate generate`
3. Thoroughly test the migration script: `pytest tests/test_migrations.py`
4. Once tests pass, merge to main and make a release commit, **bump** the version number
5. Deploy the migration to production database via `lnhub migrate deploy`.
