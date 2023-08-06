from helper.base.writer import EnhancedWriter
from helper.plugin.etl_base import DataGroup, ModelFile, PluginBase


class Plugin(PluginBase):
    def write_group(self, group: DataGroup, w: EnhancedWriter):
        w.write("SELECT\n")
        for i in range(len(group.data)):
            d = group.data[i]
            w.write(f"    {d.mapping_rule} AS {d.column_name}")
            if i < len(group.data) - 1:
                w.write(",")
            w.write(f"    -- {d.column_cn_name}")
            w.write("\n")

        mt = group.main_table()
        w.write(f"FROM {mt.source_table} {mt.source_table_id}\n")
        for d in filter(lambda x: x.is_join(), group.data):
            w.write(
                f"{d.join_type} {d.source_table} {d.source_table_id} {d.join_on_condition}\n"
            )
        w.write(f"{mt.where_condition};\n")

    def write_etl_script(self, model: ModelFile, writer: EnhancedWriter):
        function_name = "dcx_" + model.table_name
        if model.schema is not None:
            function_name = f"{model.schema}.dcx_{model.table_name}"
        writer.writeln(
            f"CREATE OR REPLACE FUNCTION {function_name}(IN p_date int4, OUT p_srccnt int4, OUT p_dstcnt int4) AS $$"
        )
        writer.writeln("BEGIN")
        writer.writeln()

        temp_table_name = "tmp_" + model.table_name
        writer.writeln(f"DROP TABLE IF EXISTS {temp_table_name};")
        writer.writeln(
            f"CREATE TEMPORARY TABLE {temp_table_name} AS (SELECT * FROM {model.target_table_name} WHERE 1=2);"
        )
        for group in model.data:
            if group.group_id is None:
                continue
            writer.writeln(f"-- Group {group.group_id}")
            writer.writeln(f"INSERT INTO {temp_table_name}")
            self.write_group(group, writer)

        writer.writeln(f"DELETE FROM {model.target_table_name} WHERE dcdate=p_date;")
        writer.writeln(
            f"INSERT INTO {model.target_table_name} SELECT * FROM {temp_table_name};"
        )
        writer.writeln()
        writer.writeln(f"SELECT count(1) INTO p_srccnt FROM {temp_table_name};")
        writer.writeln("p_dstcnt := p_srccnt;")
        writer.writeln()
        writer.writeln("END;")
        writer.writeln("$$ LANGUAGE plpgsql;")

    def write_ddl_script(self, model: ModelFile, w: EnhancedWriter):
        w.writeln(f"-- Table: {model.target_table_name} {model.target_table_cn_name}")
        pks = model.get_primary_keys()
        w.writeln(f"CREATE TABLE {model.target_table_name} (")
        group = model.data[0]
        for i in range(len(group.data)):
            d = group.data[i]
            w.write(f"    {d.column_name} {d.column_type} {d.column_null_str}")
            if i < len(group.data) - 1 or len(pks) > 0:
                w.write(",")
            w.writeln(f"    -- {d.column_cn_name}")
        if len(pks) > 0:
            w.writeln(
                f"    CONSTRAINT pk_{model.table_name} PRIMARY KEY ({','.join(pks)})"
            )

        w.writeln(f");")

        w.writeln(
            f"COMMENT ON TABLE {model.target_table_name} IS '{model.target_table_cn_name}';"
        )
        for i in range(len(group.data)):
            d = group.data[i]
            w.writeln(
                f"COMMENT ON COLUMN {model.target_table_name}.{d.column_name} IS '{d.column_cn_name}';"
            )
