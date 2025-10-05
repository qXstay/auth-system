from sqlalchemy.orm import Session
from models.role import Role
from database.db import SessionLocal
from models.access_roles_rules import AccessRolesRules

def create_default_rules():
    db: Session = SessionLocal()
    try:
        roles = db.query(Role).all()
        for role in roles:
            if role.name == "admin":
                rules = [
                    AccessRolesRules(
                        role_id=role.id,
                        element="users",
                        read_all_permission=True,
                        update_all_permission=True,
                        delete_all_permission=True,
                        create_permission=True
                    ),
                    AccessRolesRules(
                        role_id=role.id,
                        element="products",
                        read_all_permission=True,
                        update_all_permission=True,
                        delete_all_permission=True,
                        create_permission=True
                    )
                ]
            elif role.name == "user":
                rules = [
                    AccessRolesRules(
                        role_id=role.id,
                        element="users",
                        read_permission=True,
                        update_permission=True
                    ),
                    AccessRolesRules(
                        role_id=role.id,
                        element="products",
                        read_permission=True,
                        update_permission=True,
                        create_permission=True
                    )
                ]
            else:
                rules = []
            for rule in rules:
                db.add(rule)
        db.commit()
    finally:
        db.close()