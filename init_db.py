from database.db import SessionLocal, engine
from models.role import Role
from models.user import User
from models.access_roles_rules import AccessRolesRules
from utils.security import hash_password


def init_database():
    db = SessionLocal()

    try:
        # Создаем роли
        admin_role = Role(name="admin", description="Administrator")
        user_role = Role(name="user", description="Regular User")

        db.add_all([admin_role, user_role])
        db.commit()

        # Обновляем объекты чтобы получить ID
        db.refresh(admin_role)
        db.refresh(user_role)

        # Создаем правила для админа
        admin_rules = [
            AccessRolesRules(
                role_id=admin_role.id,
                element="users",
                read_permission=True,
                read_all_permission=True,
                create_permission=True,
                update_permission=True,
                update_all_permission=True,
                delete_permission=True,
                delete_all_permission=True
            ),
            AccessRolesRules(
                role_id=admin_role.id,
                element="products",
                read_permission=True,
                read_all_permission=True,
                create_permission=True,
                update_permission=True,
                update_all_permission=True,
                delete_permission=True,
                delete_all_permission=True
            )
        ]

        # Создаем правила для пользователя
        user_rules = [
            AccessRolesRules(
                role_id=user_role.id,
                element="users",
                read_permission=True,
                read_all_permission=False,
                create_permission=False,
                update_permission=True,  # Может обновлять только свой профиль
                update_all_permission=False,
                delete_permission=True,  # Может удалить только свой аккаунт
                delete_all_permission=False
            ),
            AccessRolesRules(
                role_id=user_role.id,
                element="products",
                read_permission=True,
                read_all_permission=False,
                create_permission=True,
                update_permission=True,  # Может обновлять только свои продукты
                update_all_permission=False,
                delete_permission=True,  # Может удалять только свои продукты
                delete_all_permission=False
            )
        ]

        db.add_all(admin_rules + user_rules)

        # Создаем тестового админа
        admin_user = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role_id=admin_role.id
        )

        db.add(admin_user)
        db.commit()

        print("Database initialized successfully!")
        print(f"Admin user created: admin@example.com / admin123")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()