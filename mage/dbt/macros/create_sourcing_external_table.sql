-- macros/create_sourcing_external_table.sql

{% macro create_sourcing_external_table(project_name, dataset_name, table_name, csv_uri) %}
CREATE OR REPLACE EXTERNAL TABLE `{{ project_name }}.{{ dataset_name }}.{{ table_name }}`
OPTIONS (
  format='CSV',
  field_delimiter=';',
  skip_leading_rows=1,
  allow_quoted_newlines=true,
  uris = [{{ csv_uri }}]
);
{% endmacro %}