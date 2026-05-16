# ddd

- [ ] entrar mais a fundo nos conceitos
  - [ ] shared kernel
  - [ ] anti-corruption layer
  - [ ] conformist
  - [ ] aggregate
  - [ ] domain event
  - [ ] specification pattern

## projeto

- [ ] raise nos base errors, e tratar isso globalmente, é trivialmente serializável pra json ou qualquer outra coisa, já que é só code, title e details
- [x] achar um jeito melhor de lidar com mappers
- [x] strip whitespace já tá no basemodel, ignorar nos modelos herdados
- [x] fazer dependency injection direito, com factories para os use cases
- [x] transformar outros endpoints em use cases tmb

## testes

- [x] shared_kernel::env
- [x] base::error
- [x] shared_kernel::utils
- [ ] shared_kernel::value_objects
- [ ] conta::application::use_cases
- [ ] conta::application::dtos::EntrarInput
- [ ] conta::presentation::views
- [ ] conta::infrastructure::repositories
- [ ] conta::infrastructure::services
- [ ] conta::domain::aggregates
- [ ] conta::domain::value_objects
- [x] conta::shared::mappers
