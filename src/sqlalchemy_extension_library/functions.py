
from sqlalchemy.sql.functions import GenericFunction
from sqlalchemy.ext.compiler import compiles
from sqlachemy import String


# [IMPORTANT] : this is oddly specific as it only accepts a single argument and a separator
# for more info see: https://docs.sqlalchemy.org/en/20/core/compiler.html
class group_concat_distinct(sqlalachemy.sql.expression.FunctionElement):
    """
    #### DESCRIPTION:
    GROUP_CONCAT(DISTINCT expr ORDER BY expr SEPARATOR ', ') made for MariaDB/MySQL.
    SQLAlchemy func.group_concat does not support `DISTINCT`+ `ORDER BY` + `SEPARATOR`
    """

    # this is the return type
    type = sa.types.String()
    name = "group_concat_distinct"

    # True: enables the query compilation cache
    inherit_cache = True

    def __init__(
        self,

        # NOTE: no type for expression since it can be anything
        # [EXAMPLE]: sa.sql.expression.ColumnElement | sa.sql.expression.ClauseElement | sa.orm.Mapped,
        expression,
        separator: str = ", ",
    ) -> None:
        super().__init__(
            expression,
            sqlalachemy.bindparam(
                key   = None, # key is not required
                value = separator,
                type_ = sqlalachemy.types.String(), # separator type

                # [IMPORTANT] : this is required since `separator` accepts
                # only a string, not a possible placeholder (%s / ?)
                # (also should be safe from sql injections, since it does the escape of the value)
                literal_execute = True,
            ),
        )
    # #enddef __init__
# #endclass group_concat_distinct

# SQL COMPILER
@compiles(group_concat_distinct) # default compiler
@compiles(group_concat_distinct, "mysql")
@compiles(group_concat_distinct, "mariadb")
def _compile_group_concat(
    element  : group_concat_distinct       ,
    compiler : sqlalchemy.sql.compiler.SQLCompiler ,
    **kw     : dict                        ,
) -> str:
    """
    #### DESCRIPTION:
    SQL Compiler for `group_concat_distinct` registered for MariaDB & MySQL dialects.
    Translates the elements in GROUP_CONCAT(DISTINCT <expression> ORDER BY <expression> SEPARATOR <separator>)

    #### NOTES:
    - SQLAlchemy calls this method automatically, when a query that contains a `group_concat_distinct` is compiled
    and `MUST NOT` be called manually.:
    - Data is automatically truncated at `group_concat_max_len`. if thiss occurs, set `group_concat_max_len`
    to a higher value in the session that calls `group_concat_distinct`.
    for more info see:
        - MySQL   : https://dev.mysql.com/doc/refman/9.7/en/server-system-variables.html#sysvar_group_concat_max_len
        - MariaDB : https://mariadb.com/docs/server/server-management/variables-and-modes/server-system-variables#group_concat_max_len
    """

    # get the separator and the expression from the element
    expression, separator = element.clauses.clauses

    expression_processed = compiler.process(expression, **kw)
    separator_processed  = compiler.process(separator , **kw)

    return f"GROUP_CONCAT(DISTINCT {expression_processed} ORDER BY {expression_processed} SEPARATOR {separator_processed})"
# #enddef _compile_group_concat
