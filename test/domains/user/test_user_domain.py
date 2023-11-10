import pytest

from app.domains.user.domain.user import User, UserRole


# Crie um fixture para criar um usuário de exemplo para testes
@pytest.fixture
def sample_user():
    user = User(
        name="John Doe",
        email="johndoe@example.com",
        cpf="12345678901",
        password="password123",
        telephone="123-456-7890",
        coins_amount=100,
    )

    return user


# Teste para verificar se a lista de papéis está vazia no início
def test_user_roles_empty_at_start(sample_user):
    assert not sample_user.roles


# Teste para verificar se o usuário não é um administrador
def test_user_is_not_admin(sample_user):
    assert sample_user.is_admin is False


# Teste para verificar se o usuário tem pelo menos uma role
def test_user_has_any_role(sample_user):
    assert not sample_user.has_any_role

    # Adicione uma role de exemplo e teste novamente
    role = UserRole(custom_role="USER", user=sample_user)
    sample_user.add_role(role)
    assert sample_user.has_any_role


# Teste para verificar se o usuário possui uma role específica
def test_user_has_this_role(sample_user):
    assert not sample_user.has_this_role("ADMIN")

    # Adicione uma role de exemplo e teste novamente
    role = UserRole(custom_role="ADMIN", user=sample_user)
    sample_user.add_role(role)
    assert sample_user.has_this_role("ADMIN")


# Teste para garantir que não seja possível adicionar a mesma role duas vezes
def test_add_duplicate_role(sample_user):
    role = UserRole(custom_role="USER", user=sample_user)
    sample_user.add_role(role)
    with pytest.raises(ValueError):
        sample_user.add_role(role)


# Teste para verificar se a exceção é levantada ao tentar adicionar a mesma role duas vezes
def test_add_duplicate_role_raises_exception(sample_user):
    role = UserRole(custom_role="USER", user=sample_user)
    sample_user.add_role(role)
    with pytest.raises(ValueError):
        sample_user.add_role(role)


# Teste para verificar se a propriedade is_admin funciona corretamente
def test_user_is_admin_property(sample_user):
    assert not sample_user.is_admin

    admin_role = UserRole(custom_role="ADMIN", user=sample_user)
    sample_user.add_role(admin_role)

    assert sample_user.is_admin


# Teste para verificar se a propriedade has_any_role funciona corretamente
def test_user_has_any_role_property(sample_user):
    assert not sample_user.has_any_role

    role = UserRole(custom_role="USER", user=sample_user)
    sample_user.add_role(role)

    assert sample_user.has_any_role


# Teste para verificar se o método add_role adiciona corretamente a role ao usuário
def test_add_role_method(sample_user):
    assert not sample_user.roles

    role = UserRole(custom_role="USER", user=sample_user)
    sample_user.add_role(role)

    assert role in sample_user.roles
