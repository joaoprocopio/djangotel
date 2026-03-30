# type: ignore
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Generic, TypeVar
from uuid import UUID, uuid4

# ═══════════════════════════════════════════════════════════════
# UBIQUITOUS LANGUAGE
# Shared terms used everywhere in this bounded context.
# "Order" always means a customer purchase, never an instruction.
# ═══════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════
# VALUE OBJECTS
# Immutable, no identity, equality by attributes.
# Always valid — validation lives in __post_init__ or create().
# ═══════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class ValueObject:
    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(tuple(self.__dict__.values()))


@dataclass(frozen=True)
class Money(ValueObject):
    amount: float
    currency: str

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")

    @staticmethod
    def create(amount: float, currency: str) -> Money:
        currency = currency.strip().upper()
        if currency not in {"USD", "EUR", "GBP"}:
            raise ValueError(f"Unsupported currency: {currency}")
        return Money(round(amount, 2), currency)

    @staticmethod
    def zero(currency: str) -> Money:
        return Money(0.0, currency.upper())

    def add(self, other: Money) -> Money:
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(round(self.amount + other.amount, 2), self.currency)

    def multiply(self, factor: float) -> Money:
        return Money(round(self.amount * factor, 2), self.currency)


@dataclass(frozen=True)
class Email(ValueObject):
    value: str

    def __post_init__(self):
        if "@" not in self.value or "." not in self.value.split("@")[-1]:
            raise ValueError(f"Invalid email: {self.value}")

    @staticmethod
    def create(value: str) -> Email:
        return Email(value.strip().lower())


@dataclass(frozen=True)
class Address(ValueObject):
    street: str
    city: str
    country: str
    postal_code: str

    def __post_init__(self):
        if not all([self.street, self.city, self.country, self.postal_code]):
            raise ValueError("All address fields are required")


# ═══════════════════════════════════════════════════════════════
# DOMAIN EVENTS
# Immutable records of something that happened.
# Raised inside aggregates, dispatched by the application layer.
# ═══════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class CustomerRegistered(DomainEvent):
    customer_id: UUID
    email: str


@dataclass(frozen=True)
class OrderPlaced(DomainEvent):
    order_id: UUID
    customer_id: UUID
    total: float
    currency: str


@dataclass(frozen=True)
class OrderCancelled(DomainEvent):
    order_id: UUID
    reason: str


@dataclass(frozen=True)
class OrderItemAdded(DomainEvent):
    order_id: UUID
    product_id: UUID
    quantity: int
    unit_price: float


# ═══════════════════════════════════════════════════════════════
# ENTITIES
# Have a unique identity (UUID). Equality is by ID only.
# Internal state changes through explicit domain methods.
# ═══════════════════════════════════════════════════════════════


class Entity(ABC):
    id: UUID
    _events: list[DomainEvent]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Entity) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def pull_events(self) -> list[DomainEvent]:
        events, self._events = self._events, []
        return events


@dataclass
class OrderItem(Entity):
    """Entity nested inside Order aggregate."""

    id: UUID
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Money
    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    @staticmethod
    def create(
        product_id: UUID, product_name: str, quantity: int, unit_price: Money
    ) -> OrderItem:
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        return OrderItem(
            id=uuid4(),
            product_id=product_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
        )

    @property
    def subtotal(self) -> Money:
        return self.unit_price.multiply(self.quantity)


# ═══════════════════════════════════════════════════════════════
# AGGREGATES
# Cluster of entities and value objects.
# The Aggregate Root is the only public entry point.
# Enforces all invariants. Raises domain events.
# ═══════════════════════════════════════════════════════════════


@dataclass
class Order(Entity):
    """Aggregate Root — all changes to Order go through here."""

    id: UUID
    customer_id: UUID
    status: str
    shipping_address: Address
    items: list[OrderItem] = field(default_factory=list)
    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    # ── invariant: total is derived, never stored directly ──
    @property
    def total(self) -> Money:
        if not self.items:
            return Money.zero("USD")
        result = Money.zero(self.items[0].unit_price.currency)
        for item in self.items:
            result = result.add(item.subtotal)
        return result

    def add_item(
        self, product_id: UUID, product_name: str, quantity: int, unit_price: Money
    ) -> None:
        if self.status != "draft":
            raise ValueError("Cannot modify a non-draft order")
        item = OrderItem.create(product_id, product_name, quantity, unit_price)
        self.items.append(item)
        self._events.append(
            OrderItemAdded(
                order_id=self.id,
                product_id=product_id,
                quantity=quantity,
                unit_price=unit_price.amount,
            )
        )

    def place(self) -> None:
        if self.status != "draft":
            raise ValueError("Order is already placed")
        if not self.items:
            raise ValueError("Cannot place an empty order")
        self.status = "placed"
        self._events.append(
            OrderPlaced(
                order_id=self.id,
                customer_id=self.customer_id,
                total=self.total.amount,
                currency=self.total.currency,
            )
        )

    def cancel(self, reason: str) -> None:
        if self.status not in {"draft", "placed"}:
            raise ValueError(f"Cannot cancel an order with status: {self.status}")
        self.status = "cancelled"
        self._events.append(OrderCancelled(order_id=self.id, reason=reason))


@dataclass
class Customer(Entity):
    """Aggregate Root for the Customer aggregate."""

    id: UUID
    name: str
    email: Email
    billing_address: Address
    balance: Money
    _events: list[DomainEvent] = field(default_factory=list, repr=False)

    def credit(self, amount: Money) -> None:
        self.balance = self.balance.add(amount)

    def change_email(self, new_email: Email) -> None:
        self.email = new_email


# ═══════════════════════════════════════════════════════════════
# FACTORIES
# Encapsulate complex construction logic.
# Used when an aggregate requires multiple steps or dependencies
# to be built correctly.
# ═══════════════════════════════════════════════════════════════


class CustomerFactory:
    @staticmethod
    def create(
        name: str, raw_email: str, address: Address, currency: str = "USD"
    ) -> Customer:
        customer = Customer(
            id=uuid4(),
            name=name.strip(),
            email=Email.create(raw_email),
            billing_address=address,
            balance=Money.zero(currency),
        )
        customer._events.append(
            CustomerRegistered(
                customer_id=customer.id,
                email=customer.email.value,
            )
        )
        return customer


class OrderFactory:
    @staticmethod
    def create(customer: Customer, shipping_address: Address) -> Order:
        return Order(
            id=uuid4(),
            customer_id=customer.id,
            status="draft",
            shipping_address=shipping_address,
        )


# ═══════════════════════════════════════════════════════════════
# SPECIFICATIONS
# Encapsulate a single business rule as a reusable predicate.
# Can be combined with and_spec / or_spec / not_spec.
# ═══════════════════════════════════════════════════════════════

S = TypeVar("S")


class Specification(ABC, Generic[S]):
    @abstractmethod
    def is_satisfied_by(self, candidate: S) -> bool: ...

    def and_spec(self, other: Specification[S]) -> Specification[S]:
        return _AndSpecification(self, other)

    def or_spec(self, other: Specification[S]) -> Specification[S]:
        return _OrSpecification(self, other)

    def not_spec(self) -> Specification[S]:
        return _NotSpecification(self)


class _AndSpecification(Specification[S]):
    def __init__(self, a: Specification[S], b: Specification[S]):
        self._a, self._b = a, b

    def is_satisfied_by(self, candidate: S) -> bool:
        return self._a.is_satisfied_by(candidate) and self._b.is_satisfied_by(candidate)


class _OrSpecification(Specification[S]):
    def __init__(self, a: Specification[S], b: Specification[S]):
        self._a, self._b = a, b

    def is_satisfied_by(self, candidate: S) -> bool:
        return self._a.is_satisfied_by(candidate) or self._b.is_satisfied_by(candidate)


class _NotSpecification(Specification[S]):
    def __init__(self, spec: Specification[S]):
        self._spec = spec

    def is_satisfied_by(self, candidate: S) -> bool:
        return not self._spec.is_satisfied_by(candidate)


class OrderIsPlaceableSpec(Specification[Order]):
    """Business rule: an order can only be placed if it has items."""

    def is_satisfied_by(self, order: Order) -> bool:
        return order.status == "draft" and len(order.items) > 0


class OrderHasSufficientValueSpec(Specification[Order]):
    """Business rule: order total must exceed minimum threshold."""

    def __init__(self, minimum: Money):
        self._minimum = minimum

    def is_satisfied_by(self, order: Order) -> bool:
        return order.total.amount >= self._minimum.amount


# ═══════════════════════════════════════════════════════════════
# REPOSITORIES
# Abstract persistence interface. One per aggregate root.
# The domain defines the interface; infrastructure implements it.
# ═══════════════════════════════════════════════════════════════

T = TypeVar("T", bound=Entity)


class Repository(ABC, Generic[T]):
    @abstractmethod
    def find_by_id(self, id: UUID) -> T | None: ...

    @abstractmethod
    def save(self, entity: T) -> None: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...


class CustomerRepository(Repository[Customer]):
    def __init__(self) -> None:
        self._store: dict[UUID, Customer] = {}

    def find_by_id(self, id: UUID) -> Customer | None:
        return self._store.get(id)

    def find_by_email(self, email: Email) -> Customer | None:
        return next((c for c in self._store.values() if c.email == email), None)

    def save(self, entity: Customer) -> None:
        self._store[entity.id] = entity

    def delete(self, id: UUID) -> None:
        self._store.pop(id, None)


class OrderRepository(Repository[Order]):
    def __init__(self) -> None:
        self._store: dict[UUID, Order] = {}

    def find_by_id(self, id: UUID) -> Order | None:
        return self._store.get(id)

    def find_by_customer(self, customer_id: UUID) -> list[Order]:
        return [o for o in self._store.values() if o.customer_id == customer_id]

    def save(self, entity: Order) -> None:
        self._store[entity.id] = entity

    def delete(self, id: UUID) -> None:
        self._store.pop(id, None)


# ═══════════════════════════════════════════════════════════════
# DOMAIN SERVICES
# Stateless logic that spans multiple aggregates.
# Does not belong to any single entity or value object.
# ═══════════════════════════════════════════════════════════════


class DomainService(ABC):
    pass


class PricingService(DomainService):
    """Calculates prices — spans products and orders, belongs to neither."""

    def apply_discount(self, price: Money, percent: float) -> Money:
        if not 0 <= percent <= 100:
            raise ValueError("Discount must be between 0 and 100")
        return price.multiply(1 - percent / 100)

    def calculate_tax(self, price: Money, tax_rate: float) -> Money:
        return price.multiply(tax_rate)


class TransferService(DomainService):
    """Transfers balance between two customers — neither owns this logic."""

    def transfer(self, sender: Customer, receiver: Customer, amount: Money) -> None:
        if sender.balance.amount < amount.amount:
            raise ValueError("Insufficient balance")
        sender.balance = sender.balance.add(Money(-amount.amount, amount.currency))
        receiver.credit(amount)


# ═══════════════════════════════════════════════════════════════
# EVENT BUS
# Dispatches domain events to registered handlers.
# Lives in application layer — domain only raises events.
# ═══════════════════════════════════════════════════════════════


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable[[DomainEvent], None]]] = {}

    def subscribe(
        self, event_type: type, handler: Callable[[DomainEvent], None]
    ) -> None:
        self._handlers.setdefault(event_type, []).append(handler)

    def publish(self, event: DomainEvent) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)

    def publish_all(self, events: list[DomainEvent]) -> None:
        for event in events:
            self.publish(event)


# ═══════════════════════════════════════════════════════════════
# APPLICATION SERVICES / USE CASES
# Orchestrate the domain to fulfill one user action.
# No business logic here — only coordination.
# ═══════════════════════════════════════════════════════════════

Input = TypeVar("Input")
Output = TypeVar("Output")


class UseCase(ABC, Generic[Input, Output]):
    @abstractmethod
    def execute(self, input: Input) -> Output: ...


@dataclass(frozen=True)
class RegisterCustomerInput:
    name: str
    email: str
    street: str
    city: str
    country: str
    postal_code: str
    currency: str = "USD"


@dataclass(frozen=True)
class RegisterCustomerOutput:
    customer_id: UUID
    email: str
    balance: float
    currency: str


class RegisterCustomerUseCase(UseCase[RegisterCustomerInput, RegisterCustomerOutput]):
    def __init__(self, customer_repo: CustomerRepository, bus: EventBus) -> None:
        self._customers = customer_repo
        self._bus = bus

    def execute(self, input: RegisterCustomerInput) -> RegisterCustomerOutput:
        if self._customers.find_by_email(Email.create(input.email)):
            raise ValueError(f"Email already registered: {input.email}")

        address = Address(input.street, input.city, input.country, input.postal_code)
        customer = CustomerFactory.create(
            input.name, input.email, address, input.currency
        )

        self._customers.save(customer)
        self._bus.publish_all(customer.pull_events())

        return RegisterCustomerOutput(
            customer_id=customer.id,
            email=customer.email.value,
            balance=customer.balance.amount,
            currency=customer.balance.currency,
        )


@dataclass(frozen=True)
class PlaceOrderInput:
    customer_id: UUID
    items: list[dict]  # [{"product_id", "name", "quantity", "unit_price", "currency"}]
    discount_percent: float = 0.0
    minimum_order_amount: float = 0.0


@dataclass(frozen=True)
class PlaceOrderOutput:
    order_id: UUID
    total: float
    currency: str
    status: str


class PlaceOrderUseCase(UseCase[PlaceOrderInput, PlaceOrderOutput]):
    def __init__(
        self,
        customer_repo: CustomerRepository,
        order_repo: OrderRepository,
        pricing_service: PricingService,
        bus: EventBus,
    ) -> None:
        self._customers = customer_repo
        self._orders = order_repo
        self._pricing = pricing_service
        self._bus = bus

    def execute(self, input: PlaceOrderInput) -> PlaceOrderOutput:
        # Load aggregate
        customer = self._customers.find_by_id(input.customer_id)
        if not customer:
            raise ValueError(f"Customer not found: {input.customer_id}")

        # Build order via factory
        order = OrderFactory.create(customer, customer.billing_address)

        # Add items
        for item in input.items:
            raw_price = Money.create(item["unit_price"], item["currency"])
            discounted = self._pricing.apply_discount(raw_price, input.discount_percent)
            order.add_item(
                product_id=UUID(item["product_id"]),
                product_name=item["name"],
                quantity=item["quantity"],
                unit_price=discounted,
            )

        # Validate via specifications
        placeable = OrderIsPlaceableSpec()
        min_value = OrderHasSufficientValueSpec(
            Money.create(input.minimum_order_amount, order.total.currency)
        )
        combined = placeable.and_spec(min_value)

        if not combined.is_satisfied_by(order):
            raise ValueError("Order does not meet placement requirements")

        # Mutate aggregate
        order.place()

        # Persist and dispatch
        self._orders.save(order)
        self._bus.publish_all(order.pull_events())

        return PlaceOrderOutput(
            order_id=order.id,
            total=order.total.amount,
            currency=order.total.currency,
            status=order.status,
        )


# ═══════════════════════════════════════════════════════════════
# ANTI-CORRUPTION LAYER
# Translates an external model into our domain model.
# Protects the domain from foreign concepts or naming.
# ═══════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class ExternalPaymentEvent:
    """Simulates a foreign bounded context payload (e.g. a payment service)."""

    transaction_ref: str
    payer_email: str
    paid_amount: float
    paid_currency: str
    timestamp: str


class PaymentACL:
    """
    Anti-Corruption Layer — translates payment events into
    domain concepts without polluting the Order context.
    """

    def __init__(self, customer_repo: CustomerRepository) -> None:
        self._customers = customer_repo

    def to_domain_credit(self, event: ExternalPaymentEvent) -> tuple[Customer, Money]:
        customer = self._customers.find_by_email(Email.create(event.payer_email))
        if not customer:
            raise ValueError(f"No customer for email: {event.payer_email}")
        amount = Money.create(event.paid_amount, event.paid_currency)
        return customer, amount


# ═══════════════════════════════════════════════════════════════
# SHARED KERNEL
# A small, stable model shared between bounded contexts.
# Changed only with agreement from all teams that use it.
# ═══════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class SharedCurrency(ValueObject):
    """
    Shared Kernel — agreed currency codes used across
    the Order and Payment bounded contexts.
    """

    code: str
    SUPPORTED: frozenset[str] = field(
        default_factory=lambda: frozenset({"USD", "EUR", "GBP"})
    )

    def __post_init__(self):
        if self.code not in self.SUPPORTED:
            raise ValueError(f"Unsupported currency: {self.code}")


# ═══════════════════════════════════════════════════════════════
# INTEGRATION EVENT
# A domain event promoted to cross bounded context boundaries.
# Carries only the data the outside world needs — no internals.
# ═══════════════════════════════════════════════════════════════


@dataclass(frozen=True)
class OrderPlacedIntegrationEvent:
    """
    Crosses from the Order context → Notification / Shipping context.
    Stripped of internal domain types; only primitives.
    """

    order_id: str
    customer_email: str
    total_amount: float
    currency: str
    placed_at: str


class IntegrationEventTranslator:
    """Maps internal domain events to integration events."""

    def __init__(self, customer_repo: CustomerRepository) -> None:
        self._customers = customer_repo

    def from_order_placed(self, event: OrderPlaced) -> OrderPlacedIntegrationEvent:
        customer = self._customers.find_by_id(event.customer_id)
        if not customer:
            raise ValueError("Customer not found")
        return OrderPlacedIntegrationEvent(
            order_id=str(event.order_id),
            customer_email=customer.email.value,
            total_amount=event.total,
            currency=event.currency,
            placed_at=event.occurred_at.isoformat(),
        )


# ═══════════════════════════════════════════════════════════════
# WIRING & DEMO
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Infrastructure
    customer_repo = CustomerRepository()
    order_repo = OrderRepository()
    pricing_service = PricingService()
    bus = EventBus()
    translator = IntegrationEventTranslator(customer_repo)

    # Event handlers (could live in Notification bounded context)
    def on_customer_registered(e: DomainEvent) -> None:
        assert isinstance(e, CustomerRegistered)
        print(f"  [Notification] Welcome email sent to customer {e.customer_id}")

    def on_order_placed(e: DomainEvent) -> None:
        assert isinstance(e, OrderPlaced)
        integration_event = translator.from_order_placed(e)
        print(
            f"  [Shipping]     Order {integration_event.order_id} dispatched to shipping context"
        )
        print(
            f"  [Email]        Confirmation sent to {integration_event.customer_email}"
        )

    def on_order_cancelled(e: DomainEvent) -> None:
        assert isinstance(e, OrderCancelled)
        print(
            f"  [Refund]       Refund triggered for order {e.order_id} — reason: {e.reason}"
        )

    bus.subscribe(CustomerRegistered, on_customer_registered)
    bus.subscribe(OrderPlaced, on_order_placed)
    bus.subscribe(OrderCancelled, on_order_cancelled)

    print("\n── Register Customer ──────────────────────────────")
    register = RegisterCustomerUseCase(customer_repo, bus)
    customer_out = register.execute(
        RegisterCustomerInput(
            name="Alice",
            email="alice@example.com",
            street="123 Main St",
            city="Porto",
            country="PT",
            postal_code="4000-001",
            currency="USD",
        )
    )
    print(f"  Customer ID : {customer_out.customer_id}")
    print(f"  Email       : {customer_out.email}")

    print("\n── Place Order ────────────────────────────────────")
    place = PlaceOrderUseCase(customer_repo, order_repo, pricing_service, bus)
    order_out = place.execute(
        PlaceOrderInput(
            customer_id=customer_out.customer_id,
            items=[
                {
                    "product_id": str(uuid4()),
                    "name": "Notebook",
                    "quantity": 2,
                    "unit_price": 49.99,
                    "currency": "USD",
                },
                {
                    "product_id": str(uuid4()),
                    "name": "Pen Set",
                    "quantity": 1,
                    "unit_price": 12.00,
                    "currency": "USD",
                },
            ],
            discount_percent=10.0,
            minimum_order_amount=5.0,
        )
    )
    print(f"  Order ID    : {order_out.order_id}")
    print(f"  Total       : ${order_out.total} {order_out.currency}")
    print(f"  Status      : {order_out.status}")

    print("\n── Cancel Order ───────────────────────────────────")
    order = order_repo.find_by_id(order_out.order_id)
    assert order is not None
    order.cancel("Customer changed their mind")
    order_repo.save(order)
    bus.publish_all(order.pull_events())

    print("\n── Anti-Corruption Layer ──────────────────────────")
    acl = PaymentACL(customer_repo)
    external = ExternalPaymentEvent(
        transaction_ref="TXN-999",
        payer_email="alice@example.com",
        paid_amount=100.0,
        paid_currency="USD",
        timestamp=datetime.utcnow().isoformat(),
    )
    customer_entity, credit_amount = acl.to_domain_credit(external)
    customer_entity.credit(credit_amount)
    customer_repo.save(customer_entity)
    print(f"  Credited ${credit_amount.amount} to {customer_entity.email.value}")
    print(
        f"  New balance: ${customer_entity.balance.amount} {customer_entity.balance.currency}"
    )
