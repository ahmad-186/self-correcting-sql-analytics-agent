from math import sqrt

from sqlalchemy import text

from app.database.session import SessionLocal
from app.embeddings import embeddings
from app.config.logging import get_logger

logger = get_logger(__name__)


def get_database_schema() -> dict[str, list[dict]]:
    """
    Retrieve all tables and their columns from PostgreSQL.
    """

    session = SessionLocal()

    try:
        result = session.execute(
            text("""
                SELECT
                    table_name,
                    column_name,
                    data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
            """)
        )

        rows = result.mappings().all()

        schema = {}

        for row in rows:
            table = row["table_name"]

            if table not in schema:
                schema[table] = []

            schema[table].append(
                {
                    "column_name": row["column_name"],
                    "data_type": row["data_type"],
                }
            )

        return schema

    finally:
        session.close()


def get_table_relationships() -> list[dict]:
    """
    Retrieve foreign-key relationships from PostgreSQL.
    """

    session = SessionLocal()

    try:
        result = session.execute(
            text("""
                SELECT
                    tc.table_name AS source_table,
                    kcu.column_name AS source_column,
                    ccu.table_name AS target_table,
                    ccu.column_name AS target_column
                FROM information_schema.table_constraints AS tc

                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema

                JOIN information_schema.constraint_column_usage AS ccu
                    ON tc.constraint_name = ccu.constraint_name
                    AND tc.table_schema = ccu.table_schema

                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = 'public';
            """)
        )

        rows = result.mappings().all()

        return [
            {
                "source_table": row["source_table"],
                "source_column": row["source_column"],
                "target_table": row["target_table"],
                "target_column": row["target_column"],
            }
            for row in rows
        ]

    finally:
        session.close()


def build_schema_documents(
    schema: dict[str, list[dict]]
) -> list[dict]:
    """
    Convert database schema into searchable table documents.
    """

    documents = []

    for table_name, columns in schema.items():

        column_text = ", ".join(
            f"{column['column_name']} ({column['data_type']})"
            for column in columns
        )

        text_content = (
            f"Table: {table_name}. "
            f"Columns: {column_text}"
        )

        documents.append(
            {
                "table_name": table_name,
                "text": text_content,
            }
        )

    return documents


def _cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """
    Calculate cosine similarity between two vectors.
    """

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = sqrt(
        sum(a * a for a in vector_a)
    )

    magnitude_b = sqrt(
        sum(b * b for b in vector_b)
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (magnitude_a * magnitude_b)


def keyword_score(
    question: str,
    table_name: str,
    columns: list[dict],
) -> int:
    """
    Calculate lexical relevance between the question
    and a table.
    """

    question_tokens = set(
        question.lower().replace("?", "").split()
    )

    score = 0

    table_words = set(
        table_name.lower().split("_")
    )

    score += len(
        question_tokens.intersection(table_words)
    )

    for column in columns:

        column_words = set(
            column["column_name"]
            .lower()
            .split("_")
        )

        score += len(
            question_tokens.intersection(column_words)
        )

    return score


def hybrid_table_search(
    question: str,
    schema: dict[str, list[dict]],
    top_k: int = 3,
) -> list[str]:
    """
    Retrieve relevant tables using both lexical and
    semantic similarity.
    """

    documents = build_schema_documents(schema)

    # Embed the user question
    question_embedding = embeddings.embed_query(question)

    scored_tables = []

    lexical_scores = []

    for document in documents:

        table_name = document["table_name"]

        lexical = keyword_score(
            question,
            table_name,
            schema[table_name],
        )

        lexical_scores.append(lexical)

    max_lexical = max(lexical_scores, default=1)

    for document in documents:

        table_name = document["table_name"]

        lexical = keyword_score(
            question,
            table_name,
            schema[table_name],
        )

        lexical_normalized = (
            lexical / max_lexical
            if max_lexical > 0
            else 0
        )

        table_embedding = embeddings.embed_query(
            document["text"]
        )

        semantic = _cosine_similarity(
            question_embedding,
            table_embedding,
        )

        # Hybrid score
        final_score = (
            0.4 * lexical_normalized
            + 0.6 * semantic
        )

        scored_tables.append(
            (
                table_name,
                final_score,
            )
        )

    scored_tables.sort(
        key=lambda item: item[1],
        reverse=True,
    )

    return [
        table
        for table, score in scored_tables[:top_k]
        if score > 0
    ]


def expand_related_tables(
    relevant_tables: list[str],
    relationships: list[dict],
) -> list[str]:
    """
    Add only the tables required to connect the initially
    retrieved relevant tables.

    Example:
        customers + orders
    will remain:
        customers + orders

    It will NOT expand further to:
        order_items + products
    """

    relevant = set(relevant_tables)

    if len(relevant) <= 1:
        return list(relevant)

    # Build an undirected relationship graph
    graph: dict[str, set[str]] = {}

    for relationship in relationships:

        source = relationship["source_table"]
        target = relationship["target_table"]

        graph.setdefault(source, set()).add(target)
        graph.setdefault(target, set()).add(source)

    expanded = set(relevant)

    # Find shortest paths between relevant candidate tables.
    for start in relevant:

        queue = [(start, [start])]
        visited = {start}

        while queue:

            current, path = queue.pop(0)

            # We reached another relevant table.
            if (
                current != start
                and current in relevant
            ):
                expanded.update(path)
                break

            for neighbor in graph.get(current, set()):

                if neighbor not in visited:

                    visited.add(neighbor)

                    queue.append(
                        (
                            neighbor,
                            path + [neighbor]
                        )
                    )

    return list(expanded)


def build_schema_context(
    relevant_tables: list[str],
    schema: dict[str, list[dict]],
) -> str:
    """
    Build an LLM-friendly schema description.
    """

    context_parts = []

    for table in relevant_tables:

        context_parts.append(
            f"Table: {table}"
        )

        for column in schema[table]:

            context_parts.append(
                f"- {column['column_name']} "
                f"({column['data_type']})"
            )

        context_parts.append("")

    return "\n".join(context_parts)


def inspect_schema(question: str) -> dict:
    """
    Retrieve and format the relevant database schema.
    """

    logger.info("Retrieving database schema")

    schema = get_database_schema()

    logger.info(
        "Database schema retrieved. Tables found: %d",
        len(schema)
    )

    relationships = get_table_relationships()

    logger.info(
        "Database relationships retrieved. Relationships found: %d",
        len(relationships)
    )

    # Step 1: Hybrid retrieval
    candidate_tables = hybrid_table_search(
        question=question,
        schema=schema,
    )

    logger.info(
        "Hybrid schema search returned candidate tables: %s",
        candidate_tables
    )


    # Step 2: Relationship expansion
    relevant_tables = expand_related_tables(
        relevant_tables=candidate_tables,
        relationships=relationships,
    )

    logger.info(
        "Relevant tables after relationship expansion: %s",
        relevant_tables
    )

    # Step 3: Build schema context
    schema_context = build_schema_context(
        relevant_tables=relevant_tables,
        schema=schema,
    )

    logger.info("Schema context successfully generated")

    return {
        "database_schema": schema,
        "schema_context": schema_context,
    }