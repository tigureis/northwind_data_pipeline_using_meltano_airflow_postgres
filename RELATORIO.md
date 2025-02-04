# Relatório do Projeto

## Etapa 1: Configurar o PostgreSQL
Utilize o arquivo docker-compose.yml para criar um banco de dados PostgreSQL e subir o arquivo northwind.sql para esse banco de dados. Nessa etapa, também foi feito o upload do arquivo order-details.sql.

#### Passos:
Configurar o Docker Compose:

* Crie um diretório data na raiz do projeto e coloque os arquivos northwind.sql e order-details.sql dentro deste diretório.
* Carregue o arquivo docker-compose.yml na raiz do projeto.
* Execute o Docker Compose via linha de comando, ou execute os "comandos mágicos" do notebook init_and_config_meltano.ipynb na ordem em que aparecem.

## Etapa 2: Configurar o Meltano
Configure o Meltano utilizando comandos de linha, conforme descrito no arquivo init_and_config_meltano.ipynb. Embora tenha sido utilizado comandos de linha para melhor demonstrar as etapas, recomendo configurar os extractors e loaders através da edição direta do arquivo meltano.yml.

#### Passos:

1 - Criar um Projeto Meltano:

```
sh

meltano init meltano
```

2 - Instalar Extractors e Loaders:

* Entre no diretório meltano e instale os extractors e loaders:

```
sh

cd meltano
meltano add extractor tap-postgres
meltano add extractor tap-csv
meltano add loader target-csv
meltano add loader target-postgres
```

#### Observação. Embora para o melhor entendimento do projeto, a configuração dos extractors e loaders esta demonstrada por uma sequencia de linhas de comandos, recomendo que execute a mesma editando diretamente o arquivo meltano.yml apos o comando acima


3 - Configurar tap-postgres:

* Configure o tap-postgres com as informações do servidor:
```
sh

meltano config tap-postgres set database northwind
meltano config tap-postgres set host localhost
meltano config tap-postgres set port 5432
meltano config tap-postgres set user northwind_user
```
*** Nota: o tap-postgres em conjunto com o target-csv não teve o comportamento esperado, dessa forma foi editado o arquivo *meltano.yml* direwtamente, para garantir o funcionamento desejado dop etl

```
    select:
    - public-*.*
```

4 - Configurar target-postgres:

* Da mesma forma que no passo acima, configure o loader que vai subir os dados tratados para o postgres
```
sh

meltano config target-postgres set database northwind
meltano config target-postgres set host localhost
meltano config target-postgres set port 5432
meltano config target-postgres set user northwind_user
meltano config target-postgres set default_target_schema golden
```

5 - Criar Esquema no Banco de Dados:

* Crie um arquivo .env no diretório meltano com a variável:
  * mesmo o sistema rodando em uma maquina local, por boas praticas optei por escondeer o pasword do postgres em um .env até mesmo para evitar que o github bloqueie o upload do arquivo por expor uma senha
```
TAP_POSTGRES_PASSWORD='sua_senha_aqui'
```

* Utilize a senha do .env para criar um esquema no banco de dados para receber os dados processados, e tambem para configurar o extractor e loader postgres :
  * Por utilizar senha um subprocess no python, optou-se por configurar o schema no banco de dados de destino, assim como os acessos ao postgress em um mesmo bloco de comando

    *o trecho abaixo não representa a totalidade do código, para o código completo, verifique o arquivo *init_and_config_meltano.ipyn*
```
Python

load_dotenv()
password = os.getenv("TAP_POSTGRES_PASSWORD")
command = f"psql -h localhost -U northwind_user -d northwind -c \"CREATE SCHEMA IF NOT EXISTS golden;\""
env = os.environ.copy()
env["PGPASSWORD"] = password
subprocess.run(command, shell=True, env=env, check=True)
```

6 - Configurar o tap-csv com as Informações do Arquivo:

* Configure o tap-csv com as informações do caminho e titulo do arquivo order_details.csv:
```
sh

meltano config tap-csv set files '[{"entity": "order_details", "path": "caminho_para_o_arquivo/order_details.csv", "keys": ["order_id"]}]'
```

7 - Configurar o target-csv com o Caminho de Destino e Esquema de Nomeação de Arquivo:

```
sh

meltano config target-csv set destination_path /caminho_para_o_destino/
meltano config target-csv set file_naming_scheme raw_{stream_name}_{datestamp}.csv
```
8 - Configurar um segundo tap-csv

* Crie um tap-csv--golden para fazer utilizar na etapa final de carregar os dados tratados para de volta para o postgres

```
sh

!meltano add extractor tap-csv--golden --inherit-from tap-csv
!meltano config tap-csv--golden set files '[{"entity": "order-merged-detail", "path": "/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/data/uploaded/to_go/order-merged-detail.csv", "keys": ["order_id"], "delimiter": ",", "encoding": "utf-8", "header": true}]'
```
9 Instalar Plugins:

* Execute o comando para garantir que  as configurações sejam implantadas.

```
sh

meltano install
```

## Etapa 3: Configurando o Airflow


#### Observação: Meltano possui uma ferramenta de orquestração de dados compatível com o Airflow. No entanto, essa ferramenta parece estar desatualizada e não é compatível com versões mais novas do Python. Por isso, optou-se por usar diretamente o Airflow.


#### Passos:
1 - Instalar e Iniciar o Airflow:

* Instale o Airflow via linha de comando:

```
sh

pip install apache-airflow
airflow db init
```

2 - Configurar Diretórios e Arquivos do Airflow:

* Crie um diretório airflow na raiz do projeto:
* Dentro do diretório airflow, crie um subdiretório dags
* Dentro do diretório dags, crie um arquivo chamado dag.py para definir as DAGs e sua ordem de execução:
* Dentro do diretório dags, crie um subdiretório apps para armazenar as funções a serem executadas pelas DAGs:

```
sh

mkdir airflow
mkdir airflow/dags
touch airflow/dags/dag.py
mkdir airflow/dags/apps
```

#### Observação: Garantir que o Airflow leia as DAGs no diretorio do seu projeto.
#### Verifique no arquivo  airflow.cfg dags_folder <span style="color:blue"> dags_folder = </span>

3 - Subir o airflow 

* Utilize o comando para subir o scheduler em segundo plano:
* Utilize o comando para iniciar o webserver do Airflow:

```
sh

airflow scheduler -d
airflow webserver -p 8080
```

## Etapa 4: Configurar as DAGs de ETL

#### Passos:

* Crie um arquivo para armazenar as funções

Na pasta app crie um arquivo específico chamado file_organizer.py para melhorar a modularidade e a legibilidade do código. Isso permite que as funções sejam testadas individualmente e facilita a manutenção e a reutilização do código.

* Explicação das Tasks

#### Task 1: extract_load_postgres
Execução: Executa o comando {et tap-postgres target-csv} para extrair dados do PostgreSQL e salvá-los em arquivos CSV.
Resultado Esperado: Arquivos CSV contendo os dados extraídos do PostgreSQL.


#### Task 2: organize_postgres_files
Execução: Chama a função organize_postgres_files para organizar os arquivos CSV extraídos em pastas nomeadas pelo nome da tabela e pela data da extração.
Resultado Esperado: Arquivos CSV movidos para pastas estruturadas.


#### Task 3: extract_load_csv
Execução: Executa o comando {et tap-csv target-csv} para extrair dados do arquivo CSV disponibilizado.
Resultado Esperado: Arquivos CSV contendo os dados extraídos do arquivo CSV original.


#### Task 4: organize_csv_files
Execução: Chama a função organize_csv_files para organizar os arquivos CSV extraídos em pastas nomeadas pelo nome da tabela e pela data da extração.
Resultado Esperado: Arquivos CSV movidos para pastas estruturadas.



#### Dependências:
Task 2 depende da Task 1.
Task 4 depende da Task 3.

Esse esquema garante que os dados sejam extraídos e organizados de maneira eficiente, com cada task realizando uma etapa específica do processo de ETL e respeitando as dependências necessárias para a integridade do fluxo de dados.

### Observação: confira os arquis gerados na pasta data/upload/raw para garantir que as tasks executaram corretamente


## Etapa 5: Join Data

#### Passos:

1 - Criação da função merge_orders

No diretorio dags/app  Crie uma função que utiliza o pandas para ler os arquivos order e order_details na pasta raw, considerando apenas os arquivos com a data de hoje. Em seguida, realiza um merge dos DataFrames pela chave order_id e salva o DataFrame resultante.

2 - Crie uma task que executa a função.

#### Task 5: merge_orders_task
Execução: executar a função merge_orders, para criar um Arquivos CSV com os dados desejados.
Resultado Esperado: Arquivo .csv com a união dos dados das tabelas ordedr e order-details

## Etapa 6: Subir a tabela tratada de volta para o Postgres

#### Passos:

1 - Preparar o arquivo para preparação do arquivo

Na pasta app defina a função rdy_data_to_go que procuraa tebela tratada com a data igual à da execução da função. Em seguida, salva uma cópia do arquivo em uma pasta específica para ser enviado para o Postgres, substituindo qualquer arquivo existente.

2 - Defina uma task para executar a função rdy_data_to_go

#### Task 6: rdy_data_task
Execução: Executa a função rdy_data_to go.
Resultado Esperado:  Arquivos CSV sem a data no titulo na pasta to_go (o arquivo deve substituir versões anteriores do mesmo).

3 - Defina uma task no DAG para subir os para o Postgres

#### Task 7: upload_golden_db
Execução: Executa o comando {et tap-csv--golden target-postgres} para subir os dados para o postgres
Resultado Esperado: Atualização dos tabelas no schema Golden do banco de dados Nortwind.

#### Dependências

As tasks 5 e 6 devem ser sequenciais e não devem ser executadas caso as tasks 1, 2, 3 e 4 retornem erro de execução.


## Etapa 7: Executar Queries

O banco de dados está pronto para receber queries. 
Foram executadas criadas três queries de exemplo e os resultados foram salvos no diretório queries_results utilizando o comando psql
Criação das Queries
Para executar novas queries modifique o arquivo query.sql, ou execute os comandos diretamente utilizando o psql, ou a forma de acesso de sua preferencia
