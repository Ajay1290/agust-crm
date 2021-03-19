from flask import session
from flask_sqlalchemy import SQLAlchemy

import sqlite3
from sqlite3 import Error


import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from manager.libs.JsonDB import JsonDB

class MultiTenantSQLAlchemy(SQLAlchemy):
    
    def choose_tenant(self, tenant_name):
        if 'tenant_name' in session:
            session.pop('tenant_name')
        session['tenant_name'] = tenant_name
        super().get_engine(bind=tenant_name)

    def get_engine(self, app=None, bind=None):
        if bind is None:
            try:
                bind = session['tenant_name']
            except Exception as e:
                print(e)
        return super().get_engine(bind=bind)
    
    def _create_sqlite_db(self, app=None, tenant_name=None):
        db_uris = JsonDB('uri', path=f"{app.config['BASE_DIR']}")
        db_uris.add(tenant_name, f"sqlite:///{app.config['DB_PATH']}\\{tenant_name}.db")
        db_uris.commit()
        
        binds = app.config['SQLALCHEMY_BINDS']
        binds[tenant_name] = f"sqlite:///{app.config['DB_PATH']}\\{tenant_name}.db"
        app.config.update(SQLALCHEMY_BINDS = binds)
        print(app.config['SQLALCHEMY_BINDS'])
        self.create_all(bind=tenant_name)
        return True

    def _create_postgres_db(self, app=None, tenant_name=None):
        con = psycopg2.connect(dbname='agust_db', user='postgres', host='', password='apku1290')
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute(sql.SQL(f"CREATE DATABASE {tenant_name}"))

        db_uris = JsonDB('uri', path=f"{app.config['BASE_DIR']}")
        db_uris.add(tenant_name, f'postgresql://postgres:apku1290@localhost:5432/{tenant_name}')
        db_uris.commit()
        
        binds = app.config['SQLALCHEMY_BINDS']
        binds[tenant_name] = f'postgresql://postgres:apku1290@localhost:5432/{tenant_name}'
        app.config.update(SQLALCHEMY_BINDS = binds)
        return True

    def create_db_for_tenant(self, app=None, tenant_name=None):
        if tenant_name:
            if self._create_sqlite_db(app, tenant_name):
                return True
        return False

