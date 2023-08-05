import logging
import os
import textwrap
from datetime import datetime
from functools import lru_cache
from typing import Optional

from pyocient.api import Connection, SQLException


def openai_completion(prompt: str, model: str, temperature: float) -> str:
    import openai

    openai.api_key = os.getenv("OPENAI_API_KEY")

    logging.debug("Submitting prompt to OpenAI %s: %s", model, prompt)
    completion = openai.ChatCompletion.create(  # type:ignore[no-untyped-call]
        model=model,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    logging.debug("OpenAI response: %s", completion)
    return str(completion["choices"][0]["message"]["content"])


def anthropic_completion(prompt: str, model: str, temperature: float) -> str:
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    modified_prompt = f"{anthropic.HUMAN_PROMPT} {prompt}{anthropic.AI_PROMPT}"
    logging.debug("Submitting prompt to Anthropic %s: %s", model, prompt)
    completion = client.completions.create(
        prompt=modified_prompt,
        stop_sequences=[anthropic.HUMAN_PROMPT],
        model=model,
        max_tokens_to_sample=1024,
        temperature=temperature,
    )
    logging.debug("Anthropic response: %s", completion)
    return str(completion.completion)


@lru_cache()
def get_db_context(conn: Connection, *, with_sys_catalog: bool = False) -> str:
    """
    Assemble a sequence of `CREATE TABLE` statements generated from all
    user-defined tables in this connection's database, as well as system
    catalog tables, if requested.

    This function's results will be cached per connection and
    per-`with_sys_catalog`. Note that if `with_sys_catalog` is `True`, it will
    take about a minute to export all of the catalog tables for each connection.
    """
    with conn.cursor() as cursor:
        # Get all user-defined tables in this connection's database
        tables = cursor.execute(
            f"""
            SELECT table_schema AS schema, table_name AS name
            FROM information_schema.tables
            WHERE
                table_type = 'BASE TABLE'
                AND table_catalog = '{conn.database}'
            """
        ).fetchall()
        if cursor.description is None:
            logging.warning("Cursor has no description fetching user-defined tables")
            return "No table information available (cursor has no description)"
        if not len(tables):
            logging.warning("No tables found in database %s", conn.database)
            return "Connection has no table information (are you connected to the right database?)"

        # Export each table to DDL and include this in the LLM's context
        context = ""
        for table in tables:
            assert hasattr(table, "schema") and isinstance(table.schema, str)
            assert hasattr(table, "name") and isinstance(table.name, str)
            result = cursor.execute(f'EXPORT TABLE "{table.schema}"."{table.name}"').fetchone()
            if result is None:
                logging.warning("EXPORT TABLE %s did not return result", table.name)
                continue
            assert isinstance(result[0], str)
            context += result[0]
            context += "\n\n"

        # Get all the sys tables
        # TODO consider parallelizing this, it's slow...
        if with_sys_catalog:
            sys_tables = cursor.execute(
                "SELECT table_name AS name FROM information_schema.tables WHERE table_schema = 'sys' ORDER BY table_name"
            ).fetchall()
            if cursor.description is None:
                logging.warning("Cursor has no description fetching sys tables")
                return "No table information available (cursor has no description)"
            if not len(sys_tables):
                logging.warning("No sys tables found in system %s (port %s)", str(conn.hosts), conn.port)
                return "Connection has no system catalog information"

            # Check if the `sys.system_table_columns` table has a `description` column
            try:
                cursor.execute("SELECT description FROM sys.system_table_columns LIMIT 1").fetchall()
            except SQLException as e:
                if "reference to column 'description' is not valid" in str(e):
                    supports_description = False
                else:
                    raise
            else:
                supports_description = True

            # Get the column information of all catalog tables
            for table in sys_tables:
                assert hasattr(table, "name") and isinstance(table.name, str)
                columns = cursor.execute(
                    f"""
                    SELECT column_name, c.data_type, is_nullable{", description" if supports_description else ""}
                    FROM information_schema.columns c
                    JOIN sys.system_table_columns s ON c.column_name = s.name AND c.table_name = s.table_name
                    WHERE
                        table_schema = 'sys'
                        AND c.table_name = '{table.name}'
                    """
                ).fetchall()
                if cursor.description is None:
                    logging.warning("Cursor has no description fetching columns for %s", table.name)
                    continue
                if not len(columns):
                    logging.warning("No columns found for %s", table.name)
                    continue
                context += f'CREATE TABLE "sys"."{table.name}" (\n'
                for column in columns:
                    assert hasattr(column, "column_name") and isinstance(column.column_name, str)
                    assert hasattr(column, "data_type") and isinstance(column.data_type, str)
                    assert (
                        hasattr(column, "is_nullable")
                        and isinstance(column.is_nullable, str)
                        and column.is_nullable in ["NO", "YES"]
                    )
                    context += f'    "{column.column_name}" {column.data_type}'
                    if column.is_nullable == "YES":
                        context += " NULL,"
                    else:
                        context += " NOT NULL,"
                    if supports_description:
                        assert hasattr(column, "description") and isinstance(column.description, str)
                        if column.description:
                            context += f" -- {column.description}"
                    context += "\n"
                context = context[:-2] + "\n"  # Remove trailing comma
                context += ");\n\n"

    return context.strip()


DEFAULT_MODELS_BY_BACKEND = {
    "anthropic": "claude-1.3",
    "openai": "gpt-3.5-turbo-16k",
}


def is_supported_backend(backend: str) -> bool:  # Add dep on typing_extensions or python>=3.10 to use TypeGuard
    return backend in DEFAULT_MODELS_BY_BACKEND


def text2sql(
    conn: Connection,
    text: str,
    *,
    backend: str,
    model: Optional[str] = None,
    temperature: float = 0.2,
    with_sys_catalog: bool = False,
) -> str:
    """
    For a given database connection and plaintext question, ask a Large
    Language Model (LLM) to generate a SQL query to answer the question. To aid
    its answer, the LLM will be provided with the results of an `EXPORT TABLE`
    statement for each table available to the connected user.

    Warning: do not send sensitive tables or questions to these backends.

    If the backend is `openai`, then `OPENAI_API_KEY` must be set in the
    environment. The `openai` Python package must be importable. The model will
    default to `gpt-3.5-turbo-16k`. Available models are documented at
    https://platform.openai.com/docs/models/overview.

    If the backend is `anthropic`, then `ANTHROPIC_API_KEY` must be set in the
    environment. The `anthropic` Python package must be importable. The model
    will default to `claude-1.3`. Available models are documented at
    https://docs.anthropic.com/claude/reference/complete_post.

    Note that a SQL query is *not guaranteed* to be returned, as the output of
    the LLMs is fundamentally non-deterministic. Callers must check the
    returned value for the purposes of their use of it.
    """

    context = get_db_context(conn, with_sys_catalog=with_sys_catalog)
    today = datetime.today()
    prompt = textwrap.dedent(
        f"""
        You are a precise technical assistant designed to enable users to explore their databases more naturally
        and effectively.

        The current date is {today.strftime('%Y-%m-%d')}. The current time is {today.strftime('%H:%M:%S')}. You
        are connected to an Ocient database named "{conn.database}". This database contains the following tables:

{textwrap.indent(context, " " * len("        "))}

        Ocient tables are referred to by both their schema and table names separated by a period. When referring
        to Ocient tables, always refer to a given CREATE TABLE "foo"."bar" by its full name "foo"."bar". You must
        exactly refer to this name, e.g. if the statement is CREATE TABLE "sys"."segments", you must write
        queries that refer to "sys"."segments" by the full name.

        You may be familiar with a `PERCENTILE_CONT` function supported by other databases. Ocient does not
        support `PERCENTILE_CONT`. Instead it provides `PERCENTILE`. Whereas the syntax of `PERCENTILE_CONT`
        is coupled with a `WITHIN GROUP` clause, Ocient's `PERCENTILE` function` uses `OVER`, e.g. to compute
        the median of a column, `SELECT PERCENTILE(col, 0.5) OVER (ORDER BY col) FROM table LIMIT 1`. Note that
        using `PERCENTILE` as a scalar subquery requires a `LIMIT 1` on the subquery.

        "count" is a reserved word in Ocient. "count" cannot be used as an output column name. Do not use `AS count`.

        Using this information, answer the user's question about the database as precisely as possible. Your response
        should be ONE OF an ANSI SQL query or a plain language answer to the user's question, but not both. As a
        guideline, questions about the database, table, or schema should be answered in plain language, whereas
        questions about the data stored within should be answered with a SQL query. Do not explain your SQL queries
        in any way. Do not preface your queries with any other text. If your query contains a semicolon, all content
        after the semicolon will be ignored.

        Question: {text}
        Answer:
        """
    ).strip()

    if not is_supported_backend(backend):
        raise NotImplementedError(f'Unsupported backend "{backend}"')

    if model is None:
        model = DEFAULT_MODELS_BY_BACKEND[backend]

    if backend == "openai":
        return openai_completion(prompt, model, temperature)
    if backend == "anthropic":
        return anthropic_completion(prompt, model, temperature)

    raise AssertionError("unreachable")
