from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.access_roles_rules import AccessRolesRules


def check_permission(user, element: str, action: str, db: Session):
    # admin все может
    if user.role.name == "admin":
        return True

    # Ищем правила для роли пользователя и элемента
    rule = db.query(AccessRolesRules).filter(
        AccessRolesRules.role_id == user.role_id,
        AccessRolesRules.element == element
    ).first()

    if not rule:
        raise HTTPException(status_code=403, detail="Access denied")

    # Проверяем конкретное разрешение
    permission_map = {
        "read": rule.read_permission,
        "read_all": rule.read_all_permission,
        "create": rule.create_permission,
        "update": rule.update_permission,
        "update_all": rule.update_all_permission,
        "delete": rule.delete_permission,
        "delete_all": rule.delete_all_permission,
    }

    if action not in permission_map or not permission_map[action]:
        raise HTTPException(status_code=403, detail="Access denied")

    return True