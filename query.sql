-- Export orders from 1997 to CSV and JSON
\copy (SELECT * FROM golden.order_merged_detail WHERE EXTRACT(YEAR FROM order_date::DATE) = 1997) TO '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/queries_reults/orders_1997.csv' WITH CSV HEADER;
\copy (SELECT json_agg(t) FROM (SELECT * FROM golden.order_merged_detail WHERE EXTRACT(YEAR FROM order_date::DATE) = 1997) t) TO '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/queries_reults/orders_1997.json';

-- Export today's orders to CSV and JSON
\copy (SELECT * FROM golden.order_merged_detail WHERE order_date::DATE = CURRENT_DATE) TO '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/queries_reults/orders_today.csv' WITH CSV HEADER;
\copy (SELECT json_agg(t) FROM (SELECT * FROM golden.order_merged_detail WHERE order_date::DATE = CURRENT_DATE) t) TO '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/queries_reults/orders_today.json';

-- Export orders since 1998 to CSV and JSON
\copy (SELECT * FROM golden.order_merged_detail WHERE order_date::DATE >= '1998-01-01') TO '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/queries_reults/orders_since_1998.csv' WITH CSV HEADER;
\copy (SELECT json_agg(t) FROM (SELECT * FROM golden.order_merged_detail WHERE order_date::DATE >= '1998-01-01') t) TO '/home/tigureis/DNC_engenharia_de_dados/Indicium_Tech_Code_Challenge/queries_reults/orders_since_1998.json';