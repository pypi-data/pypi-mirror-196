"""
`delete` command
"""
from typing import List

from mindflow.db.controller import DATABASE_CONTROLLER
from mindflow.db.objects.document import Document
from mindflow.resolving.resolve import resolve_all


def run_delete(document_paths: List[str]):
    """
    This function is used to delete your MindFlow index.
    """
    documents_references = [
        document_reference.path for document_reference in resolve_all(document_paths)
    ]
    documents_to_delete = [
        document.path for document in Document.load_bulk(documents_references)
    ]

    if len(documents_to_delete) == 0:
        return "No documents to delete"

    Document.delete_bulk(documents_to_delete)

    DATABASE_CONTROLLER.databases.json.save_file()
    return "Documents deleted"
