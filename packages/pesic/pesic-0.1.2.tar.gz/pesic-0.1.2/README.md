# PESIC - PetroElektroSbyt Integrated Client

## Usage

```python
from pesic.wrapper import PESClient
username = "88005553535"
password = "ЧемУкогоТоЗанимать"
pesik = PESClient(username=username, password=password)

pesik.get_groups()
print (pesik.update_meter_counters(
            [[8760, "DAY"], [2730, "NIGHT"]]))
```

## DEBUG

```bash
export PESIC_LOGLEVE="debug"
```

## Предостережение

Личный кабинет ПетроЭлектроСбыт поддерживает несколько типов учетных записей. Как классические, для передачи показаний потребления электроэнергии, так и учетные записи поставщиков холодной и горячей воды и, возможно, какие-то еще.

Метод update_meter_counters API Wrapper в данный поддеживает только обновление двухтарифных счетчиков электроэнергии и только для первой учетной записи:

```python
pesik.get_accounts()[0]
```
