import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Lista de arquivos CSV
csv_files = ["categories.csv", "orders.csv", "products.csv", "region.csv", "shippers.csv", 
             "suppliers.csv", "territories.csv", "us_states.csv", "customer_customer_demo.csv",
             "customer_demographics.csv", "customers.csv", "employee_territories.csv", "employees.csv",
             "order_details.csv"]


# Função para criar os dataframes para cada tabela
def read_csv_files():
    dfs = {}
    for file in csv_files:
        name = file.split(".")[0]
        dfs[name] = pd.read_csv(file, sep=";")
    return dfs

dfs = read_csv_files()

orders = dfs['orders']
order_details = dfs['order_details']
products = dfs['products']

# Convertendo a coluna de data para datetime
orders['order_date'] = pd.to_datetime(orders['order_date'])
orders['month'] = orders['order_date'].dt.month
orders['year'] = orders['order_date'].dt.year

# Filtrando os pedidos dos últimos 3 anos
years = [1996, 1997, 1998]

for year in years:
    orders_year = orders[orders['year'] == year]
    merged_data = pd.merge(orders_year, order_details, on='order_id')
    merged_data = pd.merge(merged_data, products, on='product_id')
    # Faturamento mensal
    merged_data['total_price'] = merged_data['quantity'] * merged_data['unit_price_x']
    value_counts = merged_data.groupby('month')['total_price'].sum()
    value_counts = value_counts.sort_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=value_counts.index, y=value_counts.values, hue=value_counts.index, palette='magma', legend=False)
    plt.title(f'Faturamento mensal (R$) em nos meses do ano {year}')
    plt.xlabel('Mês')
    plt.ylabel('Faturamento')
    plt.grid()
    plt.show()
    total_price = merged_data['total_price'].sum()
    print(f'Faturamento total em {year}: R$ {total_price:.2f}')

    # Soma as quantidades de produtos de cada mês especifico
    value_counts = merged_data.groupby('month')['quantity'].sum()
    value_counts = value_counts.sort_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=value_counts.index, y=value_counts.values, hue=value_counts.index, palette='viridis', legend=False)
    plt.title(f'Vendas mensais em {year}')
    plt.xlabel('Mês')
    plt.ylabel('Quantidade de produtos vendidos')
    plt.grid()
    plt.show()
    # Valor do ticket médio mensal
    value_counts = merged_data.groupby('month')['total_price'].mean()
    value_counts = value_counts.sort_index()
    plt.figure(figsize=(10, 5))
    sns.barplot(x=value_counts.index, y=value_counts.values, legend=False)
    plt.title(f'Valor (R$) do ticket médio mensal em {year}')
    plt.xlabel('Mês')
    plt.ylabel('Valor do ticket médio')
    plt.grid()
    plt.show()



# 10 produtos mais vendidos em 1996, 1997 e 1998
for year in years:
    orders_year = orders[orders['year'] == year]
    merged_data = pd.merge(orders_year, order_details, on='order_id')
    merged_data = pd.merge(merged_data, products, on='product_id')
    value_counts = merged_data.groupby('product_name')['quantity'].sum()
    value_counts = value_counts.sort_values(ascending=False).head(10)
    plt.figure(figsize=(10, 10))
    sns.barplot(x=value_counts.index, y=value_counts.values, palette='hot')
    plt.title(f'10 produtos mais vendidos em {year}')
    plt.xlabel('Produto')
    plt.ylabel('Quantidade de produtos vendidos')
    plt.xticks(rotation=15)
    plt.grid()
    plt.show()

    value_counts = value_counts.sort_values(ascending=True).head(5)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=value_counts.index, y=value_counts.values, palette='cool')
    plt.title(f'5 produtos menos vendidos em {year}')
    plt.xlabel('Produto')
    plt.ylabel('Quantidade de produtos vendidos')
    plt.xticks(rotation=15)
    plt.grid()
    plt.show()



# As categorias de produtos mais vendidas da empresa
merged_data = pd.merge(order_details, products, on='product_id')
categories = dfs['categories']
merged_data = pd.merge(merged_data, categories, on="category_id")
value_counts = merged_data.groupby('category_name')['quantity'].sum()
value_counts = value_counts.sort_values(ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(x=value_counts.index, y=value_counts.values, palette='spring')
plt.title('Categorias de produtos mais vendidas')
plt.xlabel('Categoria')
plt.ylabel('Quantidade de produtos vendidos')
plt.grid()
plt.show()

# Distribuição de pedidos da empresa por países
value_count = orders.groupby('ship_country')
value_count = value_count.size()
value_count = value_count.sort_values(ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(x=value_count.index, y=value_count.values, palette='summer')
plt.title('Distribuição de pedidos da empresa por países')
plt.xlabel('País')
plt.ylabel('Quantidade de pedidos')
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Gráfico de pizza
plt.figure(figsize=(10, 5))
# Filtrando os países com quantidade de pedidos maior que 10
filtered_value_count = value_count[value_count > 10]
plt.pie(filtered_value_count.values, labels=filtered_value_count.index, autopct='%1.1f%%', startangle=90)
plt.title('Distribuição de pedidos da empresa por países')
plt.legend(bbox_to_anchor=(1, 2), loc='center left', fontsize='small')
plt.show()

orders_USA = orders.groupby('USA')
orders_USA = orders_USA.size()
orders_USA = orders_USA.sort_values(ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(x=orders_USA.index, y=orders_USA.values, palette='winter')
plt.title('Distribuição de pedidos da empresa nos EUA')
plt.xlabel('Estado')
plt.ylabel('Quantidade de pedidos')
plt.xticks(rotation=45)
plt.grid()
plt.show()

employees = dfs['employees']
employee_territories = dfs['employee_territories']
territories = dfs['territories']

merged_data = pd.merge(employees, employee_territories, on='employee_id')
merged_data = pd.merge(merged_data, territories, on='territory_id')
merged_data = merged_data.loc[:, ["employee_id", "first_name", "last_name", "territory_description"]]
print(merged_data)

merged_data = pd.merge(merged_data, orders, on="employee_id")
value_count = merged_data.groupby('first_name')
value_count = value_count.size()
value_count = value_count.sort_values(ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(x=value_count.index, y=value_count.values, hue=value_count.index, legend=False, palette='autumn')
plt.title('Distribuição de pedidos por funcionário')
plt.xlabel('Funcionário')
plt.ylabel('Quantidade de pedidos')
plt.grid()
plt.show()

valid_products = products[products['discontinued'] == 0]
merged_data = pd.merge(order_details, orders, on="order_id")
merged_data = pd.merge(merged_data, valid_products, on='product_id')
# Seleciona um produto aleatorio
product = merged_data.sample()
product_name = product['product_name'].values[0]
# Avalia o preço desse produto ao longo do tempo
product = merged_data[merged_data['product_name'] == product_name]
value_counts_2 = product.groupby('order_date')['unit_price_x'].mean()
plt.figure(figsize=(10, 5))
sns.lineplot(x=value_counts_2.index, y=value_counts_2.values, marker='o')
plt.title(f'Preço do produto {product_name} ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Preço')
plt.grid()
plt.show()



