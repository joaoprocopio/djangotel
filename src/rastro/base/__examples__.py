from dataclasses import dataclass
from typing import Protocol

from rastro.base.aggregates import AggregateRoot
from rastro.base.domain_events import DomainEvent
from rastro.base.domain_services import DomainService
from rastro.base.entities import Entity
from rastro.base.factories import Factory
from rastro.base.specifications import Specification
from rastro.base.use_cases import UseCase
from rastro.base.value_objects import ValueObject


@dataclass(frozen=True)
class Email(ValueObject[str]):
    def validate(self) -> None:
        if "@" not in self.value:
            raise ValueError(f"Invalid email: {self.value}")


@dataclass(frozen=True)
class Password(ValueObject[str]):
    def validate(self) -> None:
        if len(self.value) < 8:
            raise ValueError("Password must be at least 8 characters")


# ============================================================================
# ENTITIES (inside aggregate)
# ============================================================================


@dataclass
class UserProfile(Entity[int]):
    name: str
    avatar_url: str | None = None


# ============================================================================
# DOMAIN EVENTS
# ============================================================================


@dataclass(frozen=True)
class UserCreatedEvent(DomainEvent):
    user_id: int
    email: str


@dataclass(frozen=True)
class UserEmailChangedEvent(DomainEvent):
    user_id: int
    old_email: str
    new_email: str


# ============================================================================
# AGGREGATE ROOT
# ============================================================================


@dataclass
class User(AggregateRoot[int]):
    email: Email
    password: Password
    profile: UserProfile | None = None

    def change_email(self, new_email: Email) -> None:
        if self.email == new_email:
            return
        old_email = self.email
        self.email = new_email
        self.add_domain_event(
            UserEmailChangedEvent(
                user_id=self.id,  # type: ignore[arg-type]
                old_email=old_email.value,
                new_email=new_email.value,
            )
        )


# ============================================================================
# SPECIFICATIONS
# ============================================================================


class ActiveUserSpecification(Specification[User]):
    def is_satisfied_by(self, candidate: User) -> bool:
        return candidate.id is not None and candidate.profile is not None


class EmailDomainSpecification(Specification[User]):
    def __init__(self, domain: str) -> None:
        self._domain = domain

    def is_satisfied_by(self, candidate: User) -> bool:
        return candidate.email.value.endswith(f"@{self._domain}")


# Usage: spec = ActiveUserSpecification().and_(EmailDomainSpecification("company.com"))


# ============================================================================
# REPOSITORY
# ============================================================================


class UserRepository(Protocol):
    def add(self, user: User) -> None: ...
    def get_by_email(self, email: Email) -> User | None: ...
    def get_by_specification(self, spec: Specification[User]) -> list[User]: ...


# ============================================================================
# DOMAIN SERVICE
# ============================================================================


class UserDomainService(DomainService):
    def is_email_unique(self, email: Email, repository: UserRepository) -> bool:
        existing = repository.get_by_email(email)
        return existing is None

    def can_register(
        self, email: Email, password: Password, repository: UserRepository
    ) -> bool:
        unique_email_spec = EmailDomainSpecification("company.com")
        return self.is_email_unique(
            email, repository
        ) and unique_email_spec.is_satisfied_by(
            User(id=None, email=email, password=password)
        )


# ============================================================================
# FACTORY
# ============================================================================


class UserFactory(Factory[[str, str, str | None], User]):
    def create(self, email: str, password: str, name: str | None = None) -> User:
        email_vo = Email(email)
        password_vo = Password(password)
        user = User(id=None, email=email_vo, password=password_vo)
        if name:
            user.profile = UserProfile(id=None, name=name)
        user.add_domain_event(
            UserCreatedEvent(user_id=None, email=email)  # type: ignore[arg-type]
        )
        return user


# ============================================================================
# USE CASE (Application Service)
# ============================================================================


@dataclass
class RegisterUserInput:
    email: str
    password: str
    name: str | None = None


@dataclass
class RegisterUserOutput:
    user_id: int
    email: str


class RegisterUserUseCase(UseCase[RegisterUserInput, RegisterUserOutput]):
    repository: UserRepository
    factory: UserFactory

    def __init__(self, repository: UserRepository, factory: UserFactory) -> None:
        self.repository = repository
        self.factory = factory

    def execute(self, input: RegisterUserInput) -> RegisterUserOutput:
        user = self.factory.create(
            email=input.email, password=input.password, name=input.name
        )
        self.repository.add(user)
        return RegisterUserOutput(
            user_id=user.id,  # type: ignore[arg-type]
            email=user.email.value,
        )


# ============================================================================
# USAGE EXAMPLE
# ============================================================================


if __name__ == "__main__":
    # Create user via factory
    factory = UserFactory()
    user = factory.create(
        email="john@company.com", password="securepass123", name="John Doe"
    )

    # Check specifications
    active_spec = ActiveUserSpecification()
    company_spec = EmailDomainSpecification("company.com")
    combined_spec = active_spec.and_(company_spec)

    print(f"Is active user: {active_spec.is_satisfied_by(user)}")
    print(f"Has company email: {company_spec.is_satisfied_by(user)}")
    print(f"Combined spec: {combined_spec.is_satisfied_by(user)}")

    # Domain events
    print(f"Domain events: {[e.event_type for e in user.domain_events]}")
