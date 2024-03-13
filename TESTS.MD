| Item              | In Stock | Price |
| :---------------- | :------: | :---: |
| Python Hat        |   True   | 23.99 |
| SQL Hat           |   True   | 23.99 |
| Codecademy Tee    |  False   | 19.99 |
| Codecademy Hoodie |  False   | 42.99 |


Teste sequencial
| Test | Until number | Total time in seconds |
| :---------------- | :------: | :---: |
| 1    | 1,000        | Total time in seconds |



- Enviando os dados um a um tivemos muito overhead e o tempo inclusive aumentou nos testes.
O tempo do processamento paralelo com um worker aumentou em cerca de 30% em comparação ao código sequencial.
Ainda, colocando mais worker o tempo aumentava ainda mais.

Resolvemos esta situação de overhead de comunicação enviando os dados por lote. Ou seja, ao invés de dizer que quero saber se o número X é primo, eu envio para o worker pedindo para calcular se os números de X até Y são primos.