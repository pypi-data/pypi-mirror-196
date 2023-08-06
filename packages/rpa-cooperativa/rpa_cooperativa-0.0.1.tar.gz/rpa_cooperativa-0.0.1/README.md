# dias-uteis-brasil
get dias_uteis_brasil, dias_uteis_mes, hoje_eh_dia_util

########### como chamar e utilizar a classe ###################
```python
from dias_uteis_brasil import dia_util

dia_util.dias_uteis_mes()
dia_util.feriados_nacionais(2022)    
dia_util.dias_uteis_mes(11, 2022)

res = dia_util.hoje_eh_dia_util(25, 12, 2022)
print(res)
```