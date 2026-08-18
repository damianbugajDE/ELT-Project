{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set default_schema = target.schema -%}
    
    {# If this is production (Airflow / target prod), use the default schema or custom one (e.g., silver, gold_finance) #}
    {%- if target.name == 'prod' -%}
        {%- if custom_schema_name is none -%}
            {{ default_schema }}
        {%- else -%}
            {{ custom_schema_name | trim }}
        {%- endif -%}
        
    {# If this is the local environment (dev), EVERYTHING lands in a single 'sandbox' schema #}
    {%- else -%}
        sandbox
    {%- endif -%}
{%- endmacro %}